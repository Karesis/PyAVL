# tests/test_tree.py
import pyavl
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def empty_tree():
    """这是一个 fixture，它会创建一个空的 Tree 对象，并在测试结束后自动清理。"""
    with pyavl.AVLTree() as t:
        yield t

@pytest.fixture
def populated_tree():
    """一个包含一些数据的 fixture，方便测试。"""
    with pyavl.AVLTree() as t:
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            t.insert(key)
        yield t

# --- 你的已有测试 (保持不变) ---
def test_initial_state(empty_tree):
    assert not (10 in empty_tree)

def test_single_insertion_and_search(empty_tree):
    empty_tree.insert(20)
    assert 20 in empty_tree
    assert not (10 in empty_tree)

def test_delete(populated_tree):
    assert 10 in populated_tree
    populated_tree.delete(10)
    assert not (10 in populated_tree)
    assert 20 in populated_tree
    assert 5 in populated_tree

@pytest.mark.parametrize("key_to_test", [0, -999, 123456789])
def test_various_keys(empty_tree, key_to_test):
    empty_tree.insert(key_to_test)
    assert key_to_test in empty_tree
    empty_tree.delete(key_to_test)
    assert not (key_to_test in empty_tree)


# --- 新增测试用例 ---

# 1. 测试错误和边界条件 (提高 insert/delete/search 覆盖率)
@pytest.mark.parametrize("method_name, args", [
    ("insert", (1.0,)),      # 浮点数
    ("delete", ("a",)),      # 字符串
    ("search", (None,)),     # None
    ("__contains__", ([],))  # 列表
])
def test_type_errors(empty_tree, method_name, args):
    """测试当传入非整数键时，方法是否正确抛出 TypeError。"""
    with pytest.raises(TypeError, match="Key must be an integer"):
        # 使用 getattr 动态调用方法
        if method_name == "__contains__":
             _ = args[0] in empty_tree
        else:
            method = getattr(empty_tree, method_name)
            method(*args)

def test_insert_memory_error(empty_tree):
    """(高级) 使用 mock 模拟 C 库返回 NULL，测试 MemoryError。"""
    empty_tree.insert(10) # 先插入一个节点，确保 self._ptr 不为 NULL

    # 将 'pyavl._myclib.lib' 整个替换为一个 MagicMock 对象
    with patch('pyavl._myclib.lib', new_callable=MagicMock) as mock_lib:
        # 配置这个 mock_lib，让它的 avl_insert 方法返回 ffi.NULL
        mock_lib.avl_insert.return_value = pyavl._myclib.ffi.NULL
        
        with pytest.raises(MemoryError, match="Failed to insert node"):
            empty_tree.insert(20)

# 2. 测试 0% 覆盖的函数
def test_in_order_traverse(populated_tree):
    """测试中序遍历功能。"""
    result = []
    def callback(key, height, balance):
        # 简单地把 key 添加到列表中
        result.append(key)

    populated_tree.in_order_traverse(callback)
    
    # 中序遍历的结果应该是排序好的
    assert result == [5, 10, 15, 20, 25, 30, 35]

def test_in_order_traverse_type_error(empty_tree):
    """测试当中序遍历的回调不是函数时，抛出 TypeError。"""
    with pytest.raises(TypeError, match="callback must be a callable function"):
        empty_tree.in_order_traverse("not a function")

def test_split(populated_tree):
    """测试 split 功能。"""
    original_keys = [5, 10, 15, 20, 25, 30, 35]
    
    # 按 20 分裂
    small_tree, large_tree = populated_tree.split(20)

    # 验证返回的是两个 Tree 对象
    assert isinstance(small_tree, pyavl.AVLTree)
    assert isinstance(large_tree, pyavl.AVLTree)

    # 验证分裂后的树的内容
    assert all(k in small_tree for k in [5, 10, 15, 20]) 
    assert all(k in large_tree for k in [25, 30, 35])
    assert not any(k in large_tree for k in [5, 10, 15, 20]) 
    
    # 验证原始树被消耗 (现在应该是空的)
    assert all(not (k in populated_tree) for k in original_keys)

    # 清理新创建的树
    small_tree.close()
    large_tree.close()

def test_merge():
    """测试 merge 功能。"""
    with pyavl.AVLTree() as tree1, pyavl.AVLTree() as tree2:
        for k in [10, 20]:
            tree1.insert(k)
        for k in [30, 40]:
            tree2.insert(k)
            
        merged_tree = pyavl.AVLTree.merge(tree1, tree2)
    
        # 验证合并后的内容
        assert all(k in merged_tree for k in [10, 20, 30, 40])
        
        # 验证原始树被消耗
        assert not (10 in tree1)
        assert not (30 in tree2)

        merged_tree.close()

def test_merge_type_error():
    """测试当 merge 的参数类型不正确时抛出 TypeError。"""
    with pyavl.AVLTree() as tree1:
        with pytest.raises(TypeError, match="Inputs must be Tree objects"):
            pyavl.AVLTree.merge(tree1, "not a tree")

def test_display(populated_tree, capsys):
    """测试 display 方法是否能被调用且不崩溃。"""
    try:
        populated_tree.display()
    except Exception as e:
        pytest.fail(f"display() method raised an unexpected exception: {e}")