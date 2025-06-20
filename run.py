import pyavl

def print_menu():
    """打印操作菜单"""
    print("\n" + "="*30)
    print("      AVL Tree Operations")
    print("="*30)
    print("  i <key>  - Insert a key")
    print("  d <key>  - Delete a key")
    print("  s <key>  - Search for a key")
    print("  p        - Print the tree")
    print("  q        - Quit")
    print("="*30)

def main():
    """主交互循环"""
    # 使用 with 语句确保程序退出时树能被正确销毁
    with pyavl.AVLTree() as tree:
        print("AVL Tree initialized.")
        tree.display()

        while True:
            print_menu()
            try:
                # 获取用户输入并分割指令和参数
                line = input("> ").strip().lower().split()
                if not line:
                    continue
                
                command = line[0]
                
                if command == 'q':
                    print("Exiting. Goodbye!")
                    break
                
                elif command == 'p':
                    print("\nCurrent Tree Structure:")
                    tree.display()
                    
                elif command in ('i', 'd', 's'):
                    if len(line) < 2:
                        print("Error: Command requires a key.")
                        continue
                    
                    key = int(line[1])
                    
                    if command == 'i':
                        print(f"Inserting {key}...")
                        tree.insert(key)
                        print("Tree updated:")
                        tree.display()
                    
                    elif command == 'd':
                        print(f"Deleting {key}...")
                        tree.delete(key)
                        print("Tree updated:")
                        tree.display()
                        
                    elif command == 's':
                        found = key in tree
                        if found:
                            print(f"Key {key} found in the tree.")
                        else:
                            print(f"Key {key} not found in the tree.")
                            
                else:
                    print(f"Error: Unknown command '{command}'")

            except (ValueError, IndexError):
                print("Error: Invalid input. For insert/delete/search, use command followed by a number (e.g., 'i 10').")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()