# tests/test_tree.py

import pytest
import pyavl  # 导入你的库

# --- Fixtures (测试固件) ---
# Fixture 是可复用的、为测试准备“环境”的函数。

@pytest.fixture
def empty_tree():
    """提供一个空的、会自动清理的 AVLTree 实例。"""
    with pyavl.AVLTree() as tree:
        yield tree

@pytest.fixture
def populated_tree():
    """提供一个包含一些数据的、会自动清理的 AVLTree 实例。"""
    keys = [50, 25, 75, 10, 30, 60, 80]
    with pyavl.AVLTree(keys) as tree:
        yield tree

# --- 测试用例 ---

def test_init_empty(empty_tree):
    """测试默认构造函数创建的是一棵空树。"""
    assert not (10 in empty_tree)

def test_init_with_iterable():
    """测试用一个列表来初始化树。"""
    keys = [10, 20, 5, 15]
    with pyavl.AVLTree(keys) as tree:
        for k in keys:
            assert k in tree
        assert 99 not in tree

def test_repr_and_str(populated_tree):
    """测试 __repr__ 和 __str__ 的基本行为。"""
    # __repr__ 应该包含类名和内存地址
    representation = repr(populated_tree)
    assert "AVLTree at" in representation
    assert "closed" not in representation

    # __str__ 应该返回一个非空的字符串 (因为树不为空)
    string_form = str(populated_tree)
    assert isinstance(string_form, str)
    assert len(string_form) > 0

def test_operations_on_closed_tree():
    """测试在一个已关闭的树上执行操作会抛出 ValueError。"""
    tree = pyavl.AVLTree([10])
    tree.close()

    # 验证 __repr__ 的显示
    assert "closed" in repr(tree)

    # 验证所有需要检查状态的方法
    with pytest.raises(ValueError, match="instance has been closed"):
        tree.insert(20)
    with pytest.raises(ValueError, match="instance has been closed"):
        tree.delete(10)
    with pytest.raises(ValueError, match="instance has been closed"):
        _ = 10 in tree # `in` 调用了 search
    with pytest.raises(ValueError, match="instance has been closed"):
        str(tree)

def test_context_manager_protocol():
    """测试 with 语句是否能正常工作并自动关闭树。"""
    # 创建一个实例，但不立即进入 with 块
    tree = pyavl.AVLTree()
    
    with tree:
        tree.insert(100)
        assert 100 in tree
    
    # 离开 with 块后，树应该已经被自动关闭了
    with pytest.raises(ValueError, match="instance has been closed"):
        tree.search(100)

def test_in_order_traverse(populated_tree):
    """测试中序遍历返回的键值是正确有序的。"""
    collected_keys = []
    
    def callback(key, height, bf):
        collected_keys.append(key)
        
    populated_tree.in_order_traverse(callback)
    
    # 对于二叉搜索树，中序遍历的结果一定是排序好的
    assert collected_keys == [10, 25, 30, 50, 60, 75, 80]

def test_split(populated_tree):
    """测试分裂功能。"""
    # 原始树的键: [10, 25, 30, 50, 60, 75, 80]
    small, large = populated_tree.split(40)

    # 1. 检查原始树是否已被消耗
    with pytest.raises(ValueError):
        _ = 10 in populated_tree

    # 2. 检查小树的内容
    with small:
        assert (10 in small) and (25 in small) and (30 in small)
        assert not (50 in small)

    # 3. 检查大树的内容
    with large:
        assert (50 in large) and (60 in large) and (75 in large) and (80 in large)
        assert not (10 in large)

def test_merge():
    """测试合并功能。"""
    t1 = pyavl.AVLTree([1, 2, 3])
    t2 = pyavl.AVLTree([10, 20, 30])

    # 使用类方法进行合并
    merged = pyavl.AVLTree.merge(t1, t2)

    # 1. 检查原始树是否已被消耗
    with pytest.raises(ValueError):
        _ = 1 in t1
    with pytest.raises(ValueError):
        _ = 10 in t2

    # 2. 检查合并后的树
    with merged:
        for k in [1, 2, 3, 10, 20, 30]:
            assert k in merged
        assert 99 not in merged