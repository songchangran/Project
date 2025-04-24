**Xshell远程连接**

```shell
1.查看sshd服务是否开启
systemctl status sshd # 查看状态
systemctl start sshd # 启动服务
systemctl stop sshd # 停止服务
systemctl enable sshd # 开机自启
systemctl disable sshd # 永久关闭

2.查看本机IP地址
ifconfig/ip addr

3.在Xshell连接
```



**Vim文本文件编辑器**

1. 首行模式

   ```shell
   dd：删除光标所在行
   u：撤销操作
   yy：复制光标所在行
   nyy：n为数字
   p：粘贴光标的下一行
   ……
   ```

2. 编辑模式

   ```shell
   键入i：光标前输入内容
   键入a：光标后移一个字符输入内容
   键入o：新启一行输入内容
   ```

3. 末行模式

   ```shell
   :w			保存
   :wq			保存退出
   :q			退出
   :q!			强制退出
   :wq!		强制保存退出
   :set nu 	设置行号
   :set nonu	取消设置行号
   :/			向后搜索指定模式
   :?			向前搜索指定模式
   :noh		取消高亮
   :h			帮助
   ```

   

**Yum源**

Yum源是什么

- 配置yum源

  - 配置本地源

    ```shell
    1.创建本地源目录
    mkdir /media/cdrom
    2.挂载光盘镜像
    mount /dev/cdrom /media/cdrom
    3.备份
    mv CentOS-*.* bak/
    4.拷贝本地源目录
    cp bak/CentOS-Media.repo
    5.开启本地源目录
    vim CentOS-Media.repo
    enable=1
    ```

  - 配置网络源

    ```shell
    1.配置阿里云yum源
    wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
    2.生成缓存
    yum makecache
    ```

- yum源的切换

  ```shell
  mv CentOS-Media.repo CentOS-Media.repo1
  ```

- yum的常用命令

  ```shell
  1.安装
  yum -y install 包名
  2.升级
  yum -y update 包名 # 更新指定包
  yum upgrade # 更新所有包
  yum check-update # 检查可以更新的包
  3.查找
  yum info 包名 # 显示某个包的详细信息
  yum info # 显示所有安装的包的详细信息
  yum list # 显示软件包的信息
  4.删除
  yum -y remove 包名 # 删除指定包
  5.缓存
  yum makecache # 生成缓存
  yum clean all # 删除所有缓存
  ```



定时任务

- 一次性定时任务

  ```shell
  at 时间
  命令（Ctrl + d退出）
  
  相对时间：
  at now+3min
  mkdir /root/test
  
  绝对时间：
  at 20:51
  mkdir /root/test
  
  atq:显示未执行的任务列表
  atrm：删除未执行的任务
  
  now：表示当前时刻。
  tomorrow：表示明天。
  today：表示今天。
  now + 1 minute：表示从当前时间起 1 分钟后执行。
  now + 1 hour：表示从当前时间起 1 小时后执行。
  now + 1 day：表示从当前时间起 1 天后执行。
  now + 2 weeks：表示从当前时间起 2 周后执行。
  
  HH:MM（24小时制）
  HH:MM AM/PM（12小时制）
  YYYY-MM-DD HH:MM（年-月-日 时:分）
  ```

- 周期性定时任务

  ```
  cat /etc/crontab # 查看配置文件
  
  *:表示任意值（例如：*在分钟字段表示每分钟）
  ,:用于分割多个值（1，2，3）
  -:表示范围（1-5）
  /:表示步长（*/5）
  
  crontab -e	编辑定时任务
  crontab -l	显示已经存在的定时任务
  crontab -r	删除所有的定时任务
  
  第一位	分钟（0 - 59）	0-59
  第二位	小时（0 - 23）	0-23
  第三位	日（1 - 31）	1-31
  第四位	月（1 - 12）	1-12
  第五位	星期（0 - 6）	0-6（0代表星期日，1代表星期一，依此类推）
  ```



**练习**

- ![image-20250117123606487](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117123606487.png)
- ![image-20250117123643540](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117123643540.png)
- ![image-20250117123729932](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117123729932.png)



**作业**

```shell
需求：用定时任务完成，包括一次性定时任务和周期性定时任务，不限用户

1.在主目录递归创建3层目录
mkdir -p ~/1/2/3
2.在第二层目录创建一个文件，分两次写入内容
touch ~/1/2/hd.txt
echo 'hello' >> ~/1/2/hd.txt
echo 'world' >> ~/1/2/hd.txt
3.在主目录给/etc 递归创建3层目录
mkdir -p /etc/1/2/3
4.将2文件的内容复制到3中的最里层目录
cp ~/1/2/hd.txt /etc/1/2/3
5.将4的文件复制到/tmp中
cp /etc/1/2/3/hd.txt /tmp
6.将1的第三层目录进行重命名
mv ~/1/2/3 ~/1/2/0
7.查看文件的第一行内容
head -1 ~/1/2/hd.txt
8.删除创建文件和目录 
rm -rf ~/1
rm -rf /etc/1
rm -rf /tmp/hd.txt
```

![image-20250117131158877](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117131158877.png)

![image-20250117131115316](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117131115316.png)

![image-20250117134338717](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117134338717.png)

![image-20250117135122878](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250117135122878.png)