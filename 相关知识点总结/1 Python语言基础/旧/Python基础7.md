**面向对象-继承**

- 继承的基本概念

  - 多个类之间的所属关系，子类（衍生类，派生类）继承父类（基类）的属性和方法，就无需重写了

- 单继承

  ```python
  class Master():
      def __init__(self):
          self.kongfu = '天罡三十六变'
  
      def skill(self):
          print(f'使用{self.kongfu}')
  
  class Prentice(Master):
      pass
  
  prentice = Prentice()
  # 继承父类的属性
  print(prentice.kongfu)
  # 继承父类的方法
  prentice.skill()
  ```

- 多继承

  - 多继承时，父类具有相同的属性名或者方法名的时候，子类优先继承前面的父类的属性名或者方法名

  ```python
  class Master_one():
      def __init__(self):
          self.kongfu = '天罡三十六变'
  
      def skill(self):
          print(f'使用{self.kongfu}')
  
  class Master_two():
      def __init__(self):
          self.kongfu = '火眼金睛'
  
      def skill(self):
          print(f'使用{self.kongfu}')
  
      def skill1(self):
          print(f'使用火眼金睛')
  class Prentice(Master_one, Master_two):
      pass
  
  prentice = Prentice()
  print(prentice.kongfu)
  prentice.skill()
  prentice.skill1()
  ```

- 方法重写

  - 子类重写与父类同名的属性和方法

    ```python
    class Master():
        def __init__(self, str1):
            self.kongfu1 = str1
    
        def skill(self):
            print(f'使用{self.kongfu1}')
    
        def skill1(self):
            print(f'使用火眼金睛')
    
    class Prentice(Master):
        def __init__(self, str1):
            super().__init__(str1) # 通过super()调用父类的构造方法实现属性注入
            self.kongfu2 = '火眼金睛'
        def skill(self):
            super().skill1() # 调用父类的方法
            print(f'{self.kongfu1}和{self.kongfu2}太厉害了') # 调用父类的属性和自己的属性
    
    
    str1 = '天罡三十六变'
    
    prentice = Prentice(str1)
    prentice.skill()
    ```

- 私有属性和私有方法

  - 设置私有权限的方法：在属性或者方法前面加上两个下划线__

  - 私有方法和私有属性类外和子类不能访问，但仍有方法可以访问私有方法和私有属性，_A__属性名（/方法（））

    ```python
    class Master():
        def __init__(self):
            self.__kongfu = '天罡三十六变'
    
        def __skill(self):
            print(f'使用{self.__kongfu}')
    
    master = Master()
    print(master._Master__kongfu)
    master._Master__skill()
    
    class Prentice(Master):
        def print_info(self):
            print(self._Master__kongfu)
            self._Master__skill()
    
    prentice = Prentice()
    prentice.print_info()
    ```

- 获取和修改私有属性值

  - 通过setter修改器和getter获取器来修改和获取私有属性

    ```python
    class Master():
        def __init__(self):
            # 私有属性
            self.__kongfu = '天罡三十六变'
        
        # 私有方法
        def __skill(self):
            print(f'使用{self.__kongfu}')
        # 通过setter修改器，修改私有属性
        def set_kongfu(self, kongfu):
            self.__kongfu = kongfu
        # 通过getter获取器，获取私有属性
        def get_kongfu(self):
            return self.__kongfu
        # 通过use_private_method()访问私有方法
        def use_private_method(self):
            self.__skill()
    
    master = Master()
    master.set_kongfu('火眼金睛')
    print(master.get_kongfu())
    master.use_private_method()
    ```



**面向对象-多态**

- 多态的概念：一类事物有多种形态

  ```python
  class Animal():
      def behavior(self):
          print('所有动物都会移动')
  
  class Dog(Animal):
      def behavior(self):
          super().behavior()
          print('狗会跑')
  
  class Bird(Animal):
      def behavior(self):
          super().behavior()
          print('鸟会飞')
  
  class Caller():
      def observe(self, animal):
          animal.behavior()
  
  dog = Dog()
  bird = Bird()
  caller = Caller()
  caller.observe(dog)
  caller.observe(bird)
  
  # 不用调用者，直接写一个方法也能实现多态
  ```

- 类属性和实例属性

  - 类属性的获取可以通过类对象和实例对象
  - 但是类属性的修改只能通过类属性

  ```python
  class Dog(object):
      age = 10 # 类属性
  
  wangcai = Dog()
  xiaohei = Dog()
  
  print(Dog.age)  #　类对象访问类属性
  print(wangcai.age) # 实例对象访问类属性
  print(xiaohei.age) # 实例对象访问类属性
  
  wangcai.age = 20 # 实例对象不能修改类属性，他只是添加了一个新的实例属性（产生的效果，自己的那个类属性好像修改了）
  Dog.age = 30 # 类对象修改类属性
  
  print(Dog.age)
  print(wangcai.age)
  print(xiaohei.age)
  
  """
      类属性的优点：
          1.记录的某项数据始终不变的时候，可以定义类属性
          2.实例属性要求每个对象为其开辟一份内存空间来记录数据，而类属性为全类所有，仅占用一份内存，更加节省内存空间
  """
  ```

- 类方法

  ```python
  class Person:
      population = 0  # 类变量
  
      def __init__(self, name):
          self.name = name
          Person.population += 1 # 每实例化一次对象，类变量加一
  
      # 类方法，类方法用@classmethod注解修饰，（cls类本身）
      @classmethod
      def get_population(cls):
          return cls.population  # 访问类变量
  
  # 使用类方法
  print(Person.get_population())  # 调用类方法的方式，输出: 0
  p1 = Person("Alice")
  p2 = Person("Bob")
  print(Person.get_population())  # 输出: 2
  ```

- 静态方法

  ```python
  class Calculator:
      # 静态方法，静态方法用@staticmethod注解修饰，（）里面没有self或者self
      @staticmethod
      def add(a, b):
          return a + b
  
      @staticmethod
      def subtract(a, b):
          return a - b
  
  # 使用静态方法，通过类名调用
  print(Calculator.add(3, 5))  # 输出: 8
  print(Calculator.subtract(10, 4))  # 输出: 6
  ```

- property装饰器

  ```python
  # 通过 @property 可以将方法变成“属性”，让调用者像访问属性一样访问这些方法。
  class Dog():
      def __init__(self):
          self.__name = 'dog'
          self.__age = 3
  
      @property # 将方法封装成属性
      def name(self):
          return self.__name
  
      @property
      def age(self):
          return self.__age
      # 将方法封装成属性后，才能用@方法名.setter(或者getter)
      # 方法名必须与@property下的方法名相同，这样才能将他们关联起来
      @age.setter
      def age(self, age):
          if age <= 0:
              raise ValueError("年龄小于等于0，你在开玩笑吧？")
          else:
              self.__age = age
  
      @age.getter
      def age(self):
          return self.__age
  
  dog = Dog()
  print(dog.name)
  print(dog.age)
  dog.age = 20
  print(dog.age)
  ```



**推导式**

- 列表推导式

- 字典推导式

- 集合推导式

  ```python
  # 列表推导式
  # 生成0-10的列表
  list1 = [i for i in range(11)]
  print(list1)
  
  # 生成0-10中的偶数的列表
  list2 = [i for i in range(11) if i % 2 == 0]
  list3 = [i for i in range(11)[::2]]
  print(list2)
  print(list3)
  
  # 不知道怎么说，反正就生成下面这个东西
  list4 = [(i,j) for i in range(1,3) for j in range(3)]
  print(list4)
  
  # 字典推导式
  list5 = [i for i in range(11)]
  list6 = [i for i in range(11)[::-1]]
  dict1 = {list5[i]:list6[i] for i in range(len(list5))}
  dict2 = {i:j for i, j in zip(list5, list6)}
  print(dict1)
  print(dict2)
  
  # 集合推导式
  list7 = [i for i in range(10)]
  set1 = {i for i in list7}
  print(set1)
  ```



**补充**

- 魔法方法的调用：

  魔法方法一般自动调用，可是手动显示的调用

  ```python
  # 魔法方法的调用
  class Person():
      def __str__(self):
          return '人'
  
  p1 = Person()
  # 自动调用
  print(p1)
  
  # 手动显示的调用
  print(p1.__str__())
  ```

- 子类没有构造方法时会自动继承父类的构造方法，当子类有构造方法的时候可以通过super()调用

- **`not is`**：这种组合是不常见的，通常是 `not (a is b)`，用来反转身份比较的结果，检查两个对象是否 **不同**。

  **`is not`**：用于检查两个对象是否 **不相同**，即是否不指向同一个内存地址。

  **`in`**：用于判断一个元素是否 **在** 可迭代对象中。

  **`not in`**：用于判断一个元素是否 **不在** 可迭代对象中。