## conda的相关操作

### conda的相关操作

- 创建新环境

  ```cmd
  # 语法
  conda create -n 环境名 python=版本号
  
  # 示例
  conda create -n labelimg-env python=3.9
  
  参数说明：
  -n：指定环境名称，例如 labelimg-env
  python=3.9：指定环境中 Python 的版本（可换成 3.10、3.8 等）
  
  # 可以指定多个初始包一起安装
  conda create -n myenv python=3.10 numpy pandas matplotlib
  ```

- 激活/切换到某个环境

  ```cmd
  # 语法
  conda activate 环境名
  
  # 示例
  conda activate labelimg-env
  
  参数说明：
  activate：用于进入某个环境
  
  环境名：你刚创建的环境名字
  ```

- 退出当前环境，回到默认环境（或者退出虚拟环境）

  ```cmd
  conda deactivate
  ```

- 删除某个环境

  ```cmd
  # 语法
  conda remove -n 环境名 --all
  
  # 示例
  conda remove -n labelimg-env --all
  
  参数说明：
  -n：指定环境名称
  
  --all：删除整个环境及其所有包
  ```

- 查看已有的环境

  ```cmd
  # 方法1
  conda env list
  
  # 方法2
  conda info --envs
  ```

  