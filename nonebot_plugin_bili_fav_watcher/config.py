import json
from pathlib import Path
from typing import Dict, List

from nonebot import logger, get_driver

CONFIG_PATH = Path("data/fav_watcher")
CONFIG_FILE_PATH = CONFIG_PATH / "config.json"

INTERVAL_BETWEEN_RUNS = 60 * 1  # 遍历间隔
NEW_VIDEO_THRESHOLD = 60 * 2  # 判定阈值
CACHE_CLEANUP_THRESHOLD = 60 * 3  # 清理阈值
SLEEP_INTERVAL = 5  # 等待时间


USER_FAV_MEDIA_CACHE: Dict[str, Dict[str, int]] = {

}

WATCH_USER_DATA: Dict[str, List] = {

}

ADMIN_USERS: List[int] = []

ADMIN_ONLY = False

if not CONFIG_PATH.exists():
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)

if CONFIG_FILE_PATH.exists():
    with open(CONFIG_FILE_PATH, "r") as f:
        data = f.read()
        if data:
            data = json.loads(data)
            USER_FAV_MEDIA_CACHE = data.get("cache", {})
            WATCH_USER_DATA = data.get("data", {})
            ADMIN_USERS = data.get("admin", [])
            ADMIN_ONLY = data.get("admin_only", False)

            logger.success(f"加载了 {len(ADMIN_USERS)} 个管理员；{str(ADMIN_USERS)}")
else:
    with open(CONFIG_FILE_PATH, "w") as f:
        f.write('{"cache": {}, "data": {}, "admin": [], "admin_only": false}')


def save_config():
    with open(CONFIG_FILE_PATH, "w") as _f:
        _f.write(json.dumps({
            "cache": USER_FAV_MEDIA_CACHE,
            "data": WATCH_USER_DATA,
            "admin": ADMIN_USERS
        }))


def is_admin(user_id: int) -> bool:
    if ADMIN_ONLY:
        return user_id in ADMIN_USERS
    return True


driver = get_driver()


@driver.on_shutdown
async def _():
    save_config()
