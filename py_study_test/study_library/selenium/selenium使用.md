

#  Selenium 攻略

[攻略来源](https://zhuanlan.zhihu.com/p/462460461)

**爬虫库**：

1. 抓取类：
   1. urllib(Python3),自带的库。
2. 解析类：
   1. re：正则表达式官方库，不仅仅是学习爬虫要使用，在其他字符串处理或者自然语言处理的过程中，这是绕不过去的一个库，强烈推荐掌握。
3. 综合类：
   1. selenium：所见即所得式爬虫。综合了抓取和解析两种功能，一站式解决。
   2. scrapy：另一个爬虫神器，适合爬取大量页面，甚至对分布式爬虫提供了良好的支持。强烈推荐。

## 准备工作

### 安装selenium库

```python
pip install selenium
```

### 安装浏览器驱动

1. 先查看本地`Chrome`浏览器版本：（两种方式均可）
   - 在浏览器的地址栏键入`Chrome://version`，即可查看浏览器版本号
   - 或者点击`Chrome`菜单 **帮助**→**关于Google Chrome**，查看浏览器版本号
2. 下载 chromedriver.exe   =>   [chromedriver.exe下载地址](http://chromedriver.storage.googleapis.com/index.html)



## 基本用法

### 初始化浏览器对象

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 指定绝对路径的方式
path = r"D:\Install\Google\chromedriver.exe"

# 1.1 初始化浏览器为chrome浏览器
browser = webdriver.Chrome(path)
# browser = webdriver.Chrome(executable_path=path)

# 1.2. 无界面的浏览器
'''
option = webdriver.ChromeOptions()
option.add_argument("headless")
browser = webdriver.Chrome(options=option)
'''

# 1.3 Service
# s = Service(path)
# browser = webdriver.Chrome(service=s)

# 关闭浏览器
browser.close()
```

### browser = webdriver.Chrome()

1. 访问百度首页：browser.get(r'https://www.baidu.com/')

2. 截图预览：browser.get_screenshot_as_file('截图.png')

3. 设置浏览器大小：

   1. `set_window_size()`：可以用来设置浏览器大小（就是分辨率）eg：browser.set_window_size(500,500)  
   2. `maximize_window`：则是设置浏览器为全屏。

4. 刷新页面：browser.refresh() 

5. 前进后退：

   1. `forward()`：前进。eg：browser.forward() 
   2. `back()`：后退。eg：browser.back()  

6. 获取页面基础属性：

   1. `title`：网页标题。eg：browser.title
   2. `current_url`：浏览器名称。eg：browser.current_url
   3. `page_source`：网页源码。eg：browser.page_source

7. 定位页面元素：`8种`定位页面元素的操作方式

   1. 定位：`find_element_by_id(by, value)`根据`id`属性获取

      `by` 类型在类`By`下：

      ```python
      class By:
          # id定位
          ID = "id"
          # xpath定位
          XPATH = "xpath"
          # link定位
          LINK_TEXT = "link text"
          # partial定位
          PARTIAL_LINK_TEXT = "partial link text"
          # name定位
          NAME = "name"
          # tag定位
          TAG_NAME = "tag name"
          # class定位
          CLASS_NAME = "class name"
          #  css定位
          CSS_SELECTOR = "css selector"
      ```

   eg：

   ```python
   browser.find_element(By.ID,'kw')
   browser.find_element(By.XPATH,'//*[@id="kw"]')
   browser.find_element(By.LINK_TEXT,'新闻')
   browser.find_element(By.PARTIAL_LINK_TEXT,'闻')
   browser.find_element(By.TAG_NAME,'input')
   browser.find_element(By.NAME,'wd')
   browser.find_element(By.CLASS_NAME,'s_ipt')
   browser.find_element(By.CSS_SELECTOR,'#kw')
   ```

8. 多窗口切换：比如同一个页面的不同子页面的节点元素获取操作，不同选项卡之间的切换以及不同浏览器窗口之间的切换操作等等。

9. Frame切换：

   - `switch_to.frame()`：切换到子页面
   - `switch_to.parent_frame()`：回到父页面

10. 选项卡切换：

    - `current_window_handle`：获取当前窗口的句柄。
    - `window_handles`：返回当前浏览器的所有窗口的句柄。
    - `switch_to_window()`：用于切换到对应的窗口。

    ```python
    from selenium import webdriver
    import time
    
    browser = webdriver.Chrome()
    
    # 打开百度
    browser.get('http://www.baidu.com')
    # 新建一个选项卡
    browser.execute_script('window.open()')
    print(browser.window_handles)
    # 跳转到第二个选项卡并打开知乎
    browser.switch_to.window(browser.window_handles[1])
    browser.get('http://www.zhihu.com')
    # 回到第一个选项卡并打开淘宝（原来的百度页面改为了淘宝）
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[0])
    browser.get('http://www.taobao.com')
    ```

11. 新建一个选项卡：browser.execute_script('window.open()')

12. 关闭浏览器：browser.close()

13. 运行JavaScript：`execute_script`

    ```python
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    browser.execute_script('alert("To Bottom")')
    ```

14. **延时等待**：

    如果遇到使用`ajax`加载的网页，页面元素可能不是同时加载出来的，这个时候尝试在`get`方法执行完成时获取网页源代码可能并非浏览器完全加载完成的页面。所以，这种情况下需要设置延时等待一定时间，确保全部节点都加载出来。

    1. 强制等待：`time.sleep(n)` 强制等待n秒，在执行`get`方法之后执行。

    2.  隐式等待：`implicitly_wait()`设置等待时间，如果到时间有元素节点没有加载出来，就会抛出异常。

       eg：隐式等待，等待时间10秒：`browser.implicitly_wait(10)  `

    3. 显式等待：设置一个等待时间和一个条件，在规定时间内，每隔一段时间查看下条件是否成立，如果成立那么程序就继续执行，否则就抛出一个超时异常。

       ```python
       from selenium import webdriver
       from selenium.webdriver.support.wait import WebDriverWait
       from selenium.webdriver.support import expected_conditions as EC
       from selenium.webdriver.common.by import By
       import time
       
       browser = webdriver.Chrome()
       browser.get('https://www.baidu.com')
       # 设置等待时间10s
       wait = WebDriverWait(browser, 10)
       # 设置判断条件：等待id='kw'的元素加载完成
       input = wait.until(EC.presence_of_element_located((By.ID, 'kw')))
       # 在关键词输入：关键词
       input.send_keys('Python')
       
       # 关闭浏览器
       time.sleep(2)
       browser.close()
       ```

       **WebDriverWait的参数说明**：

       > ```text
       > WebDriverWait(driver,timeout,poll_frequency=0.5,ignored_exceptions=None)
       > ```
       >
       > `driver`: 浏览器驱动
       >
       > `timeout`: 超时时间，等待的最长时间（同时要考虑隐性等待时间）
       >
       > `poll_frequency`: 每次检测的间隔时间，默认是0.5秒
       >
       > `ignored_exceptions`:超时后的异常信息，默认情况下抛出`NoSuchElementException`异常
       >
       > until(method,message='')
       >
       > `method`: 在等待期间，每隔一段时间调用这个传入的方法，直到返回值不是False
       >
       > `message`: 如果超时，抛出`TimeoutException`，将`message`传入异常
       >
       > until_not(method,message='')
       >
       > `until_not` 与`until`相反，`until`是当某元素出现或什么条件成立则继续执行，`until_not`是当某元素消失或什么条件不成立则继续执行，参数也相同。

       **WebDriverWait的参数说明**：

       > ```text
       > WebDriverWait(driver,timeout,poll_frequency=0.5,ignored_exceptions=None)
       > ```
       >
       > `driver`: 浏览器驱动
       >
       > `timeout`: 超时时间，等待的最长时间（同时要考虑隐性等待时间）
       >
       > `poll_frequency`: 每次检测的间隔时间，默认是0.5秒
       >
       > `ignored_exceptions`:超时后的异常信息，默认情况下抛出`NoSuchElementException`异常
       >
       > until(method,message='')
       >
       > `method`: 在等待期间，每隔一段时间调用这个传入的方法，直到返回值不是False
       >
       > `message`: 如果超时，抛出`TimeoutException`，将`message`传入异常
       >
       > until_not(method,message='')
       >
       > `until_not` 与`until`相反，`until`是当某元素出现或什么条件成立则继续执行，`until_not`是当某元素消失或什么条件不成立则继续执行，参数也相同。

       **其他等待条件**：

       ```python
       from selenium.webdriver.support import expected_conditions as EC
       
       # 判断标题是否和预期的一致
       title_is
       # 判断标题中是否包含预期的字符串
       title_contains
       
       # 判断指定元素是否加载出来
       presence_of_element_located
       # 判断所有元素是否加载完成
       presence_of_all_elements_located
       
       # 判断某个元素是否可见. 可见代表元素非隐藏，并且元素的宽和高都不等于0，传入参数是元组类型的locator
       visibility_of_element_located
       # 判断元素是否可见，传入参数是定位后的元素WebElement
       visibility_of
       # 判断某个元素是否不可见，或是否不存在于DOM树
       invisibility_of_element_located
       
       # 判断元素的 text 是否包含预期字符串
       text_to_be_present_in_element
       # 判断元素的 value 是否包含预期字符串
       text_to_be_present_in_element_value
       
       #判断frame是否可切入，可传入locator元组或者直接传入定位方式：id、name、index或WebElement
       frame_to_be_available_and_switch_to_it
       
       #判断是否有alert出现
       alert_is_present
       
       #判断元素是否可点击
       element_to_be_clickable
       
       # 判断元素是否被选中,一般用在下拉列表，传入WebElement对象
       element_to_be_selected
       # 判断元素是否被选中
       element_located_to_be_selected
       # 判断元素的选中状态是否和预期一致，传入参数：定位后的元素，相等返回True，否则返回False
       element_selection_state_to_be
       # 判断元素的选中状态是否和预期一致，传入参数：元素的定位，相等返回True，否则返回False
       element_located_selection_state_to_be
       
       #判断一个元素是否仍在DOM中，传入WebElement对象，可以判断页面是否刷新了
       staleness_of
       ```

    

### element = browser.find_element(By.ID, 'kw')

获取：`element = browser.find_element_by_class_name('index-logo-src')`

1. `get_attribute()`：获取属性
   1. 获取logo的图片地址：logo.get_attribute('src')
   2. 获取超链接：logo.get_attribute('href')
2. `text`：获取文本
3. `id`：获取id
4. `location`：获取位置
5. `tag_name`：获取标签名
6. `size`：获取大小属性
7. `send_keys()`：输入文本
8. `click()`：点击
9. `clear()`：清除文本
10. `submit()`：回车确认

### Cookie

在`selenium`使用过程中，还可以很方便对`Cookie`进行获取、添加与删除等操作。

1. 获取cookie：`get_cookies()`

2. 添加cookie：`add_cookie({'name':'才哥', 'value':'帅哥'})`

3. 删除cookie：`delete_all_cookies()`

   ```python
   from selenium import webdriver
   
   browser = webdriver.Chrome()
   # 知乎发现页
   browser.get('https://www.zhihu.com/explore')
   # 获取cookie
   print(f'Cookies的值：{browser.get_cookies()}')
   # 添加cookie
   browser.add_cookie({'name':'才哥', 'value':'帅哥'})
   print(f'添加后Cookies的值：{browser.get_cookies()}')
   # 删除cookie
   browser.delete_all_cookies()
   print(f'删除后Cookies的值：{browser.get_cookies()}')
   ```

### Select 下拉框

下拉框的操作相对复杂一些，需要用到`Select`模块。

先导入该类：`from selenium.webdriver.support.select import Select`

1. 三种选择某一选项项的方法：
   - select_by_index()：通过索引定位；注意：>index索引是从“0”开始。
   - select_by_value()：通过value值定位，va>lue标签的属性值。
   - select_by_visible_text()：通过文本值定位，即显>示在下拉框的值。
2. 三种返回options信息的方法
   - voptions：返回select元素所有>的options
   - all_selected_options：返回select元素中所>有已选中的选项
   - first_selected_options：返回select元素中选>中的第一个选项           
3. 四种取消选中项的方法
   - deselect_all： 取消全部的已选择项
   - deselect_by_index：取消已选中的索引项
   - deselect_by_value： 取消已选中的value值
   - deselect_by_visible_text：取消已选中的文本值

### ActionChains 模拟鼠标操作

既然是模拟浏览器操作，自然也就需要能模拟鼠标的一些操作了，这里需要导入`ActionChains` 类。

```python
# 1. 导入包
from selenium.webdriver.common.action_chains import ActionChains
# 2. 获取action `ActionChains(browser)`：调用`ActionChains()`类，并将浏览器驱动`browser`作为参数传入
actions = ActionChains(browser)
```

1. `click()`：左键

2. `context_click()`：右键。模拟鼠标双击，需要传入指定元素定位作为参数

   - `perform()`：执行`ActionChains()`中储存的所有操作，可以看做是执行之前一系列的操作

   eg：

   ```text
   # 定位到要右击的元素，这里选的新闻链接
   right_click = browser.find_element_by_link_text('新闻')
   
   # 执行鼠标右键操作
   ActionChains(browser).context_click(right_click).perform()
   ```

3. `double_click()`：双击

   ```python
   # 定位到要双击的元素
   double_click = browser.find_element_by_css_selector('#bottom_layer > div > p:nth-child(8) > span')
   # 双击
   ActionChains(browser).double_click(double_click).perform()
   ```
   
4. `drag_and_drop(source,target)`：拖拽。开始位置和结束位置需要被指定，这个常用于滑块类验证码的操作之类。

   ```python
   # 开始位置
   source = browser.find_element_by_css_selector("#draggable")
   
   # 结束位置
   target = browser.find_element_by_css_selector("#droppable")
   
   # 执行元素的拖放操作
   actions = ActionChains(browser)
   actions.drag_and_drop(source, target)
   actions.perform()
   ```

5. `move_to_element()`： 悬停

   ```python
   # 定位悬停的位置
   move = browser.find_element_by_css_selector("#form > span.bg.s_ipt_wr.new-pmd.quickdelete-wrap > span.soutu-btn")
   
   # 悬停操作
   ActionChains(browser).move_to_element(move).perform()
   ```

### Keys 模拟键盘操作

`selenium`中的`Keys()`类提供了大部分的键盘操作方法，通过`send_keys()`方法来模拟键盘上的按键。

引入`Keys`类：

```python
from selenium.webdriver.common.keys import Keys
```

常见的键盘操作

1. `send_keys(Keys.BACK_SPACE)`：删除键(BackSpace)

2. `send_keys(Keys.SPACE)`：空格键(Space)

3. send_keys(Keys.TAB)`：制表键(TAB)`

4. send_keys(Keys.ESCAPE)`：回退键(ESCAPE)`

5. send_keys(Keys.ENTER)`：回车键(ENTER)`

6. send_keys(Keys.CONTRL,'a')`：全选(Ctrl+A)`

7. send_keys(Keys.CONTRL,'c')`：复制(Ctrl+C)`

8. send_keys(Keys.CONTRL,'x')`：剪切(Ctrl+X)`

9. send_keys(Keys.CONTRL,'v')`：粘贴(Ctrl+V)`

10. send_keys(Keys.F1)`：键盘F1`

11. `send_keys(Keys.F12)`：键盘F12

12. .....

    ```python
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    import time
    
    browser = webdriver.Chrome()
    url = 'https://www.baidu.com'
    browser.get(url)  
    time.sleep(2)
    
    # 定位搜索框
    input = browser.find_element_by_class_name('s_ipt')
    # 输入python
    input.send_keys('python')
    time.sleep(2)
    
    # 回车
    input.send_keys(Keys.ENTER)
    time.sleep(5)
    
    # 关闭浏览器
    browser.close()
    ```