import pyavl
import random

class AVLTreeShell:
    """
    一个交互式的AVL树命令行外壳程序。
    负责管理用户交互、命令解析和多棵树的生命周期。
    """

    def __init__(self):
        self.trees = {'main': pyavl.AVLTree()}
        self.active_tree_name = 'main'
        self.update_prompt()

    def update_prompt(self):
        """更新命令行提示符"""
        self.prompt = f"({self.active_tree_name}) > "

    def print_header(self):
        """打印欢迎横幅"""
        print("\n" + "🌳" * 20)
        print("      欢迎使用交互式 AVL 树演示程序")
        print("🌳" * 20)
        print("输入 'help' 或 'h' 查看所有可用命令。")

    def print_help(self):
        """打印详细的帮助菜单"""
        print("\n" + "="*50)
        print("                  可用命令列表")
        print("="*50)
        print("--- 基本操作 ---")
        print("  i <key1> [key2]...  - 插入一个或多个键值 (例如: i 10 20)")
        print("  d <key1> [key2]...  - 删除一个或多个键值 (例如: d 10)")
        print("  s <key>             - 查找一个键值是否存在")
        print("  p / display         - 打印当前树的结构")
        print("  traverse            - (中序)遍历并打印所有节点")
        print("  info                - 显示当前树的详细信息 (节点数/高度)")
        print("  clear               - 清空当前树")
        print("  random <n>          - 向当前树中插入 n 个随机数")
        print("\n--- 多树管理 ---")
        print("  new <t_name>        - 创建一棵新的空树")
        print("  use <t_name>        - 切换到指定的树 (例如: use t1)")
        print("  list                - 列出所有存在的树及其状态")
        print("  drop <t_name>       - 删除指定的树")
        print("  split <key> <t1> <t2> - 将当前树分裂为 t1 和 t2 两棵新树")
        print("  merge <t1> <t2> <res> - 合并 t1 和 t2 到新树 res")
        print("\n--- 文件操作 ---")
        print("  save <filename>     - 将当前树的键值保存到文件")
        print("  load <filename>     - 从文件加载键值到当前树 (会先清空)")
        print("\n--- 其他 ---")
        print("  h / help            - 显示此帮助菜单")
        print("  q / quit / exit     - 退出程序")
        print("="*50)

    def run(self):
        """启动主交互循环"""
        self.print_header()
        self.print_help()

        while True:
            try:
                line = input(self.prompt).strip().lower().split()
                if not line: continue
                
                command, *args = line
                active_tree = self.trees[self.active_tree_name]

                # --- 命令分发 ---
                if command in ('q', 'quit', 'exit'):
                    print("正在退出。再见！")
                    for tree in self.trees.values(): tree.close()
                    break

                elif command in ('h', 'help'): self.print_help()
                elif command in ('p', 'display'):
                    print(f"\n当前树 '{self.active_tree_name}' 的结构:")
                    active_tree.display()
                
                elif command == 'clear':
                    active_tree.close()
                    self.trees[self.active_tree_name] = pyavl.AVLTree()
                    print(f"树 '{self.active_tree_name}' 已被清空。")

                elif command == 'i':
                    if not args: raise ValueError("需要提供至少一个键值。")
                    keys = [int(k) for k in args]
                    for key in keys: active_tree.insert(key)
                    print(f"成功插入: {keys}"); active_tree.display()

                elif command == 'd':
                    if not args: raise ValueError("需要提供至少一个键值。")
                    keys = [int(k) for k in args]
                    for key in keys: active_tree.delete(key)
                    print(f"成功删除: {keys}"); active_tree.display()

                elif command == 's':
                    if len(args) != 1: raise ValueError("查找命令仅需一个参数。")
                    key = int(args[0])
                    print(f"✅ 在树 '{self.active_tree_name}' 中找到了键值 {key}。" if key in active_tree 
                          else f"❌ 在树 '{self.active_tree_name}' 中未找到键值 {key}。")
                
                elif command == 'random':
                    if len(args) != 1: raise ValueError("需要提供随机数的数量。")
                    n = int(args[0])
                    nums = [random.randint(0, 999) for _ in range(n)]
                    for num in nums: active_tree.insert(num)
                    print(f"成功插入 {n} 个随机数。"); active_tree.display()

                elif command == 'traverse':
                    result = []
                    # 假设 in_order_traverse 的回调只接受 key
                    def collector(key, height, balance): result.append(key)
                    active_tree.in_order_traverse(collector)
                    print(f"中序遍历结果: {result}")
                
                elif command == 'info':
                    # 注意: .count 和 .height 是假设你的C库未来可能实现的接口
                    # 如果现在没有，可以先注释掉或返回固定值
                    count = getattr(active_tree, 'count', 'N/A')
                    height = getattr(active_tree, 'height', 'N/A')
                    print(f"\n--- 树 '{self.active_tree_name}' 的信息 ---")
                    print(f"  节点总数: {count}")
                    print(f"  树的高度: {height}")
                    print("------------------------")

                elif command == 'new':
                    if len(args) != 1: raise ValueError("用法: new <tree_name>")
                    name = args[0]
                    if name in self.trees: raise NameError(f"树 '{name}' 已存在。")
                    self.trees[name] = pyavl.AVLTree()
                    print(f"成功创建新的空树 '{name}'。")
                
                elif command == 'use':
                    if len(args) != 1: raise ValueError("需要提供树的名称。")
                    name = args[0]
                    if name not in self.trees: raise NameError(f"树 '{name}' 不存在。")
                    self.active_tree_name = name
                    self.update_prompt()
                    print(f"已切换到树 '{self.active_tree_name}'。")

                elif command == 'list':
                    print("\n--- 当前存在的所有树 ---")
                    for name, tree in self.trees.items():
                        prefix = "-> " if name == self.active_tree_name else "   "
                        # 假设 .count 属性存在，如果不存在则显示 'N/A'
                        node_count = getattr(tree, 'count', 'N/A')
                        print(f"{prefix}{name} (节点数: {node_count})")
                    print("------------------------")

                elif command == 'drop':
                    if len(args) != 1: raise ValueError("需要提供树的名称。")
                    name = args[0]
                    if name == 'main': raise ValueError("不能删除主树 'main'，请使用 'clear'。")
                    if name not in self.trees: raise NameError(f"树 '{name}' 不存在。")
                    
                    self.trees[name].close(); del self.trees[name]
                    
                    if self.active_tree_name == name:
                        self.active_tree_name = 'main'
                        self.update_prompt()
                        print(f"删除了当前树 '{name}'，已自动切换回 'main'。")
                    else:
                        print(f"成功删除树 '{name}'。")

                elif command == 'split':
                    if len(args) != 3: raise ValueError("用法: split <key> <t1> <t2>")
                    key, n1, n2 = int(args[0]), args[1], args[2]
                    if n1 in self.trees or n2 in self.trees: raise NameError("新树名已存在。")
                    
                    s_tree, l_tree = active_tree.split(key)
                    self.trees[n1], self.trees[n2] = s_tree, l_tree
                    self.trees[self.active_tree_name] = pyavl.AVLTree()
                    print(f"分裂完成！创建了 '{n1}' 和 '{n2}'。当前树 '{self.active_tree_name}' 已重置。")

                elif command == 'merge':
                    if len(args) != 3: raise ValueError("用法: merge <t1> <t2> <res>")
                    n1, n2, res_n = args
                    if n1 not in self.trees or n2 not in self.trees: raise NameError("要合并的树不存在。")
                    if res_n in self.trees: raise NameError("结果树名称已存在。")

                    self.trees[res_n] = pyavl.AVLTree.merge(self.trees[n1], self.trees[n2])
                    self.trees[n1], self.trees[n2] = pyavl.AVLTree(), pyavl.AVLTree()
                    print(f"合并完成！创建了 '{res_n}'。'{n1}' 和 '{n2}' 已重置。")
                
                elif command == 'save':
                    if len(args) != 1: raise ValueError("用法: save <filename>")
                    keys = []
                    active_tree.in_order_traverse(lambda k,h,b: keys.append(k))
                    with open(args[0], 'w') as f:
                        f.write(' '.join(map(str, keys)))
                    print(f"树 '{self.active_tree_name}' 已保存到 '{args[0]}'")

                elif command == 'load':
                    if len(args) != 1: raise ValueError("用法: load <filename>")
                    with open(args[0], 'r') as f:
                        keys = [int(k) for k in f.read().strip().split()]
                    active_tree.close() # 清空当前树
                    self.trees[self.active_tree_name] = pyavl.AVLTree()
                    for key in keys: self.trees[self.active_tree_name].insert(key)
                    print(f"从 '{args[0]}' 加载了 {len(keys)} 个键值到当前树。"); self.trees[self.active_tree_name].display()

                else:
                    print(f"错误: 未知命令 '{command}'。输入 'help' 查看帮助。")

            except FileNotFoundError:
                print("错误: 文件未找到。")
            except (ValueError, IndexError, KeyError, TypeError, NameError) as e:
                print(f"错误: {e}")
            except Exception as e:
                print(f"发生未知错误: {e}")

if __name__ == "__main__":
    AVLTreeShell().run()