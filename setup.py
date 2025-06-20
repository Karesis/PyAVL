from setuptools import setup, find_packages

setup(
    # 明确告诉 setuptools 在 'src' 目录下查找包
    packages=find_packages(where="src"),
    # 明确告诉 setuptools 包的根目录是 'src'
    package_dir={"": "src"},

    # CFFI 的配置
    cffi_modules=[
        "src/pyavl/_cffi_build.py:ffibuilder",
    ]
)