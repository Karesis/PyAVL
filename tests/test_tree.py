# tests/test_tree.py (重构一下)
import pyavl
import pytest

@pytest.fixture
def empty_tree():
    """这是一个 fixture，它会创建一个空的 Tree 对象，并在测试结束后自动清理。"""
    with pyavl.AVLTree() as t:
        yield t # yield 关键字把 t 对象提供给测试函数使用

def test_initial_state(empty_tree): # 直接把 fixture 的名字作为参数传入
    """测试树的创建和初始状态"""
    assert not (10 in empty_tree)

def test_single_insertion_and_search(empty_tree):
    """测试单次插入和查找"""
    empty_tree.insert(20)
    assert 20 in empty_tree
    assert not (10 in empty_tree)

def test_delete(empty_tree):
    """测试删除功能"""
    keys = [10, 20, 5]
    for k in keys:
        empty_tree.insert(k)
    
    empty_tree.delete(10)
    assert not (10 in empty_tree)
    assert 20 in empty_tree
    assert 5 in empty_tree

@pytest.mark.parametrize("key_to_test", [
    0,
    -999,
    123456789
])
def test_various_keys(empty_tree, key_to_test):
    """测试不同的合法key值"""
    empty_tree.insert(key_to_test)
    assert key_to_test in empty_tree
    empty_tree.delete(key_to_test)
    assert not (key_to_test in empty_tree)