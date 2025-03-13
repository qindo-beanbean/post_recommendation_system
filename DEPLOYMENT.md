# PythonAnywhere 部署指南

本指南详细介绍如何将帖子推荐系统部署到 PythonAnywhere。

## 步骤 1: 注册 PythonAnywhere 账户

1. 访问 [PythonAnywhere](https://www.pythonanywhere.com/) 并注册一个账户（免费账户即可）。
2. 完成注册后登录。

## 步骤 2: 上传项目文件

有两种方式可以上传你的项目：

### 方式 1: 使用 Git（推荐）

1. 在 PythonAnywhere 中，打开一个 Bash 控制台（Dashboard -> Consoles -> Bash）。
2. 克隆你的 Git 仓库:
```bash
git clone https://github.com/yourusername/post-recommendation-system.git
```
3. 如果是私有仓库，需要输入你的 Git 凭据。

### 方式 2: 直接上传 ZIP 文件

1. 将项目文件打包为 ZIP 文件。
2. 在 PythonAnywhere Dashboard，点击 "Files" 标签。
3. 点击 "Upload a file" 按钮并上传你的 ZIP 文件。
4. 在 Bash 控制台中解压文件:
```bash
unzip your-project.zip -d post-recommendation-system
```

## 步骤 3: 创建虚拟环境并安装依赖

在 Bash 控制台中运行:

```bash
cd post-recommendation-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 步骤 4: 创建 Web 应用

1. 在 PythonAnywhere Dashboard，点击 "Web" 标签。
2. 点击 "Add a new web app" 按钮。
3. 选择 "Manual configuration"（手动配置）。
4. 选择 Python 版本（推荐 Python 3.8 或更高版本）。

## 步骤 5: 配置 Web 应用

在 "Web" 页面的 "Code" 部分:

1. 设置 "Source code" 路径为你的项目目录（例如 `/home/yourusername/post-recommendation-system`）。
2. 设置 "Working directory" 为你的项目目录。
3. 在 "Virtualenv" 部分，输入你的虚拟环境路径（例如 `/home/yourusername/post-recommendation-system/venv`）。

在 "WSGI configuration file" 部分:

1. 点击 WSGI 配置文件链接（如 `/var/www/yourusername_pythonanywhere_com_wsgi.py`）。
2. 用以下内容替换文件内容:

```python
import sys
import os

# 添加项目目录到 Python 路径
path = '/home/yourusername/post-recommendation-system'
if path not in sys.path:
    sys.path.append(path)

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 导入应用并创建 WSGI 应用对象
from app import create_app
application = create_app()
```

3. 保存文件。

## 步骤 6: 创建静态文件映射

在 "Web" 页面的 "Static files" 部分:

1. 添加以下映射:
   - URL: `/static/` 对应 Directory: `/home/yourusername/post-recommendation-system/static/`

## 步骤 7: 创建数据库目录

确保实例目录存在:

```bash
mkdir -p /home/yourusername/post-recommendation-system/instance
```

## 步骤 8: 启动 Web 应用

1. 回到 "Web" 页面。
2. 点击 "Reload" 按钮启动你的应用。

## 步骤 9: 访问应用

你的应用现在应该可以通过 `yourusername.pythonanywhere.com` 访问了。

## 故障排除

如果应用无法启动或有错误:

1. 检查错误日志:
   - 在 "Web" 页面，查看 "Error log" 部分。
2. 确保所有依赖都已正确安装:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. 确保文件权限设置正确。

## 维护应用

- 每次更新代码后，需要在 "Web" 页面点击 "Reload" 按钮。
- 免费账户的网站会在一段时间无活动后休眠，这是正常的。