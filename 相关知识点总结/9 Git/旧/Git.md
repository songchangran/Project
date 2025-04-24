# Git

1. Git简介

   - *开源的分布式版本控制系统*

2. Linux环境（CentOS）中Git环境的安装配置

   - ```shell
     # 1.安装Git
     yum -y install git-core
     
     # 2.配置个人的用户名称和电子邮件地址（或手机号）
     git config --global user.name "scr"
     git config --global user.email 3192355619@qq.com
     
     # 3.查看配置信息
     git config --list
     
     # 4.生成SSH密钥（用来Git托管服务，邮箱可以用手机号替换，在gitee（Github等）上配置密钥）
     ssh-keygen -t rsa -b 4096 -C 3192355619@qq.com
     
     # 5.验证安装
     git --version
     git config --list
     
     # git的工作流程
     https://www.runoob.com/wp-content/uploads/2015/02/git-process.png
     ```

     

3. Windows环境下Git环境的安装配置

   ```
   在Git官网上下载安装，然后在Git Bush中操作或者在Git的GUI界面操作
   ```

   

4. Git的相关操作

   ```shell
   # 克隆仓库
   git clone https://github.com/username/repo.git
   cd repo
   
   # 创建新分支
   git checkout -b new-feature
   
   # 将修改的文件添加到暂存区，或者添加所有修改的文件
   git add filename
   git add .
   
   # 提交更改
   git commit -m "Add new feature"
   
   # 从远程仓库拉取最新更改，或者如果在新的分支上工作
   git pull origin main
   git pull origin new-feature
   
   # 将本地仓库推送到远程仓库
   git push origin new-feature
   
   # 将远程仓库的主分支合并到本地分支
   git checkout main
   git pull origin main
   git merge new-feature
   
   # 删除分支，或者从远程仓库删除分支
   git branch -d new-feature
   git push origin --delete new-feature
   
   # 查看暂存区中的文件
   git status
   
   # 版本库常用命令
   git commit -m "Commit message"   # 将暂存区的更改提交到本地版本库
   git log                          # 查看提交历史
   git diff                         # 查看工作区和暂存区之间的差异
   git diff --cached                # 查看暂存区和最后一次提交之间的差异
   
   # 版本库 -> 远程仓库
   git push origin branch-name
   
   # 远程仓库 -> 本地版本库
   git pull origin branch-name
   
   # 初始化Git仓库
   git init
   
   # 创建分支
   git checkout -b <branchname>
   
   # 切换分支
   git checkout <branchname>
   
   # 查看所有分支（-r远程分支，-a本地和远程所有分支）
   git branch -r/-a
   
   # 将其他分支合并到当前分支
   git merge <branchname>
   
   # 解决合并冲突（修改冲突的地方，然后add再commit）
   
   # 删除分支
   git branch -d <branchname>
   
   注： 在 Linux 系统中，commit 信息使用单引号 '，Windows 系统，commit 信息使用双引号 "。所以在 git bash 中 git commit -m '提交说明' 这样是可以的，在 Windows 命令行中就要使用双引号 git commit -m "提交说明"。
   
   # 菜鸟教程-Git教程：https://www.runoob.com/git/git-tutorial.html
   ```

   