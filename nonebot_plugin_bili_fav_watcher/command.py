from typing import Union

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.internal.params import ArgStr
from nonebot.params import CommandArg

from .config import BILI_FAV_WATCHER_PRIORITY
from .local import is_admin, WATCH_USER_DATA, save_plugin_data, is_superuser, ADMIN_USERS, ADMIN_ONLY, set_admin_only
from .util import get_bili_user_name, get_group_message_first_at


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
        # 判断group_id是否已经存在
        if event.group_id in WATCH_USER_DATA[uid]:
            await bot.send(event=event, message=f"B站用户 `{user_name}` 已在监听列表中", reply_message=True)
            return
        WATCH_USER_DATA[uid].append(event.group_id)
    else:
        WATCH_USER_DATA[uid] = [event.group_id]
    # 保存
    save_plugin_data()
    await bot.send(event=event, message=f"B站用户 `{user_name}` 已添加至监听列表", reply_message=True)


add_watch = on_command("favw", aliases={"视奸"}, priority=BILI_FAV_WATCHER_PRIORITY)
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
            save_plugin_data()
            await bot.send(event=event, message="uid删除成功", reply_message=True)
        else:
            await bot.send(event=event, message="uid不在列表中", reply_message=True)
    else:
        await bot.send(event=event, message="uid不在列表中", reply_message=True)


del_watch = on_command("off_favw", aliases={"取消视奸"}, priority=BILI_FAV_WATCHER_PRIORITY)
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


show_watch = on_command("show_favw", aliases={"查看视奸列表"}, priority=BILI_FAV_WATCHER_PRIORITY)
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


async def _add_admin(bot: Bot, event: GroupMessageEvent, user_id: Union[int, str]):
    int_user_id = int(user_id)
    if int_user_id in ADMIN_USERS:
        await bot.send(event=event, message="该用户已拥有此插件使用权限", reply_message=True)
        return
    ADMIN_USERS.append(int_user_id)
    save_plugin_data()
    await bot.send(event=event, message="权限添加成功", reply_message=True)


add_favw_admin = on_command("add_favw_admin", priority=BILI_FAV_WATCHER_PRIORITY)
@add_favw_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not is_superuser(event.user_id):
        await add_favw_admin.finish("权限不足")
        return

    # 拿at
    at_id = await get_group_message_first_at(event)
    if at_id != -1:
        await _add_admin(bot, event, at_id)
        await add_favw_admin.finish()
        return

    # 拿参数
    add_id = str(arg).replace(" ", "")
    if add_id.isdigit():
        # 处理
        await _add_admin(bot, event, add_id)
        await add_favw_admin.finish()
    else:
        await bot.send(event=event, message="请输入用户id", reply_message=True)


@add_favw_admin.got("add_id")
async def _(bot: Bot, event: GroupMessageEvent, add_id: str = ArgStr("add_id")):
    # 拿at
    at_id = await get_group_message_first_at(event)
    if at_id != -1:
        await _add_admin(bot, event, at_id)
        await add_favw_admin.finish()
        return

    if not add_id.isdigit():
        await add_favw_admin.finish("非法id", reply_message=True)
    else:
        # 处理
        await _add_admin(bot, event, add_id)
        await add_favw_admin.finish()


async def _del_admin(bot: Bot, event: GroupMessageEvent, user_id: Union[int, str]):
    int_user_id = int(user_id)
    if int_user_id not in ADMIN_USERS:
        await bot.send(event=event, message="该用户没有此插件使用权限", reply_message=True)
        return
    ADMIN_USERS.remove(int_user_id)
    save_plugin_data()
    await bot.send(event=event, message="权限删除成功", reply_message=True)


del_fav_admin = on_command("del_favw_admin", priority=BILI_FAV_WATCHER_PRIORITY)
@del_fav_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not is_superuser(event.user_id):
        await del_fav_admin.finish("权限不足")
        return

    # 拿at
    at_id = await get_group_message_first_at(event)
    if at_id != -1:
        await _del_admin(bot, event, at_id)
        await del_fav_admin.finish()
        return

    # 拿参数
    del_id = str(arg).replace(" ", "")
    if del_id.isdigit():
        # 处理
        await _del_admin(bot, event, del_id)
        await del_fav_admin.finish()
    else:
        await bot.send(event=event, message="请输入用户id", reply_message=True)


@del_fav_admin.got("del_id")
async def _(bot: Bot, event: GroupMessageEvent, del_id: str = ArgStr("del_id")):
    # 拿at
    at_id = await get_group_message_first_at(event)
    if at_id != -1:
        await _del_admin(bot, event, at_id)
        await del_fav_admin.finish()
        return

    if not del_id.isdigit():
        await del_fav_admin.finish("非法id", reply_message=True)
    else:
        # 处理
        await _del_admin(bot, event, del_id)
        await del_fav_admin.finish()


show_favw_admin = on_command("show_favw_admin", priority=BILI_FAV_WATCHER_PRIORITY)
@show_favw_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if ADMIN_ONLY:
        await show_favw_admin.finish("当前该插件为仅管理员可用")
        await bot.send(event=event, message=f"当前拥有插件使用权限的用户列表：\n {ADMIN_USERS} \n(不展示SUPERUSERS)")
    else:
        await show_favw_admin.finish("当前该插件为所有群员可用")


favw_admin_only_on = on_command("favw_admin_only_on", priority=BILI_FAV_WATCHER_PRIORITY)
@favw_admin_only_on.handle()
async def _(event: GroupMessageEvent):
    if not is_superuser(event.user_id):
        await favw_admin_only_on.finish("权限不足")
        return
    set_admin_only(True)
    save_plugin_data()
    await favw_admin_only_on.finish("该插件已设置为仅管理员可用")


favw_admin_only_off = on_command("favw_admin_only_off", priority=BILI_FAV_WATCHER_PRIORITY)
@favw_admin_only_off.handle()
async def _(event: GroupMessageEvent):
    if not is_superuser(event.user_id):
        await favw_admin_only_off.finish("权限不足")
        return
    set_admin_only(False)
    save_plugin_data()
    await favw_admin_only_off.finish("该插件已设置为所有群员可用")
