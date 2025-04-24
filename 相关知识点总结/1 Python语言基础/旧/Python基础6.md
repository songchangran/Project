作业1：多线程采集猫眼票房数据

```python
import re
import requests
import pandas as pd
from lxml import etree
from threading import Thread

urls = (f'https://movie.douban.com/top250?start={i}&filter=' for i in range(0, 250, 25))

headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}

movies_dict = {'电影名': [], '导演及主演': [], '评分': [], '评价人数': []}

def get_data(url):
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    movies = tree.xpath('//div/div[1]/ol')
    for movie in movies:
        titles = movie.xpath('./li/div/div[2]/div/a/span[1]/text()')
        dirs = movie.xpath('./li/div/div[2]/div[2]/p[1]/text()[1]')
        scores = movie.xpath('./li/div/div[2]/div[2]/div/span[2]/text()')
        pjs = movie.xpath('./li/div/div[2]/div[2]/div/span[4]/text()')
        movies_dict['电影名'].extend(titles)
        movies_dict['导演及主演'].extend(dirs)
        movies_dict['评分'].extend(scores)
        movies_dict['评价人数'].extend(pjs)
    pattern = re.compile(r'.*?start=(.*?)&filter.*?')
    ys = int(int(pattern.findall(url)[0])/25)
    print(f'第{ys}页采集完毕')

threads = []

for url in urls:
    t = Thread(target=get_data, args=(url,))
    t.start()
    threads.append(t)

for _ in threads:
    _.join()

pd.DataFrame(movies_dict).to_csv('./top250.csv',mode='a', index=False, encoding='utf-8')
```

运行结果：

![image-20250407112441167](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250407112441167.png)



### 多任务

- 让程序同时做多件事
- 实现多任务的三种方式：
  - 多线程：可以将一个程序分解成若干个独立的子任务
  - 多进程：可以同时执行多个程序
  - 协程：多个子任务并发的执行，从而缩短程序的执行时间



### 并行和并发

- 并发：在同一个时间段内，多个任务轮流执行（逻辑上同时发生，靠快速切换）

- 并行：在同一时间点，多个任务真正的同时执行（物理上同时发生）



### 进程和线程

- 进程：是程序运行的实例，拥有独立的内存空间和资源

- 线程：是进程中的执行单元，多个线程共享进程的资源

- 关系：

  - 一个进程至少有一个线程，线程是进程的一部分，所以线程也被称为轻量级的进程

  - 进程是容器，线程是内容物
  - 最少配比：一个进程至少有一个线程
  - 资源共享：同一进程内的线程共享资源
  - 通信方式：进程之间通信复杂（IPC），线程通信更容易

- 区别：

  - 进程是操作系统资源分配的基本单位，线程是处理器任务调度和执行的基本单位



### 线程的状态

- 就绪状态：程序能够运行了，但是正在等待被调度

- 执行状态：程序正在运行
- 阻塞状态：线程等待外部时间的发生而无法执行
- 终止状态：线程完成了，结束了



### Python实现多线程

- 导包：from threading import Thread

- Thread类构造方法的参数：

  - target：目标函数，线程调用的对象
  - name：给线程起名字
  - args：以元组格式传递的参数
  - kwargs：以字典形式传递的参数
  - daemon：设置线程是否随着主线程的退出而退出

- 方法实现多线程：

  ```python
  import threading
  
  def fun1():
      for i in range(100):
          print('子线程', i)
  
  if __name__ == '__main__':
      t1 = threading.Thread(target=fun1) # 注意target这里，参数只写函数名，不加“()”
      t1.start()
      for i in range(100):
          print('主线程', i)
  ```

- 类实现多线程：

  ```python
  from threading import Thread
  
  class MyThread(Thread):
      def run(self):
          for i in range(10):
              print('子线程', i)
  
  if __name__ == '__main__':
      t = MyThread()
      t.start()
      for i in range(10):
          print(i)
  ```

  

### 主线程

- 主线程就是第一个启动的线程，在主线程中启动的线程都是该线程的子线程，而该线程是那些子线程的父线程

- daemon属性：可以设置子线程是否随着主线程结束而结束，默认false（不随着主线程的结束而结束）

  ```python
  from threading import Thread
  import time
  
  # def fun1():
  #     time.sleep(2)
  #     for i in range(10):
  #         print('子线程', i)
  
  class MyThread(Thread):
      def run(self):
          time.sleep(2)
          for i in range(10):
              print('子线程', i)
  
  if __name__ == '__main__':
      # t = Thread(target=fun1,daemon=True)
      t = MyThread(daemon=True)
      t.start()
      for i in range(10):
          print('主线程', i)
  ```

  

### 阻塞线程

- 线程因为等待某个条件（I/O，锁释放等）而暂停执行的状态
- join()：阻塞主线程，等待子线程执行完毕再继续执行主线程

```python
import time
from threading import Thread

def task(name):
    print(f'{name}:开始执行，即将阻塞3秒')
    time.sleep(3)
    print(f'{name}:阻塞结束，继续执行')

if __name__ == '__main__':
    t1 = Thread(target=task, args=('子线程1',))
    t2 = Thread(target=task, args=('子线程2',))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('主线程结束了')
```



### 锁（LOCK）

- 用来控制多个线程对共享资源的访问

- 使用锁的原因：线程安全问题（在多线程中，多个线程可能同时访问或修改同一个变量）

- Lock 用来保证：同一时间只有一个线程能访问关键代码区（临界区）

- 代码举例（100个人同时向一个人汇款一块钱）:

  ```python
  from threading import Thread, Lock
  
  class Account(object):
      def __init__(self):
          self._balance = 0
          self._lock = Lock()
  
      # 汇款方法
      def remittance(self, money):
          with self._lock:
              self._balance += money
          # self._lock.acquire()
          # try:
          #     self._balance += money
          # finally:
          #     self._lock.release()
  
      @property
      def balance(self):
          return self._balance  # 返回当前的余额
  
  class AddMoney(Thread):
      def __init__(self, money, account):
          super().__init__()
          self.account = account
          self.money = money
      def run(self):
          self.account.remittance(self.money)
  
  def main():
      account = Account()
      money = 1
      threads = []
      for _ in range(100):
          t = AddMoney(money,account)
          threads.append(t)
          t.start()
      for _ in threads:
          _.join()
  
      print(f'账户余额为{account.balance}')
  
  if __name__ == '__main__':
      main()
  ```

  



