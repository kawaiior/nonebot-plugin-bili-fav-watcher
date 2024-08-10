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

示例:

`favw 123456`

`off_favw 123456`

ps: 使用前请在命令前添加命令判定符，一般为`/`或`#`

## 配置

配置文件存储与项目根路径下的`data/fav_watcher`文件夹内，配置文件名为`config.json`。 第一次运行插件时，会自动创建。

修改`config.json`内的`admin_only`字段，可以设置是否仅管理员可使用该插件。默认情况下为`false`，即每个人都可以使用。

将`admin_only`字段设置为`true`后，只有管理员可以使用该插件。可以修改`admin`字段，添加管理员QQ号。管理员QQ号之间用英文逗号分隔。

示例：

```json
{
  "cache": {}, 
  "data": {}, 
  "admin": [123456, 234567], 
  "admin_only": true
}
```

ps: 若无必要，请勿修改`config.json`内的其他字段。
