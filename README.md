# pyavl: 一个由 C 语言驱动的高性能 Python AVL 树库

[![CI/CD Status](https://github.com/Karesis/PyAVL/actions/workflows/ci.yml/badge.svg)](https://github.com/Karesis/PyAVL/actions/workflows/ci.yml)
[![Coverage Status](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![PyPI version](https://img.shields.io/pypi/v/pyavl?color=blue&label=pypi)](https://pypi.org/project/pyavl/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**`pyavl`** 是一个功能完备、性能卓越的平衡二叉树（AVL树）Python 库。它的核心数据结构与算法由纯 C 语言实现，确保了在进行大量插入、删除和查找操作时的高效率；同时，它通过精心设计的封装层，为 Python 用户提供了简洁、易用且符合语言习惯的面向对象接口。

这个项目诞生于一次数据结构课程的作业，并致力于在满足学术要求的基础上，探索真实世界中 Python 与 C 语言混合编程的最佳工程实践。

---

## 主要特性

* **性能卓越**: 核心逻辑由 C 语言编写，执行速度远超纯 Python 实现。
* **Pythonic 接口**: 提供优雅的 `AVLTree` 类，支持 `with` 语句进行自动资源管理，支持 `in` 关键字进行查找，并提供了 `print()` 的直观显示。
* **功能完备**: 实现了 AVL 树所有基本操作，包括插入、删除、查找和自定义中序遍历。
* **高级操作**: 支持两棵树的**合并 (merge)**、将一棵树**分裂 (split)** 为两棵，为复杂数据处理提供了强大工具。
* **强大的交互式CLI**: 自带一个功能丰富的命令行工具，支持多树管理、文件存取和实时可视化，是学习和调试的绝佳伴侣。
* **健壮可靠**: 配备了完整的测试套件（使用 `pytest`），代码覆盖率达到100%，并集成了跨平台（Windows, macOS, Linux）的自动化测试流程。
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
git clone [https://github.com/Karesis/PyAVL.git](https://github.com/Karesis/PyAVL.git)
cd PyAVL  # 注意大小写

# 2. (推荐) 创建并激活虚拟环境
uv venv
source .venv/bin/activate  # 在 Windows PowerShell 中是 .\.venv\Scripts\Activate.ps1

# 3. 以可编辑模式安装（这将编译C扩展）
uv pip install -e .
```

---

## 交互式演示 (CLI)

`pyavl` 不仅仅是一个库，更是一个开箱即用的学习工具。我们提供了一个强大的交互式命令行界面（CLI），让你能够直观地探索AVL树的各种操作。

**启动方式：**
在项目根目录下运行：
```bash
python run.py
```

你将看到一个友好的交互式环境：
```
🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
      欢迎使用交互式 AVL 树演示程序
🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
输入 'help' 或 'h' 查看所有可用命令。
(main) > i 50 30 70 20 40 80
成功插入: [50, 30, 70, 20, 40, 80]
└── 50
    ├── 70
    │   └── 80
    └── 30
        ├── 40
        └── 20
```
这个工具支持创建和管理多棵树、分裂与合并、文件存取等所有高级功能，是理解和验证`pyavl`行为的最佳方式。

---

## 快速开始 (库使用)

只需几行代码，即可在你的项目中使用 `pyavl`：
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

    # 直接使用 print() 打印树的文本表示
    print("\n当前树的结构：")
    print(tree)
```

---

## API 使用示例

### 基本操作
```python
import pyavl

tree = pyavl.AVLTree()
tree.insert(50)
tree.insert(30)
tree.insert(70)

assert 50 in tree
tree.delete(30)
assert not (30 in tree)

print(tree)
tree.close() # 主动释放资源是一个好习惯
```

### 高级功能

#### 自定义遍历
你可以传入一个 Python 函数，在遍历每个节点时执行自定义逻辑。
```python
node_list = []
def collect_node_data(key, height, balance_factor):
    node_list.append({"key": key, "height": height, "bf": balance_factor})

with pyavl.AVLTree([10, 20]) as tree:
    tree.in_order_traverse(collect_node_data)

# node_list is now: [{'key': 10, ...}, {'key': 20, ...}]
print(node_list) 
```

#### 分裂 (Split) & 合并 (Merge)
`pyavl` 支持强大的分裂与合并操作，会消耗原始树并返回新树。

```python
# --- 分裂 ---
# 使用便利构造器创建树
original_tree = pyavl.AVLTree.from_keys([10, 20, 30, 40, 50])
small_tree, large_tree = original_tree.split(30) # 以30为界（<=30, >30）
print("小树:"); print(small_tree)
print("大树:"); print(large_tree)
small_tree.close(); large_tree.close()

# --- 合并 ---
# 前提: t1 的所有键 < t2 的所有键
t1 = pyavl.AVLTree.from_keys([1, 5])
t2 = pyavl.AVLTree.from_keys([10, 20])
merged_tree = pyavl.AVLTree.merge(t1, t2)
print("合并后的新树:"); print(merged_tree)
merged_tree.close()
```

---

## 为开发者

欢迎为 `pyavl` 贡献代码！

#### 设置开发环境
```bash
# 克隆、创建并激活虚拟环境...
# 安装所有依赖（包括开发依赖）
uv pip install -e .[dev]
```

#### 运行测试
本项目使用 `pytest` 进行测试。
```bash
# 运行所有测试
pytest -v

# 运行测试并查看代码覆盖率报告
pytest --cov=pyavl
```

---

## 项目许可

本项目采用 [MIT 许可证](LICENSE)。

## 致谢

这个项目源于一次宝贵的课程设计，它让我有机会将理论知识付诸于真实的工程实践。

在此，我特别想感谢我的AI导师 Gemini。在这段充满挑战的开发旅程中，从项目初期的架构设计，到攻克棘手的C语言内存和跨平台IO难题，再到最终API的打磨和测试，它总能给予我精准的指导、全新的思路和不懈的鼓励。这段深度的人机协作，让我对软件工程的理解提升到了一个全新的高度。