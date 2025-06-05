## Scrapy爬虫框架

### 1 Scrapy是什么

Scrapy 是一个用 Python 编写的高性能 Web 爬虫框架，专为抓取网站数据并提取结构化信息而设计。它基于异步网络库 Twisted，具备请求调度、页面下载、数据提取、数据存储等完整流程，支持模块化开发，适合构建大型、可扩展的数据采集项目。

### 2 Scrapy的工作流程

![image-20250519082231173](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250519082231173.png)

- 相关部件说明：

  1. Engine（引擎）：管理所有部件的数据流转，控制整个爬虫的调度流程
  2. Schedule（调度器）:管理Request队列
  3. Downloader（下载器）：执行请求
  4. Spider（爬虫）：提供Request，解析Response
  5. Pipline（管道）：处理并持久化数据
  6. Downloader Middlewares（下载器中间件）：Request/Response的拦截器
  7. Spider Middlewares（爬虫中间件）：Spider输入输出的拦截器
  8. Item（数据结构）：存储爬取数据的容器

- 工作流程介绍：

  1. Spider将初始Request发送给Engine

  2. Engine接收Request并将其发送给Schedule入队

  3. Engine将一个Request出队交给Engine

  4. Engine将Schedule出队的Request发送给Downloader Middlewares

  5. Downloader Middlewares将Request传给Downloader

  6. Downloder向Internet发送Request并接收来自Internet的Response

  7. Downloader将Response发送给Downloader Middlewares

  8. Downloader Middlewares将接收到的Response发送给Engine

  9. Engine将Response发送给Spider Middlewares

  10. Spider Middlewares将Response发送给Spider

      情况1：Item

  11. Spider将Item发送给Spider Middlewares

  12. Spider Middlewares将Item发送给Pipline

      情况2：Request

      - 11+12：Spider将Request发送给Engine

  13. Engine将Item发送给Pipline



### 3 Scrapy项目的创建

1. 安装scrapy包

   ```cmd
   pip install scrapy
   ```

2. 创建Scrapy项目

   ```cmd
   scrapy startproject 【项目名】
   ```

3. 创建爬虫

   - 基础爬虫（base）

     ```cmd
     scrapy genspider 【爬虫名】 【允许的域名】
     ```

   - 使用模板

     - 查看爬虫模板

       ```cmd
       genspider -t
       ```

     - 指定模板

       ```cmd
       scrapy genspider -t 模板 【爬虫名】 【允许的域名】
       ```

       - 例如

         ```cmd
         scrapy genspider -t crawl【爬虫名】 【允许的域名】
         ```

   - 运行Scrapy爬虫

     - 直接运行

       ```cmd
       scrapy crawl 【爬虫名】
       ```

     - 保存结果为json格式

       ```cmd
       scrapy crawl 【爬虫名】 -o result.json
       ```

     - 可以在这个项目中新建run.py，然后运行run_more.py（思路：多进程）

       ```python
       from scrapy.cmdline import execute
       
       execute(['scrapy','crawl','[爬虫名]'])
       ```

4 Scrapy项目的部署

5 分布式Scrapy爬虫 