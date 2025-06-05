## Scrapy爬虫框架

1 Scrapy是什么



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

   

4 Scrapy项目的部署

5 分布式Scrapy爬虫 