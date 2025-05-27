## 基本概念

html代码如下：

```html
<html>
<body>
<div id="one">
    <p class="p_cls" id="row1" data="a">第一行</p>
    <p class="p_cls" id="row2" data="b">第二行</p>
    <p class="p_cls">第三行</p>
</div>
<div id="two">
    第二个div
</div>
</body>
</html>
```

定位：

```python
tab.ele('@id=one')  # 获取第一个id为one的元素
tab.ele('@tag()=div')  # 获取第一个div元素
tab.ele('@text()=第一行')  # 获取第一个文本为“第一行”的元素
```

当需要多个条件同时确定一个元素时，每个属性用`'@@'`开头

```python
ele = tab.ele('@@class=p_cls@@text()=第三行')  # 查找class为p_cls且文本为“第三行”的元素
```

当需要以或关系条件查找元素时，每个属性用`'@|'`开头。

```python
eles = tab.eles('@|id=row1@|id=row2')  # 查找所有id为row1或id为row2的元素
```

如果`@!`后面只有属性名而没有属性值，查找没有这个属性的元素。

```python
ele = tab.ele('@!id=one')  # 获取第一个id等于“one”的元素
ele = tab.ele('@!class')  # 匹配没有class属性的元素
```

### 精确匹配

```python
ele = tab.ele('@id=row1')  # 获取id属性为'row1'的元素
```

### 模糊匹配

```python
ele = tab.ele('@id:ow')  # 获取id属性包含'ow'的元素
```

### 匹配开头

```python
ele = tab.ele('@id^row')  # 获取id属性以'row'开头的元素
```

### 匹配结尾 

```python
ele = tab.ele('@id$w1')  # 获取id属性以'w1'结尾的元素
```

### id 匹配符

```python
ele = tab.ele('#one')  # 查找id为one的元素
ele = tab.ele('#=one')  # 和上面一行一致
ele = tab.ele('#:ne')  # 查找id属性包含ne的元素
ele = tab.ele('#^on')  # 查找id属性以on开头的元素
ele = tab.ele('#$ne')  # 查找id属性以ne结尾的元素
```

### class 匹配符

```python
ele = tab.ele('.p_cls')  # 查找class属性为p_cls的元素
ele = tab.ele('.=p_cls')  # 与上一行一致
ele = tab.ele('.:_cls')  # 查找class属性包含_cls的元素
ele = tab.ele('.^p_')  # 查找class属性以p_开头的元素
ele = tab.ele('.$_cls')  # 查找class属性以_cls结尾的元素
```

### 文本匹配符

```python
ele = tab.ele('text=第二行')  # 查找文本为“第二行”的元素
ele = tab.ele('text:第二')  # 查找文本包含“第二”的元素
ele = tab.ele('第二')  # 与上一行一致
ele = tab.ele('第\u00A0二')  # 匹配包含&nbsp;文本的元素，需将&nbsp;转为\u00A0
```

### 类型匹配符 `tag`

```python
ele = tab.ele('tag:div')  # 查找第一个div元素
ele = tab.ele('tag:p@class=p_cls')  # 与单属性查找配合使用
ele = tab.ele('tag:p@@class=p_cls@@text()=第二行')  # 与多属性查找配合使用
```

### xpath 匹配符

```python
ele2 = ele1.ele('xpath:.//div')  # 查找后代中第一个 div 元素
ele2 = ele1.ele('xpath://div')  # 和上面一行一样，查找元素的后代时，// 前面的 . 可以省略
ele_class_str = ele1.ele('xpath://div/@class')  # 使用xpath获取div元素的class属性（页面元素无此功能）
```

### `ele()`

用于查找其内部第一个条件匹配的元素。

```python
from DrissionPage import SessionPage
from DrissionPage import ChromiumPage
page = SessionPage()
#page = ChromiumPage()
# 在页面内查找元素
ele1 = page.ele('#one')

# 在元素内查找后代元素
ele2 = ele1.ele('第二行')

```

这里强调一下SessionPage和ChromiumPage的区别，他们都能定位元素，但是

返回的东西不一样

也就是说SessionPage返回的是一个SessionElement，这个玩意可以继续用于定位其他元素，但是这个是一个静态的东西，不能用于点击等和页面进行交互的情况，也不能直接访问到iframe里面的元素

另一个则可以返回可以与页面继续进行交互的元素

第三是说如果定位的是个iframe元素会返回的东西

第四个是没定位到元素会返回什么，默认情况没定位到不会报错，会返回NoneElement，这个东西是假的，所以可以直接写if来进行是否定位到该元素的判断

```python
ele = tab.ele('****')

# 判断是否找到元素
if ele:
    print('找到了。')

if not ele:
    print('没有找到。')
```



```python
try:
    ele.click()
except ElementNotFoundError:
    print('没有找到。')
```

该方法三个参数，第一就是元素的定位信息，第二是获取第几个元素的序号，从1开始可以有-号进行倒数，第三就是超时时间，默认等待十秒（SessionPage无效）。

### `eles()`

这里提到

```python
loc 元组是指 selenium 定位符，例：(By.ID, '****')。下同。
ele('****', index=2)和eles('****')[1]结果一样，不过前者会快很多。
```

这里还提供一种静态方法

### `s_ele()`

### `s_eles()`

静态页面可以提高速度，但不方便进一步的交互

## `<iframe>`中查找

对于跨域名的iframe

虽然ele()可以定位到iframe,但不建议用，建议用get_frame()

```python
iframe = page.get_frame(1)  # 获取页面中第一个iframe元素
iframe = page.get_frame('#theFrame')  # 获取页面id为theFrame的iframe元素对象
```

还有一种写法

假设一个`<iframe>`的 id 为 `'iframe1'`，要在其中查找一个 id 为`'abc'`的元素：

```python
page = ChromiumPage()
iframe = page('#iframe1')
ele = iframe('#abc')
```

对于不跨域名的iframe,可以直接获取

```python
page = ChromiumPage()
ele = page('#abc')
```



# 简化写法

```python
# 查找tag为div的元素
ele = tab.ele('tag:div')  # 原写法
ele = tab('t:div')  # 简化写法

# 用xpath查找元素
ele = tab.ele('xpath://****')  # 原写法
ele = tab('x://****')  # 简化写法

# 查找text为'something'的元素
ele = tab.ele('text=something')  # 原写法
ele = tab('tx=something')  # 简化写法
```



# 获取元素信息

返回的三个属性就是我们经常用到的，html用于获取页面源码，text获取文本信息，attr()获取某个属性值

