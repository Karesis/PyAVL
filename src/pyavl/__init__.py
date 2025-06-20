# src/pyavl/__init__.py

# 从我们的内部封装模块中，只导入我们想让用户看到的 Tree 类
from ._myclib import AVLTree

# __all__ 是一个列表，定义了 "from pyavl import *" 时会导入哪些名字。
# 这也是一个最佳实践，明确了包的公共API。
__all__ = ['AVLTree']