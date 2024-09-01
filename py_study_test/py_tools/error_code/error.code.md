# 错误码翻译工具介绍

## 介绍

**作用**：

- 将错误码的 `简体中文` 内容翻译成 `英文` 和 `繁体中文`
- 并生成对应 `errorTips_zh_CN.properties, errorTips_en_US.properties, errorTips_zh_TW.properties` 文件。

**文件说明**：

1. `generate_error_code.py`： 错误码生成脚本
2. `baidu_translate_util.py`：百度翻译工具类
3. `errorcode.java.template`：**ErrorCode.java** 代码生成模板



## 环境

1. 版本：`python3.8`
2. 依赖库：
    - `jinja2`: pip install jinja2
    - `requests`: pip install requests 
3. 修改 errorTips 生成目录: 进入 generate_error_code.py, 修改 ERROR_TIPS_DIR 变量路径


## 使用说明

1. 若错误码脚本目录不在`sgj`项目中，则需配置 项目根路径：`generate_error_code.PROJECT_ROOT_PATH`

   eg：PROJECT_ROOT_PATH = F:\Code\WorkSpace\yjxxl_server\app\trunk\hf-parent

2. 将 `error_code` 导入成一个python工程，运行 `generate_error_code` 中的 `main` 方法。