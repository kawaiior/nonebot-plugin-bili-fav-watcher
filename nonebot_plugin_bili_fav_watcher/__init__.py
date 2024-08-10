from nonebot.plugin import PluginMetadata

usage = """使用方式:
<favw> [uid]: 添加B站用户。
<off_favw> [uid]: 移除指定B站用户。
<show_favw>: 查看监听列表。
<favw_now>: 立即执行一次监视。
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
        'version': '0.1.3'
    },
    homepage="https://github.com/kawaiior/nonebot-plugin-bili-fav-watcher"
)

from .core import *
from .command import *
