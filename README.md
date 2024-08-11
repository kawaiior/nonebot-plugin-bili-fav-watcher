# nonebot-plugin-bili-fav-watcher

<p>
  <a>
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

## 安装

```shell
nb plugin install nonebot-plugin-bili-fav-watcher
```

## 简介

这是一个用于监听B站收藏夹更新的NoneBot插件，可以自动发送收藏夹更新通知到QQ群。

## 使用
`<favw> [uid]`: 添加B站用户。

`<off_favw> [uid]`: 移除指定B站用户。

`<show_favw>`: 查看监听列表。

`<favw_now>`: 立即执行一次监视。

`<add_favw_admin> [qq_id]`: 给指定用户添加插件使用权限。

`<del_favw_admin> [qq_id]`: 删除指定用户的插件使用权限。

`<show_favw_admin>`: 查看插件使用权限列表。

`<favw_admin_only_on>`: 设置为仅管理员可用（仅SUPERUSERS可用）。

`<favw_admin_only_off>`: 设置为所有群员可用（仅SUPERUSERS可用）。

示例:

`favw 123456`

`off_favw 123456`

ps: 使用时请在命令前添加命令判定符，一般为`/`或`#`

## 配置

`BILI_FAV_WATCHER__COMMAND_PRIORITY` 插件命令权重

`BILI_FAV_WATCHER__INTERVAL_BETWEEN_RUNS` 收藏夹遍历间隔（单位：秒，默认值：60）

`BILI_FAV_WATCHER__NEW_VIDEO_THRESHOLD` 收藏夹新视频判定阈值（单位：秒，默认值：120）

`BILI_FAV_WATCHER__CACHE_CLEANUP_THRESHOLD` 缓存清理阈值（单位：秒，默认值：180）

`BILI_FAV_WATCHER__SLEEP_INTERVAL` 遍历过程中休眠间隔（单位：秒，默认值：5）
