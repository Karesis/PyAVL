from cffi import FFI

ffibuilder = FFI()

# 1. 声明 C 接口
#    这是从你的 AVLTree.h 精确转换而来的。
ffibuilder.cdef("""
    /* --- 不透明指针声明 --- */
    // CFFI 通过 "..." 知道这是一个它不需要了解内部细节的结构体
    typedef void *AVLTree;

    /* --- 公共API函数声明 --- */
    AVLTree avl_create(void);
    void avl_destroy(AVLTree tree);
    AVLTree avl_insert(AVLTree tree, int key);
    AVLTree avl_delete(AVLTree tree, int key);
    int avl_search(const AVLTree tree, int key);
    void avl_display(const AVLTree tree);

    /* --- 选做内容：公共API函数声明 --- */
    AVLTree avl_merge(AVLTree T1, AVLTree T2);
    void avl_split(AVLTree T, int x, AVLTree* T_small, AVLTree* T_large);
    
    /* --- 回调函数类型和遍历函数 --- */
    typedef void (*avl_traverse_callback)(int key, int height, int bf);
    void avl_in_order_traverse(AVLTree tree, avl_traverse_callback callback);
""")

# 2. 配置 C 源码
ffibuilder.set_source(
    "pyavl._pyavl_c",               # 生成的 Python 扩展模块名
    '#include "AVLTree.h"',         # 编译时包含的头文件
    sources=['libavl/src/AVLTree.c'],       # C 源文件
    include_dirs=['libavl/include'],        # C 头文件目录
    # 如果你的C代码需要链接数学库(-lm)，可以像下面这样添加
    # libraries=['m'] 
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)