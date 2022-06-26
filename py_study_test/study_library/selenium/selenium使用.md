

#  Selenium 攻略

## 准备工作

### 安装selenium库

```python
pip install selenium
```

### 安装浏览器驱动

1. 先查看本地`Chrome`浏览器版本：（两种方式均可）
   - 在浏览器的地址栏键入`Chrome://version`，即可查看浏览器版本号
   - 或者点击`Chrome`菜单 **帮助**→**关于Google Chrome**，查看浏览器版本号
2. 下载 chromedriver.exe   => 下载地址  http://chromedriver.storage.googleapis.com/index.html



## 基本用法

### 初始化浏览器对象

```python
from selenium import webdriver

# 1.1 初始化浏览器为chrome浏览器
browser = webdriver.Chrome()

# 1.2. 无界面的浏览器
'''
option = webdriver.ChromeOptions()
option.add_argument("headless")
browser = webdriver.Chrome(options=option)
'''

# 指定绝对路径的方式
path = r"D:\Install\App\Google安装\chromedriver.exe"
browser = webdriver.Chrome(path)

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

### logo = browser.find_element(By.ID,'kw')

获取：`logo = browser.find_element_by_class_name('index-logo-src')`

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



### 下拉框

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



## 模拟鼠标操作

既然是模拟浏览器操作，自然也就需要能模拟鼠标的一些操作了，这里需要导入`ActionChains` 类。

```python
from selenium.webdriver.common.action_chains import ActionChains
```

1. `click()`：左键

2. `context_click()`：右键

   - 

   eg：

   ```text
   # 定位到要右击的元素，这里选的新闻链接
   right_click = browser.find_element_by_link_text('新闻')
   
   # 执行鼠标右键操作
   ActionChains(browser).context_click(right_click).perform()
   ```

`ActionChains(browser)`：调用`ActionChains()`类，并将浏览器驱动`browser`作为参数传入

`context_click(right_click)`：模拟鼠标双击，需要传入指定元素定位作为参数

`perform()`：执行`ActionChains()`中储存的所有操作，可以看做是执行之前一系列的操作

3. `double_click()`：双击

   ```python
   # 定位到要双击的元素
   double_click = browser.find_element_by_css_selector('#bottom_layer > div > p:nth-child(8) > span')
   
   # 双击
   ActionChains(browser).double_click(double_click).perform()
   ```

4. `drag_and_drop(source,target)`：拖拽。开始位置和结束位置需要被指定，这个常用于滑块类验证码的操作之类。