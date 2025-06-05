### Python中的深拷贝与浅拷贝

### 1 深拷贝与浅拷贝的概念

- 深拷贝：深拷贝会递归的复制所有子对象，也就是说，不仅复制最外层对象，还会复制所有内层的对象，生成完全独立的副本。

- 浅拷贝：浅拷贝只会复制对象的第一层内容，对于对象当中包含的子对象，只会复制他们的引用地址，而不是复制真实的内容。

  ```python
  from copy import copy
  from copy import deepcopy
  
  # 定义要复制的对象
  demo_list1 = [1, 2, [3, 4]]
  # 浅拷贝
  qian_copy = copy(demo_list1)
  # 深拷贝
  shen_copy = deepcopy(demo_list1)
  # 浅拷贝 False
  print('浅拷贝后的对象与原对象是否是同一个对象：', qian_copy is demo_list1)
  # 深拷贝 False
  print('深拷贝后的对象与原对象是否是同一个对象：', shen_copy is demo_list1)
  # 判断深浅拷贝的子对象是否是同一个对象
  print(qian_copy[2] is demo_list1[2]) # True
  print(shen_copy[2] is demo_list1[2]) # False
  # 修改demo_list1，查看深浅拷贝对象是否更改
  demo_list1[2] = [5, 6]
  print(qian_copy) # [1, 2, [3, 4]]
  print(shen_copy) # [1, 2, [3, 4]]
  # 修改深拷贝对象查看demo_list1是否更改
  shen_copy[2] = [5, 6]
  print(demo_list1) # [1, 2, [5, 6]]
  # 修改浅拷贝对象查看demo_list1是否更改
  qian_copy[2] = [7, 8]
  print(demo_list1)
  ```

### 2 对比

- 浅拷贝复制对象，修改浅拷贝后对象原对象会发生改变，但是修改原对象，浅拷贝对象不会变
- 浅拷贝是创建一个副本

