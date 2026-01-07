

"""
Cursor编程
Cursor编辑器：
https://cursor.com/
Cursor 是基于 VSCode 开发的AI代码编辑器，提供智能代码补全、代码生成、代码修改、代码搜索和代码解释等。
与其他工具不同，Cursor 将 AI 辅助编码直接融入到编辑器的核心功能中，比如Curosr可以理解整个工程的代码，同时修改多个文件。可以通过 .cursorrules 文件定制 AI 的行为。
Lingma, 3. cursor 是VSCode的二次开发

Cursor Rules 帮助你定制 AI 行为，让它符合你的编码风格和项目需求。
规则设置: File => Preference => Cursor Setting
1. 之前完成正确的功能，尽量不要修改。
比如当前的instruction是完善功能A的，那么只需要专注功能A，不需要修改其他功能（比如功能B）。
2. 生成的注释用中文，并使用 UTF-8 编码。
3. 生成的代码有时候会存在中文乱码的情况，所以你在生成中文的时候，需要检查是否有中文乱码，如果有乱码需要修正。
4. 如果修改某个函数的实现，先理解之前函数实现的逻辑。然后在原来的基础上，再进行修改（保留之前的函数逻辑，不要移除）



Cursor的主要功能：
• Composer/Agent（Cmd + I）=> 现已升级为Agent模式
    允许同时编辑多个文件，并根据高级指令生成完整的应用程序，突破了单行和单文件编辑的限制。它
    能够理解项目结构上下文，并进行交互式代码优化。Composer 字面意思是作曲家，在 Cursor 中，它
    可以帮助你快速生成代码，如同自动驾驶，只需要告诉它你要做什么，它就可以帮你完成。
• 聊天功能（Cmd + L）  用于针对更宽泛的代码问题进行对话，支持多轮对话，解答更广泛的编程问题
• 提示框功能(Cmd + K)  用于生成或修改局部的代码
• Tab功能：相比GitHub Copilot等辅助开发工具，Cursor的优势在于它的代码编辑能力，不仅可以插入代码，而且可以对现有的代码进行修改，这也是Cursor在官方文档中多次强调的



Cursor 使用：
1. 打开对应文件夹，则为打开指定项目
2. 配置 python 编译环境（在插件栏中搜索python，点击安装）
3. 设置模型：点击 File => Preferences => Cursor Settings中的Models 添加模型 Add Models，创建deepseek-r1和deepseek-v3


Trae使用
Trae编辑器 (The Real AI Engineer) ：https://www.trae.com.cn/
字节推出的一款 AI 驱动的集成开发环境，特点：Builder 模式：Trae的亮点，它会自主拆解需求并自动完成多轮编码任务，从想法描述到功能实现一气呵成。
多模态支持：开发者可以上传图像，Trae 能够理解图像内容并生成相关代码
免费使用：目前 Trae 提供免费访问，包括内置的 Doubao-1.5-pro, DeepSeek-R1, DeepSeek-V3


"""