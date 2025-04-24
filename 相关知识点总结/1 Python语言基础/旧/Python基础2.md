Python基础数据类型

- 列表（list）

- 元组（tuple）

- 字典（dict）

- 集合（set）

- 对比

  - | 总结 |           list            |   tuple    |            dict            |           set           |
    | :--: | :-----------------------: | :--------: | :------------------------: | :---------------------: |
    | 说明 |           可变            |   不可变   | 可变（键必须是不可变元素） |          可变           |
    | 增加 | append  extend  insert  + |     +      |  dict1[xxx] = xxx  update  |           add           |
    | 删除 |  pop  remove  del  clear  |    del     |      pop  del  clear       | pop  remove  del  clear |
    | 修改 |        索引  切片         |            |  dict1[xxx] = xxx  update  |                         |
    | 查找 |        索引  切片         | 索引  切片 |  items(),keys(),values()   |                         |

- 补充

  1. 字符串转换为别的一般拆分
  2. append 整体加在末尾，extend挨个添加，insert按下标插入，+拼接 需要返回一个新的元素
  3. del可以按下标删除，可以按切片删除，可以删除整个，pop根据索引弹出数据，默认弹出最后一个元素，remove根据元素本身删除第一次出现的内容，元素不存在报错，clear清空
  4. index查找，找之前建议count一下
  5. 字典转成别的时候，一般是键

逻辑结构

- 顺序结构
- 分支结构
  - if
    - if 
    - if - else
    - if - elif - …… - else
    - if的嵌套使用（不建议）
  - mach - case（一般不用，if也可以实现同样效果）
- 循环结构
  - while循环
  - for循环
  - 关键字
    - continue 结束当此循环
    - break 结束当前循环
    - pass 跳过，什么都不执行

补充部分：

- len函数

- max，min函数 #abcdefghijklmnopqrstuvwxyz

- reverse逆序，sort排序

- copy浅拷贝

- 深浅拷贝的区别：

  - 浅拷贝：对于嵌套对象，只复制对象的引用
  - 深拷贝：递归的复制每个对象，创建一个独立的副本，修改拷贝前后的对象不会影响另一个对象

- operator模块中的函数：

  比较运算符：gt大于，ge大于等于，lt小于，le小于等于，eq等于，nq不等于

- 字符串进行index查找的时候建议先count一下，使用find查找不会报错，index查不到的时候会报错

  ```python
  s1 = 'hello'
  
  if s1.count('h'):
      print(s1.index('h'))
  ```

小案例：

```python
# 案例1：
"""
    for循环嵌套实现99乘法表
"""
for i in range(1, 10):
    print()
    for j in range(1, i + 1):
        print('{}x{}={}'.format(i, j, i * j), end=' ')
```

```python
# 案例2：
"""
    列表实现输入月份返回季节
"""

list1 = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]

while True:
    month_str = input('请输入月份（输入q退出）：')

    if month_str.isdigit():
        month = int(month_str)
    elif month_str == 'q':
        break
    else:
        print('输入数据不合法，请重新输入')
        continue

    if month in list1[0][0:3]:
        print('冬季')
    elif month in list1[0][0:3]:
        print('春季')
    elif month in list1[2][0:3]:
        print('夏季')
    elif month in list1[3][0:3]:
        print('秋季')
    else:
        print('输入数据不合法')
```

```python
# 案例3：
"""
    逻辑运算符实现输入月份返回季节
"""

while True:
    month_str = input('请输入月份（输入q退出）：')
    if month_str.isdigit():
        month = int(month_str)
    elif month_str == 'q':
        break
    else:
        print('输入数据不合法')
        continue
    if month > 0 and month <= 2 or month == 12:
        print('冬季')
    elif month >= 3 and month <= 5:
        print('春季')
    elif month >= 6 and month <= 8:
        print('夏季')
    elif month >= 9 and month <= 11:
        print('秋季')
    else:
        print('输入数据不合法')
```

