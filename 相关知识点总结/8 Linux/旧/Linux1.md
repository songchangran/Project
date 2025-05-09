**Linux**

- 操作系统的组成部分、

  - 内核
  - 解释器
  - 硬件
  - 软件

- 系统的分类

  - 服务器系统：
    - Windows Server
    - RHEL
    - CentOS
  - 桌面操作系统
    - Windows 10/11/7/xp
    - Ubantu
    - ChromeOS
  - 移动端操作系统
    - Andriod
    - ios
    - HarmonyOS
    - HyperOS

- Linux的特点

  - 开源免费
  - 安全性较高
  - 多任务、多用户
  - 可移植性

- Linux的哲学思想

  - 一切皆文件
  - 一个程序只做一件事

- 环境搭建（已完成）

- 快捷键

  - Ctrl + L：清屏
  - Ctrl + A:回开头

- 命令的使用

  ```shell
  su：切换用户
  sudo xxx：以管理员身份运行命令（密码是用户的密码）
  
  pwd：显示当前所在路径
  
  cd：切换目录
  参数：
  1 无参：返回当前目录主目录
  2 .：当前目录
  3 ..：上一级目录
  4 ~：当前用户主目录
  5 /：根目录
  6 [路径]：进入路径
  7 -：返回上一个目录（不是上一级目录）
  
  ls：列出当前目录内容
  参数：
  1 无参：列出当前目录内容
  2 -a：显示所有的内容，包括以 . 或 .. 开头的隐藏内容
  3 -A：显示所有内容，除了 . 和 .. 这两个特殊目录
  4 -l：以详细的格式显示文件或目录的内容（如权限、所有者、大小和修改时间等）
  5 -h：和 -l 连用，以更容易阅读的格式显示文件大小（例如 KB、MB、GB）
  6 -r：递归列出子目录的内容
  7 -t：按时间排序，默认显示最新修改的文件
  8 ll：ls -l的别名，可以加参数例如ll -h
  9 [目录路径]：列出指定目录内容
  
  mkdir：创建目录
  参数：
  1 目录名：创建单个目录
  2 目录名1 目录名2……：创建多个目录
  3 -p 目录名/子目录名：递归创建多级目录，父目录不存在会创建
  4 -m 权限 目录名：创建具有指定权限的目录
  5 -v：显示详细信息
  
  rmdir：删除空目录
  参数：
  1 目录名：删除单个空目录
  2 目录名1 目录名2……：删除多个空目录
  3 -p 目录路径：递归删除空目录
  4 -v:显示详细信息
  
  rm：删除文件或目录
  参数：
  1 文件名：删除单个文件
  2 文件名1 文件名2……：删除多个文件
  3 -d 目录名：删除空目录
  4 -r 目录名：递归删除目录及其内容
  5 -f 文件名/目录名：强制删除目录及其内容
  6 -i 文件名：交互式删除文件
  7 -rf：递归并强制删除文件和目录（无提示）
  8 -ri:同上，但逐一提示是否删除
  注意：如果文件名中包含空格或特殊字符，可以使用引号或转义字符来删除
  
  cp：复制
  参数：
  1 源文件 目标文件：复制单个文件（目标文件不存在自动创建）
  2 文件1 文件2 ... 目标目录：复制多个文件到目录
  3 -r 源目录 目标目录：复制目录
  4 -f 源文件 目标文件：强制覆盖目标文件
  5 -i：交互式复制（提示确认覆盖）
  6 -p：保留文件属性（如权限、时间戳等）
  7 -v：显示详细信息
  8 cp 源文件 目标目录/新文件名：复制文件并重命名
  
  mv：移动/重命名文件/目录
  参数：
  1 源文件 目标文件：重命名文件或目录
  2 文件名 目标目录：移动文件到指定目录
  3 文件1 文件2 ... 目标目录：移动多个文件到指定目录
  4 -f 源文件 目标文件：强制覆盖目标文件
  5 -i 源文件 目标文件：交互式移动（提示确认覆盖）
  6 目录 目标目录：移动目录
  7 源目录 目标目录/新目录名：移动并重命名目录
  8 -v：显示强制信息
  
  文件相关的命令：
  touch 文件名：创建文件
  
  echo：给文件写入内容（>覆盖 >>追加，没有文件自动创建文件）
  
  cat：从上向下一屏显示，创建文件并写入内容，查看文件内容（常用于小文件）
  
  tac: 从下往上一屏显示
  
  less：分页查看文件内容，q退出，空格向前翻页，b向后翻页，回车向前滚动一行，y向后滚动一行
  
  head: 查看文件头部内容，不加参数默认显示头10行内容（文件名前加-n表示显示行数）
  
  tail:查看文件尾部内容，剩余同上
  
  vim：
  i：插入模式
  Esc：普通模式
  ：命令行模式
  ```

- 作业：

  ```shell
  普通用户操作
  
  1.在主目录递归创建3层目录
  mkdir -p 1/2/3
  2.在第二层目录创建一个文件，分两次写入内容
  touch 1/2/hd.txt # 创建文件可以省略，因为echo时没有文件会自动创建文件
  echo 'hello' > 1/2/hd.txt（>覆盖）
  echo 'world' >> 1/2/hd.txt（>>追加）
  3.在主目录给/etc 递归创建3层目录
  sudo mkdir -p /etc/1/2/3
  4.将2文件的内容复制到3中的最里层目录
  sudo cp hd.txt /etc/1/2/3
  5.将4的文件复制到/tmp中
  sudo cp /etc/1/2/3/hd.txt /tmp
  6.将1的第三层目录进行重命名
  mv 3 0
  7.查看文件的第一行内容
  head -1 hd.txt
  8.删除创建文件和目录 
  rm -rf 1
  sudo rm -rf 1
  sudo rm -rf hd.txt
  ```
  
  ![	](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115181019350.png)
  
  ![image-20250115181307280](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115181307280.png)

​	![	](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115181613203.png)

​	![image-20250115183257354](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115183257354.png)

![image-20250115183542564](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115183542564.png)

![image-20250115183744714](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115183744714.png)

![image-20250115183845579](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250115183845579.png)