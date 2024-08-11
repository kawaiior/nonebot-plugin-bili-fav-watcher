from nonebot import logger, get_driver, require, get_plugin_config
import json
from typing import Dict, List

from pydantic import BaseModel

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

driver = get_driver()

config = driver.config

class ScopedConfig(BaseModel):
    command_priority: int = 50
    interval_between_runs: int = 60
    new_video_threshold: int = 120
    cache_cleanup_threshold: int = 180
    sleep_interval: int = 5


class Config(BaseModel):
    bili_fav_watcher: ScopedConfig


plugin_config = get_plugin_config(ScopedConfig)


BILI_FAV_WATCHER_PRIORITY: int = plugin_config.command_priority
INTERVAL_BETWEEN_RUNS: int = plugin_config.interval_between_runs  # 遍历间隔
NEW_VIDEO_THRESHOLD: int = plugin_config.new_video_threshold  # 判定阈值
CACHE_CLEANUP_THRESHOLD: int = plugin_config.cache_cleanup_threshold  # 清理阈值
SLEEP_INTERVAL: int = plugin_config.sleep_interval  # 等待时间

"""
以下为数据存储
"""

DATA_PATH = store.get_data_dir("fav_watcher")
DATA_FILE_PATH = store.get_data_file("fav_watcher", "data.json")


USER_FAV_MEDIA_CACHE: Dict[str, Dict[str, int]] = {}
WATCH_USER_DATA: Dict[str, List] = {}
ADMIN_USERS: List[int] = []
ADMIN_ONLY: bool = False

SUPERUSERS: set[str] = config.superusers

if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True, exist_ok=True)

# 加载
if DATA_FILE_PATH.exists():
    with open(DATA_FILE_PATH, "r") as f:
        data = f.read()
        if data:
            data = json.loads(data)
            USER_FAV_MEDIA_CACHE = data.get("cache", {})
            WATCH_USER_DATA = data.get("data", {})
            ADMIN_USERS = data.get("admin", [])
            ADMIN_ONLY = data.get("admin_only", False)

            logger.success(f"加载了 {len(ADMIN_USERS)} 个管理员 {str(ADMIN_USERS)}")
else:
    with open(DATA_FILE_PATH, "w") as f:
        f.write(json.dumps({
            "cache": {},
            "data": {},
            "admin": [],
            "admin_only": False
        }))


def save_plugin_data():
    with open(DATA_FILE_PATH, "w") as _f:
        _f.write(json.dumps({
            "cache": USER_FAV_MEDIA_CACHE,
            "data": WATCH_USER_DATA,
            "admin": ADMIN_USERS,
            "admin_only": ADMIN_ONLY
        }))


def is_superuser(user_id: int) -> bool:
    return str(user_id) in SUPERUSERS


def is_admin(user_id: int) -> bool:
    if ADMIN_ONLY:
        return is_superuser(user_id) or user_id in ADMIN_USERS
    return True


def set_admin_only(admin_only: bool):
    global ADMIN_ONLY
    ADMIN_ONLY = admin_only


@driver.on_shutdown
async def _():
    save_plugin_data()
