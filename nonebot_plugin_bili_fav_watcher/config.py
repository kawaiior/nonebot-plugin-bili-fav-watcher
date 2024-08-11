from nonebot import get_driver, get_plugin_config, logger

from pydantic import BaseModel


driver = get_driver()

config = driver.config


# BILI_FAV_WATCHER__COMMAND_PRIORITY
# BILI_FAV_WATCHER__INTERVAL_BETWEEN_RUNS
# BILI_FAV_WATCHER__NEW_VIDEO_THRESHOLD
# BILI_FAV_WATCHER__CACHE_CLEANUP_THRESHOLD
# BILI_FAV_WATCHER__SLEEP_INTERVAL


class ScopedConfig(BaseModel):
    command_priority: int = 50
    interval_between_runs: int = 60
    new_video_threshold: int = 120
    cache_cleanup_threshold: int = 180
    sleep_interval: int = 5


class Config(BaseModel):
    bili_fav_watcher: ScopedConfig


plugin_config = get_plugin_config(Config)


BILI_FAV_WATCHER_PRIORITY: int = plugin_config.bili_fav_watcher.command_priority
INTERVAL_BETWEEN_RUNS: int = plugin_config.bili_fav_watcher.interval_between_runs  # 遍历间隔
NEW_VIDEO_THRESHOLD: int = plugin_config.bili_fav_watcher.new_video_threshold  # 判定阈值
CACHE_CLEANUP_THRESHOLD: int = plugin_config.bili_fav_watcher.cache_cleanup_threshold  # 清理阈值
SLEEP_INTERVAL: int = plugin_config.bili_fav_watcher.sleep_interval  # 等待时间
