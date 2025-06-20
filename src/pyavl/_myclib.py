# src/pyavl/_myclib.py

# 导入我们编译好的底层C模块中的 lib 和 ffi 对象
from ._pyavl_c import lib, ffi

class AVLTree:
    """
    一个面向对象的AVL树Python封装器。
    它负责管理指向C语言AVLTree结构体的指针，并提供一套
    安全、易用的Pythonic接口。
    """

    def __init__(self):
        """创建一个新的、空的AVL树。"""
        # self._ptr 持有指向底层C结构体的指针。
        # lib.avl_create() 返回一个 AVLTree 指针 (在cdef里是 void*)
        self._ptr = lib.avl_create()
        if self._ptr == ffi.NULL:
            # 可以在这里做一些错误处理，如果创建失败的话
            pass

    def insert(self, key: int):
        """向树中插入一个键值。"""
        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")
        
        # !! 这是整个封装中最关键的细节之一 !!
        # C语言的插入/删除函数可能会改变树的根节点，因此它返回
        # 一个新的根节点指针。我们必须用这个新指针来更新我们持有的旧指针。
        new_ptr = lib.avl_insert(self._ptr, key)
        if new_ptr == ffi.NULL and self._ptr != ffi.NULL:
             # 可以根据你的C库设计，判断插入失败的情况
             raise MemoryError("Failed to insert node in C library.")
        self._ptr = new_ptr

    def delete(self, key: int):
        """从树中删除一个键值。"""
        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")
        
        # 同样，必须更新指针
        self._ptr = lib.avl_delete(self._ptr, key)

    def search(self, key: int) -> bool:
        """查找一个键值是否存在于树中。"""
        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")
        
        # 将C的 1/0 返回值优雅地转换为Python的 True/False
        return bool(lib.avl_search(self._ptr, key))
    
    def in_order_traverse(self, callback):
        """
        以中序遍历的方式访问树中的每一个节点，并对每个节点调用
        一个用户提供的 Python 回调函数。

        :param callback: 一个接受三个整数参数 (key, height, balance_factor)
                         的 Python 函数。
        """
        if not callable(callback):
            raise TypeError("callback must be a callable function.")

        c_callback = ffi.callback("void(int, int, int)", callback)
        # CFFI 会自动创建一个 trampoline，让C代码可以安全地调用 Python 函数
        lib.avl_in_order_traverse(self._ptr, c_callback)

    def split(self, key: int):
        """
        将当前的树按给定的 key 分裂成两棵新树。
        注意：此操作会消耗原始树。

        分裂规则：
        - 小树 (small_tree) 包含所有小于或等于 `key` 的元素。
        - 大树 (large_tree) 包含所有大于 `key` 的元素。
        
        :param key: 分裂的基准值。
        :return: 一个元组，包含两棵新的 Tree 对象 (small_tree, large_tree)。
        """
        # 1. 创建两个“指针的指针”，作为出参传递给C函数
        # ffi.new("AVLTree *") 会分配一块内存，用于存放一个 AVLTree 指针
        small_ptr_p = ffi.new("AVLTree *")
        large_ptr_p = ffi.new("AVLTree *")

        # 2. 调用C函数，它会把新树的地址填入我们准备好的内存中
        lib.avl_split(self._ptr, key, small_ptr_p, large_ptr_p)

        # 3. 从指针的指针中取出新树的指针
        small_tree_ptr = small_ptr_p[0]
        large_tree_ptr = large_ptr_p[0]

        # 4. 因为原始树被消耗了，所以将当前对象的指针设为NULL，防止被重复释放
        self._ptr = ffi.NULL

        # 5. 用新指针创建两个新的Python Tree对象并返回
        small_tree = AVLTree._from_ptr(small_tree_ptr)
        large_tree = AVLTree._from_ptr(large_tree_ptr)
        
        return small_tree, large_tree
    
    @classmethod
    def merge(cls, tree1, tree2):
        """
        合并两棵AVL树，返回一棵全新的树。
        前提: tree1 中所有键值必须小于 tree2 中所有键值。
        注意：此操作会消耗输入的两棵树。

        :param tree1: 较小的树。
        :param tree2: 较大的树。
        :return: 一个全新的、合并后的 Tree 对象。
        """
        if not isinstance(tree1, cls) or not isinstance(tree2, cls):
            raise TypeError("Inputs must be Tree objects.")

        # 1. 调用C函数，传入两个树的底层指针
        merged_ptr = lib.avl_merge(tree1._ptr, tree2._ptr)
        
        # 2. 因为原始树被消耗，将它们的指针设为NULL
        tree1._ptr = ffi.NULL
        tree2._ptr = ffi.NULL

        # 3. 使用辅助方法从返回的指针创建新实例
        return cls._from_ptr(merged_ptr)

    def display(self):
        """打印树的结构，这是一个直接的调用。"""
        lib.avl_display(self._ptr)
        
    def close(self):
        """
        提供一个显式的方法来释放C语言层面的内存。
        这是非常好的实践，因为用户可以精确控制资源释放的时机。
        """
        # 检查指针是否已经被释放，防止重复释放导致程序崩溃
        if self._ptr != ffi.NULL:
            lib.avl_destroy(self._ptr)
            # 释放后，将指针设置为NULL，这是一个安全的好习惯
            self._ptr = ffi.NULL
    
    @classmethod
    def _from_ptr(cls, ptr):
        """一个私有的辅助方法，用于从一个已存在的指针创建Tree对象"""
        new_tree = cls.__new__(cls) # 创建一个空实例，不调用 __init__
        new_tree._ptr = ptr
        return new_tree

    def __del__(self):
        """
        当Tree对象被Python垃圾回收器回收时，尝试自动释放C内存。
        这是一种保障机制，但不能完全依赖它，因为__del__的调用时机
        有时不确定。最好的方式还是使用 with 语句或手动调用 .close()。
        """
        self.close()

    def __enter__(self):
        """实现上下文管理器协议，让 with 语句能够工作。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """在退出 with 代码块时，自动调用 close() 方法，确保资源被释放。"""
        self.close()
        
    def __contains__(self, key: int) -> bool:
        """
        实现这个魔术方法，可以让 'in' 关键字工作。
        例如: if 10 in my_tree:
        这才是真正的 Pythonic！
        """
        return self.search(key)