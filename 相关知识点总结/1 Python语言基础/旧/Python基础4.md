**可变和不可变**

- 对象：内存地址，数据类型，值

- 可变

  - 当值发生改变时，内存地址不发生改变
  - 列表，字典，集合

- 不可变

  - 当值发生改变时，内存地址发生改变

- 引用不可变对象：首先寻找该对象是否被创建过，创建过了就直接引用，不会开辟新的内存空间

- 引用可变对象，会创建新的内存地址，值发生改变的时候，原内存地址不会发生改变

- id函数：查看对象的内存地址

- zip函数：将多个可迭代对象（如列表、元组、字符串等）打包成一个个元组

  ```python
  # 不可变对象，值相同，内存地址相同，当值发生改变时，内存地址发生改变
  a = 10
  b = 10
  print(id(a), id(b))
  b = 1
  print(id(a), id(b))
  
  # 可变对象，值相同时，内存地址不相同，当值发生改变时，内存地址不发生改变，重新赋值地址发生改变
  l1 = [1, 2, 3]
  l2 = [1, 2, 3]
  print(id(l1), id(l2))
  # l2.append(4)
  print(id(l1), id(l2))
  
  # 可变对象赋值的时候会开辟一块新的内存地址空间，但是l2 == l1这样赋值是指向同一块内存地址空间
  l1 = [1, 2, 3, 4]
  l2 = l1 # 指向同一个可变对象
  print(l1, l2, id(l1), id(l2))
  
  l1 = [1, 2, 3, 4]
  l2 = [1, 2, 3, 4]
  print(l1, l2, id(l1), id(l2))
  ```

**函数**

一段组织好了的，可以重复使用的，用来实现单一或者相关联功能的代码

- 内建函数

  - python内置的函数

- 用户自定义函数

  - 语法

    ```python
    def 函数的标识符(参数):
    	函数体
    	可省略的return
    ```

  - 说明

    - def关键字开头，后接函数的标识符，即函数名，再接圆括号，括号内放参数，最后接冒号和函数体以及可以省略的return，注意缩进
    - 函数的说明文档三对双引号或者三对单引号放在函数体的最前方

- 函数的参数

  - 必选参数/位置参数

  - 默认参数

  - 可变参数

  - 关键字参数以及可变长度关键字参数

  - 命名关键字参数

  - 强制位置参数

    ```python
    # 必选参数/位置参数/必需参数：按照位置顺序传值
    def add1(a, b):
        return a + b
    
    result = add1(1, 2)
    print(result)
    
    # 默认参数：形参优先级低于实参，可以不用传值
    def add2(a, b = 2):
        return a + b
    
    result1 = add2(1, 1)
    result2 = add2(1)
    print(result1, result2)
    
    # 可变长度参数：*加参数名（一般是*args），表示可变长度参数，以tuple形式存放数据
    def info(name, *args):
        print(type(args))
        return f'我的名字叫{name}，{args}'
    
    result3 = info('CR', '我今年18岁了','我要天天开心')
    print(result3)
    
    # 关键字参数：通过参数名 = 值来进行传参
    # 可变长度关键字参数：**加参数名（一般是**kwargs），表示关键字参数，以dict形式存放数据
    def info(name, **kwargs):
        print(type(kwargs))
        return f'我的名字叫{name}，{kwargs}'
    
    result4 = info('CR', age = 18, other = '天天开心')
    print(result4)
    
    # 命名关键字参数，*后面的参数必须通过命名传参
    def info(name, age, *, wish):
        print(name, age, wish)
        
    info('CR', 18, wish = '天天开心')
    
    # 强制位置参数，/前面的参数必须通过位置参数传递
    def info(name, age, /, *args):
        print(name, age, args)
    
    info('CR', 18, '开开心心', '平平安安')
    ```

**匿名函数**

- 举例说明

  ```python
  # 函数名 = lambda值1, 值2, 值3……:函数的逻辑
  add1 = lambda a, b: a + b
  print(add1(5, 6))
  ```

return语句

- 提供返回值

- 没有return或者return后面为None，则返回None

- 返回一个值时，外界接收到一个数据

- 返回多个值时，外界接收到一个打包好的元组数据

  ```python
  # 没有return或者return后面没有数据以及后面数据为空
  def add1():
      print('add1（）被调用了')
  
  print(add1())
  
  def add2():
      print('add2（）被调用了')
      return
  
  print(add2())
  
  def add3():
      print('add3（）被调用了')
      return None
  
  print(add3())
  
  # 返回一个值和多个值返回元组
  def add4():
      print('add4（）被调用了')
      return 1
  
  def add5():
      print('add5（）被调用了')
      return 1, 2, 3
  
  print(add4(), add5(), type(add4()), type(add5()))
  ```

**变量的作用域**

- 全局变量

- 局部变量

- global与nonlocal

  ```python
  # 全局变量与局部变量
  x = 10 # 全局变量
  def info():
      x = 20 # 局部变量
      print(20)
  
  info()
  print(x)
  
  # global在函数内部声明全局变量以及nonlocal（嵌套函数中使用）在外层函数声明外层函数的局部变量
  y = 10
  def info1():
      global y
      y = 20
      print(y)
  
  info1()
  print(y)
  
  def info1():
      x = 10
      def info2():
          nonlocal x
          x = 20
          print(x)
      info2()
      print(x)
  info1()
  ```

**递归函数**

- 函数自己调用自己

  ```python
  # 递归函数
  def story():
      print('从前有座山，山里有座庙，庙里有个老和尚在和小和尚讲故事，讲的什么呢，讲的')
      story()
  
  story()
  ```

- python中递归深度是有限的，如果递归深度过大会导致线程空间不足而崩溃

- 递归函数必须有明确的递归结束条件，称之为递归出口

- 查看和修改递归深度

  ```python
  # 查看递归深度
  def count1(n):
      try: # 可能会出现异常的代码块
          count1(n + 1)
      except:
          print(n)
  
  import sys
  print(sys.getrecursionlimit())
  
  count1(1) # 默认递归深度1000
  
  # 修改递归深度
  sys.setrecursionlimit(2000)
  print(sys.getrecursionlimit())
  count1(1)
  ```

**小案例**

```python
# 小案例1：递归之询问年龄
"""
    询问第n个人，他说比第n-1个人大两岁，询问第一个人，第一个人18岁，求第n个人的年龄，要求使用递归实现
    分析：
        n == 1时，age == 18
        n时，f（n） = f（n - 1）+ 2
"""

def age(n):
    if n == 1:
        return 18
    else:
        return age(n - 1) + 2

print(age(5))

# 小案例2：递归之斐波那契数列
"""
    斐波那契数列：从第三项开始，每一项都等于前两项之和，第一个和第二个数字通常是 0 和 1，或是 1 和 1，本题以0和1为例
    分析：
        n == 1时，result = 0
        n == 2时，result = 1
        n时，result = fib（n - 1） + fib（n - 2）
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
"""
def fib(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fib(n -1) + fib(n - 2)

for i in range(1, 11):
    print(fib(i))    
    
# 小案例3:递归之汉诺塔
"""
    汉诺塔：将不同大小的盘子从一个柱子移动到另一个柱子，每次只能移动一个盘子，并且较大的盘子不能放在较小的盘子上面。
    分析规则：
        n == 1时，A -> C
        n时：
            第一步：将n - 1个盘子从原柱子移到辅助柱子上
            第二步：将第n个盘子从原柱子上移动到目标柱子上
            第三步：将n-1个盘子从辅助柱子上移动到目标柱子上
    分析次数：
        递归公式：T(n)=2T(n − 1) + 1
        递归公式展开式：T(n)=2^n - 1
"""
def f(n):
    if n==0:
        return 0
    else:
        return 2*f(n-1)+1

def hnt(n, from_z, aux_z, to_z):
    if n == 1:
        print(from_z, ' -> ', to_z)  # 将最后一个盘子从源柱子移动到目标柱子
    else:
        # 第一步：将 n-1 个盘子从原柱子移到辅助柱子上
        hnt(n - 1, from_z, to_z, aux_z)

        # 第二步：将第 n 个盘子从原柱子上移动到目标柱子上
        print(from_z, ' -> ', to_z)

        # 第三步：将 n-1 个盘子从辅助柱子上移动到目标柱子上
        hnt(n - 1, aux_z, from_z, to_z)


# 测试函数，假设有 3 个盘子，起始柱子为 A，辅助柱子为 B，目标柱子为 C
hnt(3, 'A', 'B', 'C')
print(f(3))    
```



