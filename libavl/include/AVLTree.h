/* File: AVLTree.h */

#ifndef AVLTREE_H
#define AVLTREE_H

/* --- 不透明指针定义 --- */

/**
 * @brief AVL树的句柄(Handle)。
 * 这是一个不透明指针，隐藏了树节点的内部结构。
 * 用户应使用 avl_* 系列函数来操作此类型的变量。
 */
struct _Node; // 前向声明一个内部结构体
typedef struct _Node* AVLTree; // 将指向该结构体的指针定义为公共类型 AVLTree

/* --- 公共API函数声明 --- */

/**
 * @brief 创建一棵空的AVL树。
 * @return 返回一个指向空树的句柄 (实际上是NULL)。
 */
AVLTree avl_create(void);

/**
 * @brief 销毁一棵AVL树，释放所有节点占用的内存。
 * @param tree 需要被销毁的树的句柄。
 */
void avl_destroy(AVLTree tree);

/**
 * @brief 向AVL树中插入一个新键值。
 * @param tree 树的句柄。
 * @param key  要插入的键值。
 * @return 返回操作后树的新句柄 (根节点可能会改变)。
 */
AVLTree avl_insert(AVLTree tree, int key);

/**
 * @brief 从AVL树中删除一个键值。
 * @param tree 树的句柄。
 * @param key  要删除的键值。
 * @return 返回操作后树的新句柄 (根节点可能会改变)。
 */
AVLTree avl_delete(AVLTree tree, int key);

/**
 * @brief 在AVL树中查找一个键值是否存在。
 * @param tree 树的句柄。此操作不会修改树，故使用const。
 * @param key  要查找的键值。
 * @return 如果找到返回1 (true)，否则返回0 (false)。
 */
int avl_search(const AVLTree tree, int key);

/**
 * @brief 以美观、可视化的方式打印整棵树的结构。
 * @param tree 树的句柄。此操作不会修改树，故使用const。
 */
void avl_display_to_buffer(const AVLTree tree, char* out_buffer, int buffer_size);

//  简单的打印函数
void avl_display(const AVLTree tree);

/* --- 选做内容：公共API函数声明 --- */

/**
 * @brief 合并两棵AVL树 T1 和 T2。
 * @前提 T1 中的所有键值必须都小于 T2 中的所有键值。
 * @param T1 较小的树（所有键值都小于T2）。
 * @param T2 较大的树（所有键值都大于T1）。
 * @return 返回合并后形成的新AVL树的句柄。
 */
AVLTree avl_merge(AVLTree T1, AVLTree T2);

/**
 * @brief 将一棵AVL树 T 按键值 x 分裂成两棵新的AVL树。
 * @param T         需要被分裂的原始树的句柄。
 * @param x         分裂的基准键值。
 * @param T_small   (出参) 一个指向树句柄的指针，用于接收分裂后包含所有 key <= x 的新树。
 * @param T_large   (出参) 一个指向树句柄的指针，用于接收分裂后包含所有 key > x 的新树。
 */
void avl_split(AVLTree T, int x, AVLTree* T_small, AVLTree* T_large);

// 它接受 key, height 和 balance_factor 作为参数
typedef void (*avl_traverse_callback)(int key, int height, int bf);

// 声明新的遍历函数
void avl_in_order_traverse(AVLTree tree, avl_traverse_callback callback);

/**
 * @brief 获取AVL树中的节点总数。
 * @param tree 树的句柄。
 * @return 返回节点数量。如果树为空，返回0。
 */
int avl_get_count(const AVLTree tree);

/**
 * @brief 获取AVL树的高度。
 * @param tree 树的句柄。
 * @return 返回树的高度。空树高度为-1或0，取决于你的定义。
 */
int avl_get_height(const AVLTree tree);

#endif /* AVLTREE_H */