

"""
Ollama 是一个开源框架，专为在本地机器上便捷部署和运行大模型而设计。
官方网址：https://ollama.com/

命令：
- 拉取模型：ollama pull bge-m3
- 查看已安装列表：`ollama list`
- 验证安装：`ollama --version` `ollama`
- 运行模型：`ollama run llama3.2`
    - 结束对话可以输入 /bye 或按 Ctrl+d 按键来结束
-

命令 (Command)	         说明 (Description)	                            示例 (Example)
ollama serve	        启动服务。启动 Ollama 的 API 服务（通常后台自动运行）。ollama serve
    默认端口：11434，不直接与用户交互，而是提供 API 接口

    强制杀死所有ollama进程  pkill -9 ollama
ollama run	            运行模型。如果不存在则自动拉取。	                    ollama run llama3
ollama stop	            停止模型。如果不存在则自动拉取。	                    ollama stop llama3
ollama pull	            拉取模型。从库中下载模型但不运行。	                ollama pull mistral
ollama ps	            查看进程。显示当前正在运行的模型及显存占用。	        ollama ps
ollama list	            列出模型。显示本地所有已下载的模型。	                ollama list
ollama rm	            删除模型。移除本地模型释放空间。	                    ollama rm llama3
ollama cp	            复制模型。将现有模型复制为新名称（用于测试）。	        ollama cp llama3 my-model
ollama create	        创建模型。根据 Modelfile 创建自定义模型（高级）。	    ollama create my-bot -f ./Modelfile
ollama show	            显示信息。查看模型的元数据、参数或 Modelfile。	    ollama show --modelfile llama3
ollama push	            推送模型。将你自定义的模型上传到 ollama.com。	        ollama push my-username/my-model
ollama help	            帮助。查看任何命令的帮助信息。	                    ollama help run


通过 Python SDK 使用模型
如果你希望将 Ollama 与 Python 代码集成，可以使用 Ollama 的 Python SDK 来加载和运行模型。
安装 Python SDK 执行以下命令：pip install ollama

自定义客户端。具体可看 ollama_demo.py

Ollama Python SDK 常用 API 方法
1. chat 方法。 与模型进行对话生成，发送用户消息并获取模型响应：
    ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])
2. generate 方法。用于文本生成任务。与 chat 方法类似，但是它只需要一个 prompt 参数：
    ollama.generate(model='llama3.2', prompt='Why is the sky blue?')
3. list 方法。列出所有可用的模型：ollama.list()
4. show 方法。显示指定模型的详细信息：ollama.show('llama3.2')
5. create 方法。从现有模型创建新的模型：
    ollama.create(model='example', from_='llama3.2', system="You are Mario from Super Mario Bros.")
6. copy 方法。复制模型到另一个位置：ollama.copy('llama3.2', 'user/llama3.2')
7. delete 方法。删除指定模型：ollama.delete('llama3.2')
8. pull 方法。从远程仓库拉取模型：ollama.pull('llama3.2')
9. push 方法。将本地模型推送到远程仓库：ollama.push('user/llama3.2')
10. embed 方法。生成文本嵌入：
    ollama.embed(model='llama3.2', input='The sky is blue because of rayleigh scattering')
11. ps 方法。查看正在运行的模型列表：ollama.ps()



"""