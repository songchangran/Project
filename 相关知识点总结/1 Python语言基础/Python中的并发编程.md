## Python中的并发编程

### 进程、线程和协程的核心概念讲解

进程（Process）

- 概念：
  - 进程是操作系统分配资源的最小单位，是一个**独立运行中的程序实例**。

- 特点：
  - 每个进程有自己**独立的内存空间**。
  - 进程之间**不能直接共享数据**，要用进程通信（如管道、队列）。
  - 切换进程的成本**比较高**，但更**稳定**，不会互相影响。

- 理解：
  - 每个进程就像是一台独立的计算机在干活，彼此互不干扰。

线程（Thread）

- 概念：
  - 线程是程序执行的最小单位，是进程内部的一个**执行流**。

- 特点：
  - 多个线程**共享进程的内存资源**（共享数据、文件等）。
  - 切换速度比进程快，但线程之间可能会**互相影响**（需要锁来防止冲突）。
  - Python 有 **GIL（全局解释器锁）**，在某一时刻只能运行一个线程（影响多线程并行能力）。

- 理解：
  - 线程是进程内的“多个工人”在共享一个大桌子干活，他们可以合作也会抢资源。

协程（Coroutine）

- 概念：
  - 协程是一种用户级的轻量线程，由程序自身控制切换，适合处理**高并发 I/O 操作**。

- 特点：
  - 单线程下实现**高并发**。
  - 协程之间的切换**不需要操作系统介入**，效率极高。
  - 使用 `async/await` 实现异步任务的挂起与恢复。
  - 不适合 CPU 密集型任务。

- 理解：
  - 协程是“聪明的工人”，他做一点这个，再做一点那个，不耗时间，一心多用。



### 进程、线程和协程的简单对比

| 特性     | 进程               | 线程                 | 协程                     |
| -------- | ------------------ | -------------------- | ------------------------ |
| 内存空间 | 独立               | 共享（同一个进程内） | 共享（单线程中）         |
| 切换开销 | 高（系统级）       | 中等（系统级）       | 极低（用户级）           |
| 通信方式 | 进程间通信（复杂） | 共享变量（需加锁）   | 自由共享（较安全）       |
| 使用场景 | CPU 密集型任务     | I/O 密集型任务       | 高并发 I/O，任务切换频繁 |
| 并发方式 | 真正并行           | 有 GIL 限制          | 单线程并发               |



### 进程、线程和协程的应用场景

协程：搞爬虫、做API请求；
进程：跑数据计算；
线程：操作磁盘、读文件、下载。



### Python中的锁

- 核心概念

  - 在 Python 中，**锁**（Lock）是一个常用于 **多线程编程** 的机制，用来确保**多个线程**在访问共享资源时的 **互斥**。通过锁机制，**多个线程**可以安全地访问 **共享资源**，避免出现**数据竞争**和**线程冲突**。
  - Python 提供了多种锁的实现，最常用的是 **`threading.Lock`** 和 **`threading.RLock`**。

- **`threading.Lock`** 锁

  - 概念
    - **`threading.Lock`** 是 Python 中最简单的锁，它用于保护共享资源。在一个线程获取锁之后，其他线程需要等待锁被释放才能继续执行。
  - 特点
    - **互斥性**：同一时间只有一个线程可以获得锁。
    - **不可重入性**：同一线程不能多次获取同一个锁。
  - 代码示例

  ```python
  import threading
  
  # 创建一个锁
  lock = threading.Lock()
  
  counter = 0
  
  # 线程执行的任务
  def task():
      global counter
      for _ in range(1000000):
          # 获取锁
          lock.acquire()
          try:
              counter += 1  # 修改共享变量
          finally:
              lock.release()  # 释放锁
  
  # 创建并启动多个线程
  threads = []
  for _ in range(4):
      t = threading.Thread(target=task)
      t.start()
      threads.append(t)
  
  # 等待所有线程完成
  for t in threads:
      t.join()
  
  print("所有线程完成，counter:", counter)
  ```

- **`threading.RLock`**（可重入锁）

  - 核心概念
    - **`threading.RLock`** 是 Python 中的一种特殊类型的锁，它的特点是**可重入性**。也就是说，当一个线程已经获取了锁，它仍然可以再次获得锁，而不会被阻塞。

  - 作用

    - 普通的锁（如 **`Lock`**）在同一个线程中，如果它已经持有锁，再次尝试获取该锁时会发生 **死锁**，也就是线程会永远等待自己释放锁。而 **`RLock`** 解决了这个问题：同一线程可以多次获取锁，每次获取都必须释放对应次数的锁。

  - 特性

    - **可重入性**：同一线程可以多次获得锁而不会被阻塞。
    - **锁的计数**：每次获得锁，锁会记录获得的次数（`acquire()` 的次数），直到所有的 `release()` 调用完后，锁才会真正释放。

  - 代码示例

    ```python
    import threading
    
    # 创建可重入锁
    rlock = threading.RLock()
    
    def task():
        print("试图获取锁")
        rlock.acquire()  # 获取锁
        print("锁被获得")
        rlock.acquire()  # 再次获取锁（同一线程）
        print("再次获得锁")
        rlock.release()  # 释放锁
        rlock.release()  # 再次释放锁，锁最终被释放
    
    # 创建线程并运行
    t = threading.Thread(target=task)
    t.start()
    t.join()  # 等待线程完成
    ```

    

### Python中 的 GIL（全局解释器锁）

- 核心概念

  - GIL（Global Interpreter Lock，全局解释器锁）是  `CPython`（Python 默认实现）中一个线程互斥锁**，**保证同一时刻只有一个线程在执行 Python 字节码。

- `ps`

  - 同一时间只能有一个线程执行 Python 字节码
  - GIL 保证线程安全，但限制了多线程的并行能力

- 实现

  ```python
  import time
  import threading
  
  # 创建一个锁（模拟 GIL）
  gil = threading.Lock()
  
  # 全局变量
  counter = 0
  
  # 线程执行的任务
  def task(thread_id):
      global counter
      for _ in range(1000000):
          # 获取锁，模拟 GIL
          with gil:
              counter += 1
      print(f"线程 {thread_id} 完成!")
  
  # 创建并启动多个线程
  threads = []
  for i in range(4):
      t = threading.Thread(target=task, args=(i + 1,))
      t.start()
      threads.append(t)
  
  # 等待所有线程完成
  for t in threads:
      t.join()
  
  print("所有线程完成，counter:", counter)
  ```

  

### Python中并发编程的实现

- 多线程

  适合场景：IO 密集型任务（如：网络请求、磁盘读写），线程之间共享内存资源。

  ```python
  import threading
  import time
  
  def task(name):
      print(f"{name} 开始")
      time.sleep(2)
      print(f"{name} 结束")
  
  threads = []
  for i in range(5):
      t = threading.Thread(target=task, args=(f"线程{i+1}",))
      t.start()
      threads.append(t)
  
  for t in threads:
      t.join()
  
  print("所有线程完成")
  ```

- 多进程

  适合场景：CPU 密集型任务（如：大数据计算、图像处理），进程之间**不共享内存**，但更稳定。

  注意事项：在 **Windows** 中使用 **`multiprocessing`**（多进程）时，如果没有加上 **`if __name__ == '__main__'`**，会导致程序**无限创建新进程**，因为每个新进程都会重新执行整个脚本，导致进程不断启动。

  ```python
  import multiprocessing
  import time
  
  def task(name):
      print(f"{name} 开始")
      time.sleep(2)
      print(f"{name} 结束")
  
  if __name__ == '__main__':
      processes = []
      for i in range(5):
          p = multiprocessing.Process(target=task, args=(f"进程{i+1}",))
          p.start()
          processes.append(p)
  
      for p in processes:
          p.join()
  
      print("所有进程完成")
  ```

- 协程/异步编程

  适用场景：高并发、网络 IO 密集场景，如爬虫、API 并发请求。效率非常高，但编程模型略复杂。

  ```python
  import asyncio
  
  async def task(name):
      print(f"{name} 开始")
      await asyncio.sleep(2)
      print(f"{name} 结束")
  
  async def main():
      tasks = [task(f"协程{i+1}") for i in range(5)]
      await asyncio.gather(*tasks)
  
  asyncio.run(main())
  ```

- 线程池（`ThreadPool`）

  - **`max_workers`**：指定线程池中最多同时执行的线程数（默认值是系统核心数）。
  - **`timeout`**：指定任务最大执行时间，超时会抛出异常。
  - **`thread_name_prefix`**：指定线程名的前缀（可选）。
  - **`submit()`**：用于提交单个任务，返回一个 `Future` 对象。`Future` 对象可以用来获取任务的执行结果。
  - **`map()`**：用于提交多个任务，返回一个结果列表。

  ```python
  import concurrent.futures
  import time
  
  # 任务函数
  def task(n, delay):
      print(f"任务 {n} 开始，延迟 {delay} 秒")
      time.sleep(delay)
      print(f"任务 {n} 完成")
      return f"任务 {n} 的结果"
  
  # 使用线程池
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
      # 提交任务并传递参数
      futures = [executor.submit(task, i, i) for i in range(5)]
      
      # 获取任务执行结果
      for future in concurrent.futures.as_completed(futures):
          print(future.result())  # 打印任务返回的结果
  ```

  ```python
  # 使用map提交任务
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
      # 提交多个任务并传递参数
      results = list(executor.map(lambda n: task(n, n), range(5)))
      
  print("所有任务完成:", results)
  ```

- 进程池

  - **`max_workers`**：指定进程池中最多同时执行的进程数（默认值是系统核心数）。
  - **`timeout`**：指定任务最大执行时间，超时会抛出异常。
  - **`mp_context`**：指定进程池的上下文，可以选择使用 `fork`, `spawn`, 或 `forkserver`。
  - **`submit()`**：提交单个任务，返回一个 `Future` 对象，类似线程池的 `submit()`。
  - **`map()`**：提交多个任务，返回结果的列表（同步调用，阻塞直到完成）。

  ```python
  import concurrent.futures
  import time
  
  # 任务函数
  def task(n, delay):
      print(f"任务 {n} 开始，延迟 {delay} 秒")
      time.sleep(delay)
      print(f"任务 {n} 完成")
      return f"任务 {n} 的结果"
  
  # 使用进程池
  with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
      # 提交任务并传递参数
      futures = [executor.submit(task, i, i) for i in range(5)]
      
      # 获取任务执行结果
      for future in concurrent.futures.as_completed(futures):
          print(future.result())  # 打印任务返回的结果
  ```

  ```python
  # 使用map提交参数
  with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
      # 提交多个任务并传递参数
      results = list(executor.map(lambda n: task(n, n), range(5)))
      
  print("所有任务完成:", results)
  ```

  

