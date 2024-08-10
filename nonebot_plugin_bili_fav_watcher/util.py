from bilibili_api import Credential
from bilibili_api.user import User


CREDENTIAL = Credential(
    sessdata=""
)

async def get_bili_user_name(uid: int) -> str:
    userEntity: User = User(uid, CREDENTIAL)
    user_info = await userEntity.get_user_info()
    return user_info.get('name')
