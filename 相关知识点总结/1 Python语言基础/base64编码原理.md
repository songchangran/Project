### base64编码

### 什么是base64编码

Base64编码是一种将二进制数据转换为文本格式的编码方式。



### Base64 编码表

大写字母 + 小写字母 + 数字（0-9） + “+/”



### base64编码原理

1. 将字符串33拆分并转换成对应的ASCII 整数值
2. 将对应的ASCII 整数值转换成8位二进制的形式拼接在一起然后66分组，补齐规则：66分组后不足6位的在后面补0，33分组不足的补“=“
3. 通过base64映射表输出数据

```python
base64_str = 'Mann'

# 第一步 33拆分
# Man n

# 第二步 二进制输出
# ord():将一个字符或单个字符串转换为对应的 Unicode 或 ASCII 整数值
# 77 97 110 / 110
print(ord('M'), ord('a'), ord('n'))

# 第三步 将该字符对应的整数值转换成2进制形式，并对转换的数据进行处理（去掉“0b”，在每一个二进制数据前补0，为了对齐成标准的8位二进制）
# 01101101 01100001 01101110 / 01101110
# 按照分组，不足24位补0
print(bin(109).replace('0b', '0'), bin(97).replace('0b', '0'), bin(110).replace('0b', '0'))

# 第四步 将二进制拼在一起66分组， 011011 010110 000101 101110 / 011011 100000 000000 000000
# 然后转换成十进制数，27 22 5 46 / 27 32 0 0
print(int('011011', 2), int('010110', 2), int('000101', 2), int('101110', 2), int('011011', 2), int('100000', 2))

# 第五步 构建base64映射表，并进行结果打印
from string import ascii_uppercase, ascii_lowercase, digits
base64_tabel = ascii_uppercase + ascii_lowercase + digits + '+/'
print(base64_tabel[27], base64_tabel[22], base64_tabel[5], base64_tabel[46], base64_tabel[27], base64_tabel[32], '=', '=')
```

