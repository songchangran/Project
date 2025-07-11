class PoolEmptyException(Exception):
    def __str__(self):
        """
        proxypool is used out
        :return:
        """
        # 将对象转化为供解释器读取的形式。
        # 使用pring打印的时候对象打印为str里定义的字符串
        # 如果直接在控制台打印，则调用的是repr方法
        return repr('no proxy in proxypool')