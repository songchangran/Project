- 字典(dict)：无序可变，键唯一不可变

  - 创建

    - fromkeys
  
    - dict

    - d = {}

      - ```python
        # 字典的创建
        # dict.fromkeys(iterable, value=None)
        l = [1, 2]
        dictl = dict.fromkeys(l, None)
        print(dictl, type(dictl))
        # dict
        d1 = dict(name='John', age=30)
        print(d1)
        
        ll = [[1, 2], [3, 4]]
        d2 = dict(ll)
        print(d2)
        ```
  
        
  
  - 访问
  
    - d[]：没有该键报错
    - get（）：没有该键输出可指定的默认值
  
  - 增加（没有该键）
  
    - 给不存在的键赋值
    - update
  
  - 修改（有该键）
  
    - 给不存在的键赋值
  
    - update
  
      - ```python
        dict1 = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
        dict1.update({'f':6})
        dict1['g'] = 7
        print(dict1)
        ```
  
        
  
  - 删除
  
    - del(删除单个,删除整个)
    
    - pop(按键弹出,必须指定)
    
    - clear
    
      - ```python
        # pop 必须指定
        keys = dict1.pop('a')
        print(keys, dict1)
        print(dict1)
        # del
        del dict1['b']
        print(dict1)
        ```
  
- 集合(set):无序不重复

  - 创建:空集合set()
  - 增加, +拼接,需要返回一个新的集合
  - 删除
    - del整个set
    - remove(x) 删除集合中指定的元素 `x`，如果元素不存在，会抛出 `KeyError`。
    - discards(x) 删除集合中指定的元素 `x`，如果元素不存在，不会抛出错误。
    - pop() 随机删除并返回集合中的一个元素。
    - clear 清空集合。
  - 访问,for遍历
  - 运算:
    - 交集	&
    - 并集        |
    - 补集(对称差集)        ^        
    - 差集        -

- 总结

  | 总结 | list                            | tuple      | dict                           | set                                  |
  | ---- | ------------------------------- | ---------- | ------------------------------ | ------------------------------------ |
  | 说明 | 可变有序                        | 不可变有序 | 可变（键必须是不可变元素）有序 | 可变无序                             |
  | 增加 | append  extend  insert  +拼接法 | +拼接法    | dict1[xxx] = xxx  update       | add                                  |
  | 删除 | pop  remove  del  clear         | del        | pop  del  clear                | pop  remove  del  clear  discards(x) |
  | 修改 | 下标  切片                      | 不可修改   | dict1[xxx] = xxx  update       | in操作符                             |
  | 查找 | 下标  切片                      | 下标  切片 | items(),keys(),values()        | `in` 操作符                          |
  
  list的append在末尾添加一个元素，extend在末尾挨个添加可迭代对象中的元素，insert按下标插入，set的add方法添加单个元素
  
  pop删除并返回指定索引位置的元素。如果没有指定索引，默认删除并返回最后一个元素。set中随机删除并返回
  
  集合的不可重复元素特性可用来去重	
  
  remove不存在的数据都会抛出KeyError异常
  
  pop弹出的时候list默认弹出最后一个，set随机，dict不存在抛出异常

- 小案例

  ```python
  # 小案例1：学生成绩管理系统
  """
      分析：
          1.用户查看学生列表
          2.输入学生学号记录成绩
          3.学生信息用字典存储
          4.字典的键是学生的学号，值是一个包含学生姓名和默认成绩（0分）的列表
          5.'v'查看学生列表，'r'记录成绩，'q'退出系统
          6.结束的时候打印学生列表
  """
  
  # 模拟数据库
  # 姓名按照进群顺序
  stu_info = {1:['马有芳',0],
              2:['侯佳鹏',0],
              3:['宋长燃',0],
              4:['李嘉伟',0],
              5:['袁俊泽',0],
              6:['弓皓戬',0],
              7:['邢烁琨',0],
              8:['武世泽',0],
              9:['井瑞康',0]}
  
  # 用来实现菜单
  list1 = ['v', 'r', 'q']
  list2 = ['查看学生列表', '记录成绩', '退出系统']
  while True:
      print('*' * 15 + '学生成绩管理系统' + '*' * 15)
      for i,j in zip(list1, list2):
          print(i, j)
  
      # 通过输入中断循环，获取操作信息
      info = input('请输入您的操作：')
  
      # 功能的实现
      if info == 'v':
          for i in range(1, 10):
              print(f'姓名:{stu_info[i][0]}，成绩：{stu_info[i][1]}')
      elif info == 'r':
          num_str = input('请输入学生学号：')
          # 数据校验
          if num_str.isdigit():
              num = int(num_str)
              if num not in (range(1, 10)):
                  print('学生列表内不存在此学号')
                  continue
          num1 = input('请输入成绩：')
          # 数据校验
          if num1.isdigit():
              num1 = int(num1)
              if num1 not in (range(1, 101)):
                  print('学生列表内不存在此学号')
                  continue
          else:
              print('输入数据不合法')
              continue
          # 修改成绩
          stu_info[num][1] = num1
          print('成绩修改成功')
      elif info == 'q':
          for i in range(1, 10):
              print(f'姓名:{stu_info[i][0]}，成绩：{stu_info[i][1]}')
          break
      else:
          print('输入数据不合法')
          continue
  # 小案例2：购物车小程序
  shopping = {1:['火腿肠', 5],
              2:['泡面 ', 4],
              3:['辣条 ', 3],
              4:['瑞士卷', 6],
              5:['牛肉干', 10],
              6:['瓜子 ', 8],
              7:['快乐水', 3],
              8:['啤酒 ', 5],
              9:['花生 ', 7],
              }
  
  # 购物车  {name:[prince, number], [], ……}
  shopping_car = {}
  # 用来打印总消费金额
  money = 0
  
  while True:
      for i in shopping:
          print(i, shopping[i][0], shopping[i][1], '元')
      opration = input('请输入你的选择(q退出并结算，v查看购物车)：')
      if opration.isdigit():
          opration_num = int(opration)
          if opration_num not in shopping:
              print('输入数据不合法，请重新输入')
              continue
      elif opration == 'q':
          for i in shopping_car:
              print(i, shopping_car[i][0], '元', '数量：', shopping_car[i][1], '单商品总价', shopping_car[i][0] * shopping_car[i][1])
              money += shopping_car[i][0] * shopping_car[i][1]
          print(f'您总共消费{money}元')
      elif opration == 'v':
          for i in shopping_car:
              print(i, shopping_car[i][0], '元', '数量：', shopping_car[i][1])
          continue
      else:
          print('输入数据不合法，请重新输入')
          continue
  
      name = shopping[opration_num][0]
      prince = shopping[opration_num][1]
      number = 1
      for i in shopping_car:
          if i == name:
              number = shopping_car[i][1] + 1
      shopping_car[name] = [prince, number]
  ```
  
  ​		