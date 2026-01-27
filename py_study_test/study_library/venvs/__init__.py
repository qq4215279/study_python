
"""
Python虚拟环境
什么是虚拟环境
虚拟环境（Virtual Environment）是一个 **独立 隔离** 的 Python 运行环境，它能够独立于真实环境存在，并且可以同时有多个互相独立的Python虚拟环境，每个虚拟环境都可以营造一个干净的开发环境，对于项目的依赖、版本的控制有着非常重要的作用。你可以在不同项目中使用不同的 Python 版本和依赖库，而不会相互影响。

虚拟环境的作用
1. 避免依赖冲突
    - 不同项目可能需要不同版本的库。
    - 直接在系统环境安装多个版本的库，容易导致兼容性问题，而虚拟环境可以让每个项目独立运行所需的版本。
2. 防止污染全局环境
    - 如果所有 Python 项目都共用一个全局环境，安装或卸载某个库可能影响其他项目的运行。
  使用虚拟环境，每个项目的依赖都在自己的目录中，不会污染全局 Python 目录。
3. 保持项目的可移植性
    - 在团队协作或部署到服务器时，可以迁移环境，使用 requirements.txt 记录所有依赖，其他人可以用虚拟环境安装相同的依赖，保证代码能在不同环境下运行一致。


官方推荐虚拟环境（venv）：Python 官方提供的 venv 方案十分好用，而且Python 3.3 以上版本自带 venv， 我们大多数情况下使用。
相关操作命令如下：
1. 检查venv是否可用: python -m venv --help  # 若显示帮助信息说明功能正常
2. 创建虚拟环境（推荐在项目根目录创建）：python -m venv .venv
3. 激活虚拟环境:
  - windows: .venv\Scripts\activate     # 激活后提示符变为 (.venv) PS C:\path>
  - mac: source .venv/bin/activate      # 激活后提示符变为 (.venv) user@host:~$
4. 查看激活状态
  - Linux/macOS系统: which python
  - Windows系统: where python  # 应显示虚拟环境路径下的python

5. 安装依赖包退出虚拟环境: deactivate

6. 删除虚拟环境（慎用）:
  - Windows: 直接删除环境目录即可
  - Linux/macOS: rm -rf .venv

7. 环境迁移:
7.1. 导出依赖包（已写项目）：pip freeze > requirements.txt
7.2. 安装依赖包（在新环境中）：pip install -r requirements.txt


venv环境缺陷：分不清项目中那些是项目组需要的直接依赖，那些是直接依赖需要的间接依赖。
    就算卸载直接依赖，间接依赖也卸载不了，留在了虚拟环境中，间接依赖永远的留在了项目中称为了孤儿依赖。
解决方式：使用 pyproject.toml  如下：
[project]
name = "myproject"
version = "0.1.0"
depanencies = [
    "requests",
    "numpy",
]

有了 pyproject.toml 后，可以直接删除 requirements.txt。后续安装新包则在 toml 文件中添加即可
之后安装依赖（. 代表安装当前目录下的所有依赖，-e 代表不会把源码安装到site-packages）：


这种方式痛点：无法直接用命令 pip install  这么方便。

解决方式：使用 uv 命令，可以替代上面的方式
命令：
1. 添加依赖: uv add flask
2. 同步项目环境(还会自动创建.venv 环境)：uv sync   (创建环境后，在用 source .venv/bin/activate 激活环境)
3. 在虚拟环境上下文中执行命令：uv run main.py



uv 入门教程 -- Python 包与环境管理工具
在 Python 开发中，包管理和环境隔离是每个开发者都会遇到的问题。
无论是 pip 的缓慢、virtualenv 的繁琐，还是 conda 的臃肿，uv 都让开发者们期待一个更高效的解决方案。

什么是 uv？
uv 是由 Astral 公司开发的一款 Rust 编写的 Python 包管理器和环境管理器，它的主要目标是提供比现有工具快 10-100 倍的性能，同时保持简单直观的用户体验。
uv 可以替代 pip、virtualenv、pip-tools 等工具，提供依赖管理、虚拟环境创建、Python 版本管理等一站式服务。

安装 uv
1. 在 macOS 上安装，
  推荐使用 Homebrew 安装：brew install uv
  或者使用官方安装脚本：curl -LsSf https://astral.sh/uv/install.sh | sh
2. 在 Linux 上安装
  curl -LsSf https://astral.sh/uv/install.sh | sh
3. 在 Windows 上安装
  使用 Winget：winget install uv
  使用官方安装脚本：irm https://astral.sh/uv/install.ps1 | iex


命令：
1. 安装完成后，验证安装是否成功：uv --version
2. 查看可用的 Python 版本：uv python list
3. 安装特定版本的 Python eg: 3.12: uv python install 3.12
4. 设置全局默认 Python 版本：uv python default 3.12
5. 管理虚拟环境
  5.1. 创建名为 .venv 的虚拟环境（默认）: uv venv
  5.2. 激活环境（macOS/Linux）: source .venv/bin/activate
       激活环境（Windows）: .venv\Scripts\activate
  5.3. 在项目中指定 Python 版本： uv python pin 3.11
6. 包管理
  6.1. 安装依赖包：
    - 安装最新版本 uv pip install requests
    - 安装特定版本 uv pip install requests==2.31.0
    - 从 requirements.txt 安装  uv pip install -r requirements.txt
  6.2. 升级包：uv pip upgrade requests
  6.3. 卸载包：uv pip uninstall requests
  6.4. 导出依赖：
        - 导出当前环境的依赖： uv pip freeze > requirements.txt
        - 导出生产环境依赖（排除开发依赖）：uv pip freeze --production > requirements.txt
7. 项目管理
  7.1. 初始化一个新项目：uv init my_project
                      cd my_project
  7.2. 安装项目的依赖： uv sync

8. 迁移到 uv
如果你正在使用其他工具，可以轻松迁移到 uv，对于使用 pip + virtualenv 的项目：
  8.1. 创建虚拟环境: uv venv
  8.1. 激活 uv 虚拟环境: source .venv/bin/activate
  8.3. 安装依赖: uv pip install -r requirements.txt

9. 其他命令
  - 列出uv支持的python版本  uv python list
  - 安装某个python版本 (3.12)  uv python install cpython3.12
  - 使用特定版本python运行xxx.py  uv run -p 3.12 xxx.py
  - 运行python交互界面  uv run -p 3.12 python
  - 使用系统python或当前工程的虚拟环境运行xxx.py  uv run xxx.py
  - 创建工程  uv init -p 3.12 my_project
  - 添加依赖 (pydantic_ai)  uv add pydantic_ai
  - 打印依赖树  uv tree
  - 删除依赖  uv remove pydantic_ai
  - 编译工程  uv build

"""