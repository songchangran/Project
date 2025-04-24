**文件权限**

- 所有者

- 群组

- 其他人：除了所有者和同群组的其他人

- 超级用户：root可以访问系统中所有的文件

  ```shell
  -rw-------. 1 root root 1518 1月 16 20:37 anaconda-ks.cfg
  [1] [2][3] [4] [5] [6] [7]
  1:权限
  2.文件数
  3.文件的所有者
  4.文件的所属群组
  5.文件大小
  6.文件的日期
  7.文件名
  ```

**修改文件的权限和属性**

- chown: 改变文件的拥有者

  ```shell
  # 修改文件的所有者
  [root@localhost ~]# chown xc aaa
  [root@localhost ~]# ll
  总用量 16
  -rw-r--r--. 1 xc xc 0 1月 18 19:28 aaa
  # 同时修改所有者和群组
  [root@localhost ~]# chown root:root aaa
  [root@localhost ~]# ll
  总用量 16
  -rw-r--r--. 1 root root 0 1月 18 19:28 aaa
  ```

- chgrp:改变文件的群组

  ```shell
  # 修改aaa文件的所属群组
  [root@localhost ~]# chgrp xc aaa
  [root@localhost ~]# ll
  总用量 16
  -rw-r--r--. 1 root xc 0 1月 18 19:28 aaa
  ```

- chmod:改变文件的权限

  |              文件类型              |  所有者（u）  | 群组权限（g） | 其他人权限（o） |
  | :--------------------------------: | :-----------: | :-----------: | :-------------: |
  | d:表示目录、l：表示链接文件、 - 普 | rwx 没有的用- | rwx 没有的用- |  rwx 没有的用-  |

  

  ```shell
  1、4、7位表示读取权限
  2、5、8位表示写入的权限
  3、6、9位表示执行的权限
  使用数字表示权限位
  r:4
  w:2
  x:1
  [root@localhost ~]# chmod u=rwx,g=rwx,o=rwx aaa
  [root@localhost ~]# ll
  总用量 16
  -rwxrwxrwx. 1 root root 0 1月 18 19:28 aaa
  [root@localhost ~]# chmod 777 bigdata
  [root@localhost ~]# ll
  总用量 16
  -rwxrwxrwx. 1 root root 0 1月 18 19:28 aaa
  -rw-------. 1 root root 1518 1月 16 20:37 anaconda-ks.cfg
  -rwxrwxrwx. 1 root root 12 1月 14 21:07 bigdata
  ```

**用户和用户组**

```shell
0 是超级管理员用户
1-999 是系统用户：对守护进程进行分配资源的用户
>=1000 是登录用户
[root@localhost ~]# id xc
uid=1000(xc) gid=1000(xc) 组=1000(xc),10(wheel)
[root@localhost ~]# id root
uid=0(root) gid=0(root) 组=0(root)
```

- 用户管理

  - 添加用户

    ```shell
    useradd 选项 用户名
    -c:指定一段注释性的描述
    -d:指定用户的主目录，可以使用-m参数创建用户的主目录
    -g:用户组，指定用户的所属群组
    -G:指定用户的附加组
    -s:指定用户登录的shell
    -u:指定用户的id，如果想重复使用其他用户的id可以使用-o参数
    [root@localhost zhangsan]# useradd -d /home/home1/ -m lo # 创建了一个名为
    lo的用户，指定lo的主目录是/home/home1
    ```

  - 删除用户

    ```shell
    userder 选项 用户名
    -r
    [root@localhost home]# userdel xxx
    [root@localhost home]# ls
    ccc home1 xc xxx zhangsan
    [root@localhost home]# su xxx
    su: user xxx does not exist
    [root@localhost home]# userdel -r zhangsan
    ```

  - 修改用户

    ```shell
    usermod 选项 用户名
    -d:指定用户的主目录，可以使用-m参数创建用户的主目录
    -g:用户组，指定用户的所属群组
    -G:指定用户的附加组
    -s:指定用户登录的shell
    -u:指定用户的id，如果想重复使用其他用户的id可以使用-o参数
    [root@localhost home]# usermod -s /bin/bash -d /home -g t3 ccc
    [root@localhost home]# id ccc
    uid=1005(ccc) gid=1008(t3) 组=1008(t3),1007(t2)
    ```

  - 用户口令的管理

    ```shell
    passwd 选项 用户名
    -l 锁定用户
    -u 解锁
    -d 不使用密码
    -f 强制用户在下次登录修改密码
    [root@localhost ~]# passwd ccc
    更改用户 ccc 的密码 。
    新的 密码：
    无效的密码： 密码少于 8 个字符
    重新输入新的 密码：
    passwd：所有的身份验证令牌已经成功更新。
    [root@localhost ~]# passwd -l ccc
    锁定用户 ccc 的密码 。
    passwd: 操作成功
    [root@localhost ~]# passwd -f ccc
    更改用户 ccc 的密码 。
    新的 密码：
    无效的密码： 密码少于 8 个字符
    重新输入新的 密码：
    passwd：所有的身份验证令牌已经成功更新。
    [root@localhost ~]#
    ```

- 组管理

  - 添加用户组

    ```shell
    useradd 选项 用户组名称
    -g : 指定用户组的gid
    -o : 和-g同时使用，可以为新组创建一个已有组的gid
    [root@localhost ~]# groupadd -g 1009 -o t6
    [root@localhost ~]# cat /etc/group
    ```

  - 删除用户组

    ```shell
    groupdel 用户组名称
    ```

  - 修改用户组

    ```shell
    groupmod 选项 组名
    -g : 指定用户组的gid
    -o : 和-g同时使用，可以为新组创建一个已有组的gid
    -n : 改名
    [root@localhost ~]# groupmod -g 10000 -n tt t1
    ```

**用户和组相关的配置文件**

- /etc/passwd文件：记录每一个用户操作

  ```shell
  [root@localhost ~]# head -n 2 /etc/passwd
  root:x:0:0:root:/root:/bin/bash
  1.用户名
  2.密码
  3.用户的id
  4.用户组的id
  5.注释性描述
  6.主目录
  7.用户使用的shell
  ```

- /etc/group文件：记录了用户组的信息

  ```shell
  [root@localhost ~]# cat /etc/group
  root:x:0:
  1.组名
  2.密码
  3.gid
  4.组内成员
  ```

- /etc/shadow文件：存放了系统用户的密码信息，影子文件

  ```shell
  [root@localhost ~]# head -n 2 /etc/shadow
  root:$6$cKfD.0f2hr2a4zJr$nUlLDjYqiBC4V8ZyA3a9H36skWECIxWXHJsEmizAhDkNswL
  ZxWzZ2RAms/Zah5iKpZDAsDMB3aIS4O/HlR6Gg.:
  用户名：这是用户登录时使用的用户名。
  加密密码：这是密码字段，其中包含用户密码的加密散列。
  最后一次密码更改的时间：这是上次更改用户密码时的时间戳。
  密码最小时间：这是两次更改密码前必须等待的最小天数。
  密码最大时间：这是密码保持有效的最大天数。
  密码警告时间：这是在密码过期前多少天开始警告用户。
  密码非活动时间：这是在密码过期后多少天内用户仍能登录。
  账户到期时间：这是账户的到期时间，过了这个时间用户将无法登录。
  保留字段：这是为将来的用途保留的字段。
  ```

  