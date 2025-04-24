**序列化和反序列化**

- 序列化：对象 -> 可以传输的字节

- 反序列化：可以传输的字节 -> 对象

- 序列化的作用：

  - 方便网络传输
  - 方便协议解释
  - 方便数据存储

- python中提供了两种序列化的模块

  - pickle：是python语言特定的序列化模块

  - json：支持多种编程语言

    ```python
    # pickle模块实现序列化和反序列化
    import pickle
    
    # 创建一个字典对象
    d = dict(name = 'CR ', age = 23, city = 'Chengde')
    
    with open(r'..\文件\test.data', 'wb') as f:
        pickle.dump(d, f)
    
    with open(r'..\文件\test.data', 'rb') as f:
        p = pickle.load(f)
        print(type(p), p)
    
    print(pickle.dumps(d)) # 返回的是一个 字节串（bytes）对象
    print(pickle.loads(pickle.dumps(d)))
    
    # json模块实现序列化和反序列化
    import json
    
    d = dict(name = 'CR ', age = 23, city = 'Chengde')
    
    print(json.dumps(d)) # json.dumps() 返回的是 JSON 格式的字符串
    print(json.loads(json.dumps(d)))
    
    f = open(r'..\文件\demo01.data', 'w')
    json.dump(d, f)
    f.close()
    f1 = open(r'..\文件\demo01.data', 'r')
    print(json.load(f1))
    ```

**面向对象：**一种针对大型软件程序的编程思想

- 特点：
  - 拓展性好，可读性好
  - 将数据和方法全部封装到对象中
  - 组织代码更接近人的思维
- 面向对象与面向过程
  - 区别：
    - 面向过程：
      1. 执行者思维：适合编写小型程序
      2. 按照一定的步骤，一步一步的执行
    - 面向对象：
      1. 设计者思维：适合编写大型程序
      2. 更加关注对象之间的关系
  - 相同点：
    1. 都是用来解决问题的思维方式
    2. 都是代码的组织方式
  - 选择：宏观选择面向对象，微观选择面向过程

- 面向对象三要素
  1. 封装
     - 组装：将数据和操作，及属性和方法组装到一起（放到同一个类中）
     - 隐藏数据：对象只暴露了一些接口，通过接口访问对象
  2. 继承
     - 子类继承父类后就拥有父类的所有公开的属性和方法
     - 多复用，继承下来的就不需要自己写了
     - 多继承，少修改，ocp（开-闭原则）即对拓展开放，对修改关闭
  3. 多态
     - 一个类可以拥有多个形态

- 类与对象的定义

  ```python
  # 雷鸣遵守大驼峰命名法
  class Washer():
      def behavior(self):
          print('洗衣服')
  
  haier = Washer()
  haier.behavior()
  ```

- 添加和获取对象的属性

  ```python
  class Washer():
      def print_info(self):
          print(f'宽{haier2.width}cm, 高{haier2.height}cm')
  # 类外添加属性和获取属性
  haier1 = Washer()
  haier1.haier = 'haier1'
  print(haier1.haier)
  
  # 类内添加和获取属性
  haier2 = Washer()
  haier2.width = 600
  haier2.height = 800
  haier2.print_info()
  ```

- 魔法方法

  ```python
  # 在python中__xx__()的函数叫做魔法方法，是具有特殊功能的函数
  # 1.__init__(self):初始化方法
  # 2.__str__():当使用print输出对象的时候，返回的是对象的内存地址，但是使用这个魔法方法后，输出的是该方法返回的数据
  # 3.__del__():当删除对象的时候，python解释器会默认调用这个方法
  
  class Washer():
      def __init__(self, width, height):
          self.width = width
          self.height = height
      def print_info(self):
          print('Washer: Width: {}, Height: {}'.format(str(self.width), str(self.height)))
      def __str__(self):
          return f'Washer: Width: {self.width}, Height: {self.height}'
      def __del__(self):
          print('Washer: Deleting Washer')
  
  washer = Washer(500, 1000)
  washer.print_info() # 初始化方法
  print(washer) # __str__(self)输出对象的的时候输出该对象该方法返回的值
  del washer # 删除对象调用__del__(self)方法
  ```

  **迭代器和生成器**

  迭代器：是一个可以记住遍历位置的对象，迭代器从第一个元素开始访问直到所有元素被访问完结束，迭代器只能往前，不能后退

  - 迭代器有两个方法：

    ```python
    # 1.iter()方法：返回迭代对象本身，将可迭代对象转换为一个迭代器
    # 2.next()方法：返回容器的下一个元素，当所有元素都访问完的时候，抛出异常
    # 定义一个迭代器
    
    str1 = 'CRHappyEveryDay'
    iterator = iter(str1)
    while True:
        try:
            el = next(iterator)
            print(el)
        except StopIteration as s:
            print('StopIteration')
            break
    ```

  - 判断是否是可迭代对象

    ```python
    # 判断一个对象是否可迭代
    from collections.abc import Iterable
    
    my_list = [1,2,3]
    my_string = 'hello'
    my_int = 1234
    
    print(isinstance(my_list,Iterable))
    print(isinstance(my_string,Iterable))
    print(isinstance(my_int,Iterable))
    ```

    生成器 generators **：**

    ```python
    # 生成器是一种特殊的迭代器，使用 yield 来生成值，它比普通的迭代器更高效、节省内存，适用于需要惰性计算或处理大数据的场景
    
    def my_generator():
        yield 1
        yield 2
        yield 3
        yield 4
        yield 5
    
    for i in my_generator():
        print(i)
    ```

**小案例**

```python
"""
    小案例1：用类优化收银系统
    分析:
        1.商品类(Good()):
            属性:good_name, good_prince, good_number
        2.收银员类(Cashier()):
            属性:shopping_car[good_name, good_prince, good_number]
            方法:添加(creat), 查找(read), 删除(delete), 结算(print_info)
        3.先从数据库中拿到商品菜单
"""

# 导入mysql.connector模块实现数据库相关操作
import mysql.connector

class Good():
    def __init__(self, good_name, good_prince, good_number):
        self.good_name = good_name
        self.good_prince = good_prince
        self.good_number = good_number
    def __str__(self):
        return f'{self.good_name}, {self.good_prince}, {self.good_number}'

class Cashier():
    def __init__(self):
        self.shopping_car = []

    def read(self):
        for i in self.shopping_car:
            print(i)
            print(f'good_name:{i.good_name}, good_prince:{i.good_prince}, good_number:{i.good_number}')

    def delete(self, good_name):
        for i in self.shopping_car:
            if i.good_name == good_name:
                self.shopping_car.remove(i)
                print('商品移除成功')
                return
        print('输入有误')

    def print_info(self):
        count = 0
        for i in self.shopping_car:
            count += i.good_prince * i.good_number
            print(f'good_name:{i.good_name}, good_prince:{i.good_prince}, good_number:{i.good_number}, 单个商品总价:{i.good_prince * i.good_number}')
        print('您一共消费{}元'.format(count))

cashier = Cashier()

while True:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='123456',
        database='scr'
    )

    cur = conn.cursor()

    cur.execute('select * from goods')

    rows = cur.fetchall()

    print('*' * 20 + '收银系统' + '*' * 20)
    for i in reversed(rows):
        print(i[0], i[1], i[2])
    str1 = input('请输入您的选择(r查看购物车, d删除商品, p结算):')

    if str1.isdigit():
        num1 = int(str1)
        if num1 <= 0 or num1 > 5:
            print('输入数据不合法')
            continue
    elif str1 == 'r':
        cashier.read()
        continue
    elif str1 == 'd':
        str2 = input('请输入您要删除的商品名字:')
        cashier.delete(str2)
        continue
    elif str1 == 'p':
        cashier.print_info()
        break
    else:
        print('输入数据不合法')
        continue

    for i in reversed(rows):
        if i[0] == num1:
            number = input('请输入商品数量:')
            if not number.isdigit():
                print('输入有误')
                continue
            good = Good(i[1], i[2], number)
            cashier.shopping_car.append(Good(i[1], int(i[2]), int(number)))
            
"""
    小案例2：用类实现学生管理系统
    分析：
        1.学生类（Student()）：
            属性：学号，姓名，电话号
        2.学生管理类（StuManagement()）:
            属性：学生信息表（stu_info = []）
            方法：c（添加学生），ro（按照学号查询学生信息），ra（查找所有学生），u（按照学号更新学生信息），d（按照学号删除学生）
"""

class Student(object):
    def __init__(self, stu_id, stu_name, stu_phone):
        self.stu_id = stu_id
        self.stu_name = stu_name
        self.stu_phone = stu_phone

    def __str__(self):
        return f'学号：{self.stu_id}, 姓名：{self.stu_name}, 手机号：{self.stu_phone}'

class StuManagement(object):

    def __init__(self):
        self.stu_info = []

    def create(self, student):
        for i in self.stu_info:
            if i.stu_id == student.stu_id:
                print('学号不能相同，添加失败')
                return
        self.stu_info.append(student)
        print('学生信息添加成功')

    def read_one(self):
        str1 = input('请输入您要查询学生的学号：')
        if not str1.isdigit():
            print('输入数据不合法')
            return
        for i in self.stu_info:
            if i.stu_id == str1:
                print(i)
                return
        print('请检查输入学号是否正确')

    def read_all(self):
        for i in self.stu_info:
            print(i)

    def update(self):
        str1 = input('请输入您要修改学生的学号：')
        if not str1.isdigit():
            print('输入数据不合法')
            return
        for i in self.stu_info:
            if i.stu_id == str1:
                self.stu_info.remove(i)
                str2 = input('请输入学生的姓名：')
                str3 = input('请输入学生的手机号：')
                if not str3.isdigit():
                    print('输入信息有误，程序异常退出')
                    return
        student = Student(str1, str2, str3)
        self.stu_info.append(student)
        print('学生信息修改成功')

    def delete(self):
        str1 = input('请输入您要删除学生的学号：')
        if not str1.isdigit():
            print('输入数据不合法')
            return
        for i in self.stu_info:
            if i.stu_id == str1:
                self.stu_info.remove(i)
                print('移除成功')
                return
        print('请检查输入学号是否正确')

if __name__ == '__main__':

    stu_management = StuManagement()

    while True:
        list1 = ['c', 'ro', 'ra', 'u', 'd', 'q']
        list2 = ['添加学生信息', '按照学号查询学生信息', '查询所有学生信息', '按照学号修改学生信息', '按照学号删除学生信息', '退出系统']
        print('*' * 15 + '学生管理系统' + '*' * 15)
        for i, j in zip(list1, list2):
            print(i, j)
        str1 = input('请输入您的操作：')
        if str1 == 'c':
            str2 = input('请输入要添加学生的学号：')
            str3 = input('请输入要添加学生的姓名：')
            str4 = input('请输入要添加学生的手机号：')
            if not (str2.isdigit() and str4.isdigit()):
                print('输入数据不合法')
                continue
            student = Student(str2, str3, str4)
            stu_management.create(student)
        elif str1 == 'ro':
            stu_management.read_one()
        elif str1 == 'ra':
            print('学生信息表如下')
            stu_management.read_all()
        elif str1 == 'u':
            stu_management.update()
        elif str1 == 'd':
            stu_management.delete()
        elif str1 == 'q':
            print('学生信息表如下')
            stu_management.read_all()
            break
        else:
            print('输入信息有误')
            
"""
    小案例3：用类实现简易版pugb
    分析：
        1.玩家类（player）：
            属性：血条（lifebar）， 武器/伤害（weapon/damage）：空手基础伤害0 + 随机伤害
            方法：攻击（attack()）
"""
import random

class Player():

    def __init__(self, name, lifebar):
        self.name = name
        self.lifebar = lifebar
        self.damage = random.randint(1, 50)

    def weapon(self, weapon = None):
        if weapon == 'AK-47':
            self.damage += 15
        elif weapon == 'm416':
            self.damage += 10
        elif weapon is None:
            pass
        else:
            pass

    def attack(self, player):
        player.lifebar -= self.damage
        print(
            f'玩家{self.name}攻击了玩家{player.name}，玩家{player.name}受到了{self.damage}点伤害，剩余血量：{player.lifebar}')
        if player.lifebar <= 0:
            print(f'玩家{player.name}被击败！')
            return True
        return False


if __name__ == '__main__':
    Flag = True
    fdm = Player('fdm', 100)
    ll = Player('ll', 100)
    fdm.weapon('AK-47')
    ll.weapon('m416')

    while fdm.lifebar > 0 and ll.lifebar > 0:
        if fdm.attack(ll):
            break
        if ll.attack(fdm):
            break
```

