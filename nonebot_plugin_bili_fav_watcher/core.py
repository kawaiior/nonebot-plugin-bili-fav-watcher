import asyncio
import time

from nonebot import require, get_bots, logger, on_command
from bilibili_api.favorite_list import get_video_favorite_list, get_video_favorite_list_content
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, Bot

from .config import WATCH_USER_DATA, USER_FAV_MEDIA_CACHE, SLEEP_INTERVAL, CACHE_CLEANUP_THRESHOLD, \
    INTERVAL_BETWEEN_RUNS, NEW_VIDEO_THRESHOLD, is_admin
from .util import get_bili_user_name


async def _watch_users(bot: Bot):
    count = 0

    logger.info("开始遍历收藏夹")

    # 构建一个uid list
    uids = []
    for user_id in WATCH_USER_DATA.keys():
        uids.append(user_id)

    try:
        for user_id in uids:
            int_user_id = int(user_id)
            group_ids = WATCH_USER_DATA[user_id]

            fav_cache = USER_FAV_MEDIA_CACHE.get(str(user_id), {})

            user_name = "获取用户名失败"
            try:
                # 拿到用户个人信息
                user_name = await get_bili_user_name(int_user_id)
                # 防止风控
                await asyncio.sleep(SLEEP_INTERVAL)
            finally:
                pass

            response = await get_video_favorite_list(int_user_id)
            # 这里response可能是None
            if response is None:
                # 如果没拿到response，那么就跳过这个用户
                logger.info(f"用户 {user_name} 未公开收藏夹")
                continue

            fav_list = response.get('list')

            now_time = time.time()

            # 遍历收藏夹
            for fav in fav_list:
                fav_items = await get_video_favorite_list_content(fav.get("id"))
                fav_medias = fav_items.get('medias')

                # 遍历收藏夹内的视频
                for media in fav_medias:
                    fav_time = media.get('fav_time')
                    media_id = media.get('id')

                    # 计算时间
                    time_ago = now_time - fav_time

                    if time_ago < NEW_VIDEO_THRESHOLD and str(media_id) not in fav_cache.keys():
                        count += 1

                        logger.info("检测到新收藏的视频，开始推送")
                        # 缓存已推送的视频信息
                        fav_cache[str(media_id)] = fav_time

                        title = media.get('title')
                        intro = media.get('intro')
                        cover = media.get('cover')
                        bvid = media.get('bvid')

                        msg = f"{user_name} 在{time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(fav_time))}收藏了新视频\n" \
                              f"标题：{title}\n" \
                              f"简介：{intro}\n" \
                              f"链接：https://www.bilibili.com/video/{bvid}\n" + MessageSegment.image(cover)

                        for group_id in group_ids:
                            await bot.send_msg(message_type="group", group_id=group_id, message=msg)
                            # 防止风控
                            await asyncio.sleep(SLEEP_INTERVAL)
                    else:
                        # 如果视频已经推送了，那么就直接结束循环，因为fav_medias已经是时间排序了
                        break

            # 清理缓存
            del_list = []

            for media_id, fav_time in fav_cache.items():
                time_ago = now_time - fav_time
                if time_ago > CACHE_CLEANUP_THRESHOLD:
                    del_list.append(media_id)

            if len(del_list) > 0:
                logger.info(f"清理了{len(del_list)}条数据")
                for media_id in del_list:
                    del fav_cache[media_id]

            # 保存
            USER_FAV_MEDIA_CACHE[str(user_id)] = fav_cache

            logger.info(f"已遍历完用户 {user_name} 的所有收藏夹")
    except Exception as e:
        logger.exception(e)
    finally:
        pass

    logger.info("操作结束")

    return count


watch_now = on_command("favw_now", aliases={"开始视奸"})
@watch_now.handle()
async def _(bot: Bot, event: MessageEvent):
    if not is_admin(event.user_id):
        await watch_now.finish("权限不足", reply_message=True)
        return

    count = await _watch_users(bot)

    await bot.finish(f"操作结束，共推送了{count}条消息", reply_message=True)


pusher = require("nonebot_plugin_apscheduler").scheduler


@pusher.scheduled_job("interval", seconds=INTERVAL_BETWEEN_RUNS, id="fav_sched")
async def _():

    try:
        # 获取bot
        bot, = get_bots().values()
        await _watch_users(bot)

    except Exception as e:
        logger.exception(e)
    finally:
        pass
