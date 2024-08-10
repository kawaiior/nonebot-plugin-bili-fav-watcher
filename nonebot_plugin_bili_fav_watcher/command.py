from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.internal.params import ArgStr
from nonebot.params import CommandArg

from .config import is_admin, WATCH_USER_DATA, save_config
from .util import get_bili_user_name


async def _add_uid_watch(bot: Bot, event: GroupMessageEvent, uid: str):
    try:
        # 获取用户名 用于判断uid是否存在
        user_name = await get_bili_user_name(int(uid))
    except Exception as e:
        if "啥都木有" in str(e):
            await bot.send(event=event, message="uid不存在", reply_message=True)
        else:
            logger.exception(e)
            await bot.send(event=event, message="获取用户名时遇到了未知错误，详细信息请查看控制台", reply_message=True)
        return
    finally:
        pass
    # 添加uid到监控列表
    if uid in WATCH_USER_DATA.keys():
        WATCH_USER_DATA[uid].append(event.group_id)
    else:
        WATCH_USER_DATA[uid] = [event.group_id]
    # 保存
    save_config()
    await bot.send(event=event, message=f"B站用户 `{user_name}` 已添加至监听列表", reply_message=True)

add_watch = on_command("favw", aliases={"视奸"})
@add_watch.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not is_admin(event.user_id):
        await add_watch.finish("权限不足")
        return
    # 参数处理
    uid = str(arg).replace(" ", "")
    if uid == "" or not uid.isdigit():
        await bot.send(event=event, message="请输入用户uid", reply_message=True)
    else:
        # 处理
        await _add_uid_watch(bot, event, uid)
        await add_watch.finish()

@add_watch.got("uid")
async def _(bot: Bot, event: GroupMessageEvent, uid: str = ArgStr("uid")):
    uid = str(uid).replace(" ", "")
    if uid == "" or not uid.isdigit():
        await add_watch.finish("非法uid", reply_message=True)
    else:
        # 处理
        await _add_uid_watch(bot, event, uid)
        await add_watch.finish()


async def _remove_uid_watch(bot: Bot, event: GroupMessageEvent, uid: str):
    # 删除uid
    if uid in WATCH_USER_DATA.keys():
        if event.group_id in WATCH_USER_DATA[uid]:
            WATCH_USER_DATA[uid].remove(event.group_id)
            save_config()
            await bot.send(event=event, message="uid删除成功", reply_message=True)
        else:
            await bot.send(event=event, message="uid不在列表中", reply_message=True)
    else:
        await bot.send(event=event, message="uid不在列表中", reply_message=True)


del_watch = on_command("off_favw", aliases={"取消视奸"})
@del_watch.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not is_admin(event.user_id):
        await del_watch.finish("权限不足")
        return
    # 参数处理
    uid = str(arg).replace(" ", "")
    if uid == "" or not uid.isdigit():
        await bot.send(event=event, message="请输入用户uid", reply_message=True)
    else:
        # 处理
        await _remove_uid_watch(bot, event, uid)
        await del_watch.finish()

@del_watch.got("uid")
async def _(bot: Bot, event: GroupMessageEvent, uid: str = ArgStr("uid")):
    uid = str(uid).replace(" ", "")
    if uid == "" or not uid.isdigit():
        await del_watch.finish("非法uid", reply_message=True)
    else:
        # 处理
        await _remove_uid_watch(bot, event, uid)
        await del_watch.finish()


show_watch = on_command("show_favw", aliases={"查看视奸列表"})
@show_watch.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 构建一个uid list
    uids = []
    for user_id in WATCH_USER_DATA.keys():
        uids.append(user_id)
    group_uids = []
    group_id = event.group_id
    # 遍历uids
    for uid in uids:
        if group_id in WATCH_USER_DATA[uid]:
            group_uids.append(uid)
    _message = "本群监听列表："
    # 获取用户名
    for uid in group_uids:
        user_name = await get_bili_user_name(int(uid))
        _message += f"\n{user_name} ({uid})"
    await bot.send(event=event, message=_message, reply_message=True)
