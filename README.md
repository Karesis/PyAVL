# pyavl: 一个由 C 语言驱动的高性能 Python AVL 树库

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![PyPI version](https://img.shields.io/pypi/v/pyavl?color=blue)
![License](https://img.shields.io/badge/license-MIT-blue)

**`pyavl`** 是一个功能完备、性能卓越的平衡二叉树（AVL树）Python 库。它的核心数据结构与算法由纯 C 语言实现，确保了在进行大量插入、删除和查找操作时的高效率；同时，它通过精心设计的封装层，为 Python 用户提供了简洁、易用且符合语言习惯的面向对象接口。

这个项目诞生于一次数据结构课程的作业，并致力于在满足学术要求的基础上，探索真实世界中 Python 与 C 语言混合编程的最佳工程实践。

---

## 主要特性

* **性能卓越**: 核心逻辑由 C 语言编写，执行速度远超纯 Python 实现。
* **Pythonic 接口**: 提供优雅的 `AVLTree` 类，支持 `with` 语句进行自动资源管理，支持 `in` 关键字进行查找。
* **功能完备**: 实现了 AVL 树所有基本操作，包括插入、删除和查找。
* **高级操作**: 支持两棵树的**合并 (merge)**、将一棵树**分裂 (split)** 为两棵，以及通过**回调函数**进行自定义中序遍历，为数据导出和可视化提供了极大便利。
* **健壮可靠**: 配备了完整的测试套件（使用 `pytest`），并集成了自动化测试流程。
* **内存安全**: 精心处理了 C 语言层面的内存分配与释放，通过 Python 的垃圾回收机制和上下文管理器提供双重保障。

---

## 安装

未来项目发布到 PyPI 后，可以通过以下方式安装：
```bash
# 使用 uv
uv pip install pyavl

# 或使用 pip
pip install pyavl
```

目前，你可以直接从源代码进行安装：
```bash
# 1. 克隆仓库
git clone [https://github.com/your-username/pyavl.git](https://github.com/your-username/pyavl.git)
cd pyavl

# 2. (推荐) 创建并激活虚拟环境
uv venv
source .venv/bin/activate  # 在 Windows PowerShell 中是 .\.venv\Scripts\Activate.ps1

# 3. 以可编辑模式安装
uv pip install -e .
```

---

## 快速开始

只需几行代码，即可体验 `pyavl` 的魅力：

```python
import pyavl

# 使用 with 语句，确保使用完毕后C层内存会被自动释放
with pyavl.AVLTree() as tree:
    # 插入一些数据
    keys_to_insert = [20, 10, 30, 5, 15]
    for key in keys_to_insert:
        tree.insert(key)
    
    # 用 Pythonic 的方式检查成员
    if 15 in tree:
        print("键值 15 存在于树中！")
        
    if 99 not in tree:
        print("键值 99 不存在于树中。")

    # 打印树的文本表示
    print("\n当前树的结构：")
    tree.display()
```

---

## API 使用示例

### 基本操作

```python
import pyavl

tree = pyavl.AVLTree()

# 插入
tree.insert(50)
tree.insert(30)
tree.insert(70)

# 查找 (推荐使用 'in')
assert 50 in tree

# 删除
tree.delete(30)
assert not (30 in tree)

# 打印
tree.display()

# 操作结束后，主动释放资源是一个好习惯
tree.close()
```

### 高级功能

#### 自定义遍历

你可以传入一个 Python 函数，在遍历每个节点时执行自定义逻辑，非常适合数据导出和可视化。

```python
node_list = []
def collect_node_data(key, height, balance_factor):
    node_list.append({
        "key": key,
        "height": height,
        "bf": balance_factor
    })

with pyavl.AVLTree() as tree:
    tree.insert(10)
    tree.insert(20)
    tree.in_order_traverse(collect_node_data)

# node_list 现在是 [{'key': 10, ...}, {'key': 20, ...}]
print(node_list) 
```

#### 分裂 (Split)

将一棵树分裂为二，此操作会消耗原始树。

```python
# 创建一棵较大的树
original_tree = pyavl.AVLTree()
for k in [10, 20, 30, 40, 50]:
    original_tree.insert(k)

# 以 35 为界进行分裂
small_tree, large_tree = original_tree.split(35)

print("分裂后的小树:")
small_tree.display() # 包含 10, 20, 30

print("\n分裂后的大树:")
large_tree.display() # 包含 40, 50

# 别忘了处理新创建的树
small_tree.close()
large_tree.close()
```

#### 合并 (Merge)

将两棵树合并为一棵，这是一个类方法，会消耗原始的两棵树。

```python
# 前提: t1 的所有键 < t2 的所有键
t1 = pyavl.AVLTree(); t1.insert(1); t1.insert(5)
t2 = pyavl.AVLTree(); t2.insert(10); t2.insert(20)

#像调用工厂函数一样调用 merge
merged_tree = pyavl.AVLTree.merge(t1, t2)

print("合并后的新树:")
merged_tree.display()

merged_tree.close()
```

---

## 为开发者

欢迎为 `pyavl` 贡献代码！

#### 设置开发环境
```bash
# 创建虚拟环境
uv venv
# 激活
source .venv/bin/activate
# 安装所有依赖
uv pip install -e .
```

#### 运行测试
本项目使用 `pytest` 进行测试。
```bash
# 运行所有测试
pytest

# 运行测试并查看代码覆盖率报告
pytest --cov=pyavl
```

---

## 项目许可

本项目采用 [MIT 许可证](LICENSE)。

## 致谢

感谢这次宝贵的课程设计机会，也感谢在这个充满挑战的开发过程中获得的每一次指导和进步。从一个想法到一份健壮、好用的软件库，这段旅程本身就是最好的学习。