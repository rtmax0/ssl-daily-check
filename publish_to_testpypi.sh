#!/bin/bash

# 构建包
poetry build

# 发布到 TestPyPI
poetry publish -r testpypi

# 等待几秒钟让 TestPyPI 处理上传的包
sleep 10

# 尝试从 TestPyPI 安装包
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ssl-daily-check

echo "如果没有错误信息，那么包已成功发布到 TestPyPI 并可以安装。"
