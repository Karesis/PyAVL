# src/pyavl/_myclib.py (完整修正版)
import os
import sys
import tempfile
from typing import Callable

# 导入我们编译好的底层C模块中的 lib 和 ffi 对象
from ._pyavl_c import lib, ffi

class AVLTree:
    """
    一个面向对象的AVL树Python封装器。
    它负责管理指向C语言AVLTree结构体的指针
    """

    def __init__(self, keys=None):
        """
        创建一个新的、空的AVLTree实例。
        :param keys: 一个可选的可迭代对象 (如 list, tuple)，其元素将被插入到树中。
        """
        self._ptr = lib.avl_create()
        # 关键修改 1: 初始化时，明确设置 _closed 状态为 False
        self._closed = False
        
        if keys is not None:
            for key in keys:
                self.insert(key)
    
    @property
    def count(self) -> int:
        """返回树中的节点总数。"""
        self._check_closed()
        return lib.avl_get_count(self._ptr)

    @property
    def height(self) -> int:
        """返回树的高度。"""
        self._check_closed()
        return lib.avl_get_height(self._ptr)
    
    def _check_closed(self):
        """一个内部辅助方法，用于检查树是否已被明确关闭。"""
        # 关键修改 2: 现在我们只检查 _closed 标志，而不是 _ptr
        if self._closed:
            raise ValueError("Cannot perform operation: This AVLTree instance has been closed.")

    def insert(self, key: int):
        """向树中插入一个键值。"""
        self._check_closed() # 这个检查现在是正确的
        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")
        
        new_ptr = lib.avl_insert(self._ptr, key)
        # 这个错误检查可以保留，用于捕捉C层真正的内存分配失败
        if new_ptr == ffi.NULL and self._ptr != ffi.NULL:
            raise MemoryError("Failed to insert node in C library.")
        self._ptr = new_ptr

    def delete(self, key: int):
        """从树中删除一个键值。"""
        self._check_closed()
        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")
        self._ptr = lib.avl_delete(self._ptr, key)

    def search(self, key: int) -> bool:
        """查找一个键值是否存在于树中。"""
        self._check_closed()
        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")
        return bool(lib.avl_search(self._ptr, key))
    
    def in_order_traverse(self, callback: Callable[[int, int, int], None]):
        """以中序遍历的方式访问每一个节点。"""
        self._check_closed()
        if not callable(callback):
            raise TypeError("callback must be a callable function.")
        # 显式创建回调对象是好习惯
        c_callback = ffi.callback("void(int, int, int)", callback)
        lib.avl_in_order_traverse(self._ptr, c_callback)

    def split(self, key: int):
        """将当前的树按给定的 key 分裂成两棵新树。"""
        self._check_closed()
        small_ptr_p = ffi.new("AVLTree *")
        large_ptr_p = ffi.new("AVLTree *")
        lib.avl_split(self._ptr, key, small_ptr_p, large_ptr_p)
        
        small_tree = AVLTree._from_ptr(small_ptr_p[0])
        large_tree = AVLTree._from_ptr(large_ptr_p[0])
        
        self._ptr = ffi.NULL
        self._closed = True
        
        return small_tree, large_tree
    
    @classmethod
    def merge(cls, tree1, tree2):
        """合并两棵AVL树，返回一棵全新的树。"""
        if not isinstance(tree1, cls) or not isinstance(tree2, cls):
            raise TypeError("Inputs must be AVLTree objects.")
        
        tree1._check_closed()
        tree2._check_closed()
        
        merged_ptr = lib.avl_merge(tree1._ptr, tree2._ptr)
        
        tree1._ptr = ffi.NULL
        tree1._closed = True
        tree2._ptr = ffi.NULL
        tree2._closed = True

        return cls._from_ptr(merged_ptr)
            
    def close(self):
        """显式地释放C语言层面的内存，并标记对象为已关闭。"""
        # 关键修改 5: 检查 _closed 状态，防止重复进入
        if not self._closed:
            lib.avl_destroy(self._ptr)
            self._ptr = ffi.NULL
            self._closed = True # 明确标记为已关闭
    
    @classmethod
    def _from_ptr(cls, ptr):
        """一个私有的辅助方法，用于从一个已存在的指针创建Tree对象"""
        new_tree = cls.__new__(cls)
        new_tree._ptr = ptr
        new_tree._closed = False # 新创建的对象总是未关闭状态
        return new_tree
    
    def __del__(self):
        """析构函数，作为安全网，尝试关闭资源。"""
        self.close()

    def __enter__(self):
        """上下文管理器入口。"""
        self._check_closed()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，自动关闭资源。"""
        self.close()
        
    def __contains__(self, key: int) -> bool:
        """实现 'in' 关键字。"""
        return self.search(key)
    
    def __str__(self):
        self._check_closed()
        if self._ptr == ffi.NULL:
            return "<AVLTree (empty)>"

        buffer_size = 4096 
        c_buffer = ffi.new(f"char[{buffer_size}]")

        lib.avl_display_to_buffer(self._ptr, c_buffer, buffer_size)

        captured_string = ffi.string(c_buffer).decode('utf-8', errors='replace')

        return captured_string.strip()

    def __repr__(self):
        """返回对开发者友好的对象表示。"""
        # 关键修改 6: repr 的判断依据也改为 _closed 标志
        if self._closed:
            return f"<AVLTree at {hex(id(self))} (closed)>"
        else:
            return f"<AVLTree at {hex(id(self))}>"