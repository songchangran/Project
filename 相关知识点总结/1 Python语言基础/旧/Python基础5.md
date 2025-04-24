**闭包**

通常在一个函数内部定义另一个函数，内部的这个函数就是闭包

实现闭包的条件：

- 嵌套函数

- 内部函数访问外部函数的变量或者参数

- 外部函数的返回值是内部函数

  ```python
  # 闭包
  # 嵌套函数
  def outer_function (text):
      def inner_function():
          print(text) # 内部函数调用外部函数的变量或者参数
      return inner_function() # 外部函数的返回值是内部函数
  
  outer_function('hello')
  
  # 内部函数记住了外部函数的作用域
  
  # 闭包的作用
  # 1.实现装饰器：装饰器是一种在不改变原来函数代码的情况下，为函数添加额外的功能。闭包可以用来是实现装饰器，将需要的功能封装到闭包函数中
  # 2.保护变量:闭包函数可以将变量封装起来,防止被外部的访问和修改
  # 3.实现回调函数:闭包函数可以作为参数传递给其他函数,在需要的时候被调用
  ```

**装饰器**

- 作用：在不改变原函数的情况下，给函数添加新的功能

  ```python
  def guanjia(game):
      print('开挂')
      game()
      print('关挂')
  
  def lol():
      print('面对疾风吧……')
  
  def pubg():
      print('大吉大利，今晚吃鸡！')
  
  guanjia(lol)
  guanjia(pubg)
  # 装饰器
  def lol():
      print('面对疾风吧……')
  
  def pubg():
      print('大吉大利，今晚吃鸡！')
  
  def gua(game):
      def inner():
          print('开挂')
          game()
          print('关挂')
      return inner()
  
  gua(lol)
  gua(pubg)
  
  # 注解实现装饰器
  def gua(game):
      def inner():
          print('开挂')
          game()
          print('关挂')
      return inner()
  
  @gua
  def lol():
      print('面对疾风吧……')
  
  @gua
  def pubg():
      print('大吉大利，今晚吃鸡！')
  ```

**异常**

- 错误：解释器或者编译器在解析代码时返回的一些问题，比如语法问题，拼写错误，缺少括号等等

- 异常：在程序运行过程中由于某种特定的情况导致程序无法正常继续执行时抛出的

- 在python中有一个内建的异常处理机制，允许用户在代码中指定某些可能会出现错误的代码块。并且在出现错误的时候会执行特定的代码

- 常见的异常

  - 除零异常，索引异常，键异常，类型异常，名称异常，值异常，文件不存在异常

    ```python
    # 常见的异常
    # 除零异常 ZeroDivisionError
    print(1 / 0)
    # 索引异常 IndexError
    list1 = [1, 2, 3]
    print(list1[3])
    # 键异常 KeyError
    dict1 = {'a':1, 'b':2, 'c':3, 'd':4}
    print(dict1['e'])
    # 类型异常 KeyError
    print(1 + 'hello')
    # 名称异常 KeyError
    name1 = 'CR'
    print(name2)
    # 值异常 ValueError
    str1 = 'hello'
    print(int(str1))
    # 文件不存在异常 FileNotFoundError
    with open('bucunzai.txt', 'r') as file:
        content = file.read()
        print(content)
    ```

**断言**

- 用于开发和测试阶段，确保代码能够按照预期的方式执行

- python中使用assert语句实现断言

- `assert` 语句是 Python 中的一种调试工具，用于测试表达式是否为 `True`。如果表达式为 `False`，程序会引发一个 `AssertionError` 异常，且可以附带错误消息

- isinstance：检查一个对象是否是指定类型或者其子类的实例

  ```python
  # 断言
  def add_nums(num1, num2):
      assert isinstance(num1, (int, float))
      assert isinstance(num2, (int, float))
      return num1 + num2
  
  try:
      print(add_nums(1, '2'))
  except:
      print('自定义断言异常')
  ```

  raise :用于显式的引发一个异常

  repr()  用于将异常e转换成字符串的表现形式，如果 `repr()` 返回的字符串是合法的 Python 表达式，则可以用 `eval()` 重建该对象

  ```python
  # raise
  try:
      num1 = input('请输入你的电话话码：')
      if not num1.isdigit():
          raise ValueError('电话号必须全是数字')
  except ValueError as e:
      print(repr(e))
  
  # repr
  num2 = 123
  print(type(repr(num2)), repr(num2))
  ```


文件操作

- 文件的打开和关闭

  ```python
  open(file='',mode='',encoding='')
  file: 文件的路径或名称
  mode:对文件的操作方式
  enconding:编码
      
  t:表示文本模式
  b:二进制模式
  ```

- 举例

  ```python
  # 文件的打开操作
  with open(file='../文件/demo.txt', mode='a+', encoding='utf-8') as f:
      f.write('你好\n')
      f.writelines('nihao')
      f.writelines(['1', '2'])
  
  f = open(r'C:\Users\31923\Desktop\PythonProjects\pythonProject01\文件\demo.txt', 'r+', encoding='utf-8')
  print(f.read())
  print(f.readline())
  print(f.readlines())
  print('-' * 20)
  
  list1 = f.readlines()
  str1 = '\n'.join(list1)
  print(str1)
  
  print(f.readline())
  print(f.readline())
  print(f.readline())
  print(f.readline())
  
  f.close()
  ```

- 总结

  - with open() as f：#`with` 语句可以自动管理文件的打开和关闭，这样即使在发生异常时，文件也会正确关闭，避免资源泄漏。
  - 不用with语句记得关闭文件，避免资源泄露
  - 文件读取：read,readline,readlines
  - 文件写入：write,writeline(没有writeline方法)
  - 文件权限：
    - r只读
    - w覆盖
    - a追加
    - 上述三个后面加上+，都是读写
    - b二进制，加在r,w,a后面，加在+前面
  - readline：一行一行的读

小案例:

```python
"""
    小案例1：用函数实现购物车,连接数据库实现登录
"""
import mysql.connector

# 定义菜单
goods = [['火腿',5],
         ['泡面',6],
         ['可乐',3],
         ['饼干',6],
         ['卫龙',4],
         ]

# 定义购物车
shopping_car = []
# flag
flag = 1

#　定义高亮显示的函数
def color(string,color='red'):
    color_dict = {
        'red':31,
        'green':32,
        'yellow':33,
        'blue':35
    }
    start = '\033[%dm' % color_dict[color]
    end = '\033[0m'
    return start+string+end

# 定义商品的函数
def menu():
    print(color('==========欢迎光临==========','yellow'))
    print(color('\t序号\t\t商品名\t\t单价\t'))
    # enumerate() 用于遍历序列中的元素以及下标
    for i,j in enumerate(goods):
        print(color(f'\t{i + 1}\t\t{j[0]}\t\t\t{j[1]}'))
    print(color('==========欢迎光临==========','yellow'))

# 定义购买函数
def buy_goods():
    num = input('请输入您的选择：')
    if num == 'q':
        print_result()
        flag = 0
        return
    elif num.isdigit():
        num = int(num)
        if 0 < num <= len(goods):
            num -= 1
        else:
            print(color('输入数据不合法', 'red'))
            return
    else:
        print(color('输入数据不合法', 'red'))
        return
    name = goods[num][0]
    price = goods[num][1]
    number = 1
    for i in shopping_car:
        if name == i[0]:
            number += i[2]
            shopping_car.remove(i)
    shopping_car.append([name,price,number])

def print_result():
    money = 0
    for i in shopping_car:
        money += i[1] * i[2]
        print(f'商品名：{i[0]}\t\t商品单价：{i[1]}\t\t商品份数：{i[2]}\t\t单个商品总价：{i[1] * i[2]}')
    print(f'您一共消费{money}元')

def dl():
    account = input('请输入用户名：')
    pwd = input('请输入密码：')
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='123456',
        database='scr'
    )

    cursor = conn.cursor()

    cursor.execute('select * from account')
    for i in cursor.fetchall():
        if i[1] == account and i[2] == pwd:
            print('登陆成功')
            return
    print(color('用户名或密码不正确', 'red'))
    dl()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    while flag:
        dl()
        menu()
        buy_goods()
```

