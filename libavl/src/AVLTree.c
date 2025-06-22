#include "AVLTree.h" 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* --- 内部定义 --- */

// 内部节点结构体定义 (完全隐藏，不对外暴露)
typedef struct _Node {
    int key;
    struct _Node* left;
    struct _Node* right;
    int height;
} _Node;

// 宏定义
#define _MAX(a, b) ((a) > (b) ? (a) : (b))


/* --- 内部(私有)辅助函数声明与实现 --- */

// 所有内部函数都使用 static 修饰，并以 _ 为前缀

static int _get_height(_Node* node) {
    if (node == NULL) return 0;
    return node->height;
}

static int _get_balance_factor(_Node* node) {
    if (node == NULL) return 0;
    return _get_height(node->left) - _get_height(node->right);
}

static _Node* _create_node(int key) {
    _Node* node = (_Node*)malloc(sizeof(_Node));
    node->key = key;
    node->left = NULL;
    node->right = NULL;
    node->height = 1; // 新节点高度为1
    return node;
}

static _Node* _min_value_node(_Node* node) {
    _Node* current = node;
    while (current && current->left != NULL) {
        current = current->left;
    }
    return current;
}
 
static _Node* _find_max_node(_Node* node) {
    _Node* current = node;
    while (current && current->right != NULL) {
        current = current->right;
    }
    return current;
}

static _Node* _right_rotate(_Node* y) {
    _Node* x = y->left;
    _Node* T2 = x->right;
    x->right = y;
    y->left = T2;
    y->height = _MAX(_get_height(y->left), _get_height(y->right)) + 1;
    x->height = _MAX(_get_height(x->left), _get_height(x->right)) + 1;
    return x;
}

static _Node* _left_rotate(_Node* x) {
    _Node* y = x->right;
    _Node* T2 = y->left;
    y->left = x;
    x->right = T2;
    x->height = _MAX(_get_height(x->left), _get_height(x->right)) + 1;
    y->height = _MAX(_get_height(y->left), _get_height(y->right)) + 1;
    return y;
}

static _Node* _rebalance(_Node* node) {
    if (node == NULL) return NULL;

    node->height = 1 + _MAX(_get_height(node->left), _get_height(node->right));
    int balance = _get_balance_factor(node);

    // 左-左 或 左-右
    if (balance > 1) {
        if (_get_balance_factor(node->left) < 0) { // 左-右
            node->left = _left_rotate(node->left);
        }
        return _right_rotate(node); // 左-左
    }
    // 右-右 或 右-左
    if (balance < -1) {
        if (_get_balance_factor(node->right) > 0) { // 右-左
            node->right = _right_rotate(node->right);
        }
        return _left_rotate(node); // 右-右
    }
    // 无需旋转
    return node;
}


// 内部插入函数的递归实现
static _Node* _insert_recursive(_Node* node, int key) {
    if (node == NULL) return _create_node(key);

    if (key < node->key) {
        node->left = _insert_recursive(node->left, key);
    } else if (key > node->key) {
        node->right = _insert_recursive(node->right, key);
    } else {
        // 不允许重复键值
        return node;
    }
    
    // 插入后，从插入点回溯到根的路径上所有节点都需要更新高度并检查平衡
    return _rebalance(node);
}

// 内部删除函数的递归实现
static _Node* _delete_recursive(_Node* root, int key) {
    if (root == NULL) return root;

    if (key < root->key) {
        root->left = _delete_recursive(root->left, key);
    } else if (key > root->key) {
        root->right = _delete_recursive(root->right, key);
    } else {
        if ((root->left == NULL) || (root->right == NULL)) {
            _Node* temp = root->left ? root->left : root->right;
            if (temp == NULL) {
                temp = root;
                root = NULL;
            } else {
                // 这种直接用子节点内容覆盖父节点的方式，在没有其它动态分配内存时是可行的
                // 但更好的做法是返回temp，让上一层递归去连接。不过我们保持原样。
                *root = *temp;
            }
            free(temp);
        } else {
            _Node* temp = _min_value_node(root->right);
            root->key = temp->key;
            root->right = _delete_recursive(root->right, temp->key);
        }
    }

    if (root == NULL) return root;
    
    // 删除后，从删除点回溯到根的路径上所有节点都需要更新高度并检查平衡
    return _rebalance(root);
}

static int _count_nodes(const _Node* node) {
    // 基本情况：如果节点为空，则其下的节点数为 0
    if (node == NULL) {
        return 0;
    }
    // 递归步骤：节点总数 = 1 (当前节点) + 左子树节点数 + 右子树节点数
    return 1 + _count_nodes(node->left) + _count_nodes(node->right);
}

static void _visual_to_buffer(
    const _Node* node,
    const char* prefix,
    int isTail,
    // --- 新增的参数 ---
    char* buffer,       // 目标缓冲区
    int* offset,        // 当前写入位置的指针
    int size            // 缓冲区总大小
) {
    if (node == NULL) return;

    // 检查缓冲区是否已满 (预留1字节给末尾的'\0')
    if (*offset >= size - 1) return;

    // [核心修改] 不再使用 printf，而是用 snprintf 写入到 buffer
    int written = snprintf(
        buffer + *offset,       // 从当前位置开始写
        size - *offset,         // 缓冲区剩余空间
        "%s%s%d\n",             // 格式不变
        prefix,
        isTail ? "└── " : "├── ",
        node->key
    );

    // 更新写入位置
    *offset += written;
    
    char newPrefix[256];
    // 这里使用更兼容的四个空格
    snprintf(newPrefix, sizeof(newPrefix), "%s%s", prefix, isTail ? "    " : "│   ");

    if (node->left != NULL && node->right != NULL) {
        _visual_to_buffer(node->right, newPrefix, 0, buffer, offset, size); // 递归调用也使用新函数
        _visual_to_buffer(node->left,  newPrefix, 1, buffer, offset, size);
    } else if (node->right != NULL) {
        _visual_to_buffer(node->right, newPrefix, 1, buffer, offset, size);
    } else if (node->left != NULL) {
        _visual_to_buffer(node->left,  newPrefix, 1, buffer, offset, size);
    }
}

static void _in_order_recursive(struct _Node* node, avl_traverse_callback callback) {
    if (node == NULL || callback == NULL) {
        return;
    }
    // 中序遍历：左 -> 根 -> 右
    _in_order_recursive(node->left, callback);
    callback(node->key, node->height, _get_balance_factor(node));
    _in_order_recursive(node->right, callback);
}


/* --- 公共API函数的实现 --- */

AVLTree avl_create(void) {
    return NULL;
}

void avl_destroy(AVLTree tree) {
    if (tree == NULL) return;
    avl_destroy(tree->left);
    avl_destroy(tree->right);
    free(tree);
}

AVLTree avl_insert(AVLTree tree, int key) {
    return _insert_recursive(tree, key);
}

AVLTree avl_delete(AVLTree tree, int key) {
    // 在删除前可以先检查是否存在，避免不必要的操作
    if (avl_search(tree, key) == 0) {
        printf("错误：键值 %d 不在树中，无法删除。\n", key);
        return tree;
    }
    return _delete_recursive(tree, key);
}

int avl_search(const AVLTree tree, int key) {
    const _Node* current = tree;
    while (current != NULL) {
        if (key < current->key) {
            current = current->left;
        } else if (key > current->key) {
            current = current->right;
        } else {
            return 1; // 找到了
        }
    }
    return 0; // 未找到
}

/**
 * @brief [改造后的公共API] 将AVL树的视觉表示形式写入用户提供的缓冲区。
 * * @param tree 指向AVL树的指针 (即根节点)。
 * @param out_buffer Python提供的用于写入的缓冲区。
 * @param buffer_size 缓冲区的总大小。
 */
void avl_display_to_buffer(const AVLTree tree, char* out_buffer, int buffer_size) {
    // 1. 安全检查
    if (out_buffer == NULL || buffer_size <= 0) {
        return; 
    }
    // 确保缓冲区在开始时是一个有效的空字符串
    out_buffer[0] = '\0';

    // 2. 处理空树的情况
    if (tree == NULL) {
        snprintf(out_buffer, buffer_size, "树是空的。\n");
        return;
    }

    // 3. 初始化写入位置并开始递归
    int offset = 0;
    _visual_to_buffer(tree, "", 1, out_buffer, &offset, buffer_size);
}

void avl_display(const AVLTree tree) {
    // 创建一个足够大的临时栈缓冲区
    char buffer[4096];
    
    // 调用新函数将内容写入缓冲区
    avl_display_to_buffer(tree, buffer, sizeof(buffer));
    
    // 然后用 printf 打印缓冲区的内容
    printf("%s", buffer);
}

int avl_get_height(const AVLTree tree) {
    // 将公共的、不透明的 AVLTree 指针转换为内部的 _Node 指针
    _Node* root = (_Node*)tree;
    
    if (root == NULL) {
        return 0; 
    }
    
    return root->height; 
}

int avl_get_count(const AVLTree tree) {
    // 直接调用我们的递归辅助函数
    return _count_nodes((const _Node*)tree);
}

/* --- 选做内容：合并与分裂 --- */

AVLTree avl_merge(AVLTree T1, AVLTree T2) {
    if (T1 == NULL) return T2;
    if (T2 == NULL) return T1;

    // 1. 从 T1 中找到最大的键值作为新的连接点
    _Node* max_node_T1 = _find_max_node(T1);
    int connecting_key = max_node_T1->key;
    
    // 2. 从 T1 中删除该最大值，得到一棵新的、依然平衡的 T1'
    AVLTree T1_prime = avl_delete(T1, connecting_key);
    
    // 3. 创建一个新的根节点
    _Node* new_root = _create_node(connecting_key);

    // 4. 连接 T1' 和 T2
    new_root->left = T1_prime;
    new_root->right = T2;
    
    // 5. 更新高度并对新根进行再平衡
    return _rebalance(new_root);
}

void avl_split(AVLTree T, int x, AVLTree* T_small, AVLTree* T_large) {
    if (T == NULL) {
        *T_small = NULL;
        *T_large = NULL;
        return;
    }

    if (x < T->key) {
        // 分裂点在左子树
        AVLTree left_subtree = T->left;
        AVLTree right_subtree = T->right;
        
        // 递归分裂左子树
        avl_split(left_subtree, x, T_small, T_large);
        
        // 分裂后，原根节点 T 和它的右子树需要与分裂左子树得到的 T_large' (原T_large) 合并
        // 注意：这里我们不能直接用 avl_merge，因为它会重新找最大值
        // 而是要以 T 作为连接点进行合并
        T->left = *T_large;
        T->right = right_subtree;
        *T_large = _rebalance(T);

    } else if (x > T->key) {
        // 分裂点在右子树 (与上面对称)
        AVLTree left_subtree = T->left;
        AVLTree right_subtree = T->right;
        
        avl_split(right_subtree, x, T_small, T_large);

        T->right = *T_small;
        T->left = left_subtree;
        *T_small = _rebalance(T);

    } else { // x == T->key
        // 找到分裂点，直接分裂
        *T_small = T->left;
        *T_large = T->right;

        // 将根节点 T 加入到 small 树中
        // 最简单的方法是创建一个新根
        _Node* new_small_root = _create_node(T->key);
        new_small_root->left = *T_small;
        *T_small = _rebalance(new_small_root);
        
        // 释放原根节点 T 的内存
        free(T);
    }
}



// 这是暴露给外部的公共函数
void avl_in_order_traverse(AVLTree tree, avl_traverse_callback callback) {
    _in_order_recursive(tree, callback);
}