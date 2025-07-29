from bilibili_api import Credential
from bilibili_api.user import User
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from nonebot_plugin_bili_fav_watcher.config import SESSDATA, BUVID3, BILI_JCT, AC_TIME_VALUE, DEDEUSERID

CREDENTIAL = Credential(
    sessdata=SESSDATA,
    bili_jct=BILI_JCT,
    buvid3=BUVID3,
    ac_time_value=AC_TIME_VALUE,
    dedeuserid=DEDEUSERID
)

async def get_credential():
    check_refresh = await CREDENTIAL.check_refresh()
    if check_refresh:
        await CREDENTIAL.refresh()
    return CREDENTIAL

async def get_bili_user_name(uid: int) -> str:
    userEntity: User = User(uid, CREDENTIAL)
    user_info = await userEntity.get_user_info()
    return user_info.get('name')


async def get_group_message_first_at(event: GroupMessageEvent) -> int:
    first_at = -1
    try:
        at_list = event.message.get("at", None)
        if at_list:
            first_at = int(at_list[0].data['qq'])
    finally:
        return first_at
