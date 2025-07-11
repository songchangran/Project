import pkgutil
from .base import BaseCrawler
import inspect
import pkgutil
import importlib

# load classes subclass of BaseCrawler
classes = ['Daili66Crawler']
# https://blog.csdn.net/qq_43280079/article/details/104314227
# 遍历当前包的子模块，并使用正确的前缀
# for module_info in pkgutil.walk_packages(__path__, prefix=f"{__name__}."):
#     module = importlib.import_module(module_info.name)
# #
# # for loader, name, is_pkg in pkgutil.walk_packages(__path__):
# #     module = loader.find_module(name).load_module(name)
#     # print(111111111111111,module)
#     for name, value in inspect.getmembers(module):
#         # print(2222222,name,value)
#         globals()[name] = value
#         if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler \
#                 and not getattr(value, 'ignore', False):
#             classes.append(value)
__all__ = __ALL__ = classes

