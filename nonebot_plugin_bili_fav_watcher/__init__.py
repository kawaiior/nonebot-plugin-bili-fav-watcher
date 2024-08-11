from nonebot.plugin import PluginMetadata

usage = """使用方式:
<favw> [uid]: 添加B站用户。
<off_favw> [uid]: 移除指定B站用户。
<show_favw>: 查看监听列表。
<favw_now>: 立即执行一次监视。
<add_favw_admin> [qq_id]: 给指定用户添加插件使用权限。
<del_favw_admin> [qq_id]: 删除指定用户的插件使用权限。
<show_favw_admin>: 查看插件使用权限列表。
<favw_admin_only_on>: 设置为仅管理员可用（仅SUPERUSERS可用）。
<favw_admin_only_off>: 设置为所有群员可用（仅SUPERUSERS可用）。
示例:
favw 123456
off_favw 123456"""

__plugin_meta__ = PluginMetadata(
    name="B站收藏夹监视器",
    description="监视指定B用户的收藏夹内容",
    usage=usage,
    supported_adapters={"~onebot.v11"},
    type="application",
    extra={
        'author': '鱼酱',
        'license': 'MIT',
        'version': '0.1.5'
    },
    homepage="https://github.com/kawaiior/nonebot-plugin-bili-fav-watcher"
)

from .core import *
from .command import *
