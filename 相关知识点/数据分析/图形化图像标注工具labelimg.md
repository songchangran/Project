## 图形化图像标注工具labelimg

### labelimg是什么

**LabelImg** 是一个用 Python 和 Qt 编写的图形化图像标注工具，常用于目标检测（Object Detection）任务中的 **图像数据集标注**。

它可以将图像中的目标对象通过框选的方式标注出来，并保存为常见的标注格式，比如：

- **Pascal VOC** 格式（.xml）
- **YOLO** 格式（.txt）



### LabelImg 的核心知识点

| 项目         | 内容                                                         |
| ------------ | ------------------------------------------------------------ |
| ✅ 用途       | 图像目标检测数据集的可视化标注                               |
| ✅ 支持格式   | VOC（XML）、YOLO（TXT）                                      |
| ✅ 开发语言   | Python                                                       |
| ✅ UI 框架    | Qt（PyQt5）                                                  |
| ✅ 保存方式   | 每张图片生成一个对应的 `.xml` 或 `.txt` 文件                 |
| ✅ 标注目标   | 可自定义类别，如：人、车、猫、狗等                           |
| ✅ 支持快捷键 | 大量操作可以通过键盘完成，如 `w` 创建框、`d` 下一张图、`Ctrl + S` 保存 |



### 使用流程

1. 安装程序

   ```cmd
   # pip 安装
   pip install labelImg
   
   # 源码安装
   git clone https://github.com/tzutalin/labelImg.git
   cd labelImg
   pip install -r requirements/requirements.txt
   python labelImg.py
   ```

2. 启动程序：

   ```
   
   labelImg
   ```

3. 设置图片路径（Open Dir）

4. 设置保存路径（Change Save Dir）

5. 选择标注格式（Pascal VOC / YOLO）

6. 开始标注目标(W)

7. 保存（快捷键 Ctrl + S）

8. 切换上/下一张图（快捷键 `a`/ `d`）



### 版本建议

截至目前社区使用最广泛、兼容性良好的版本：

- **推荐版本**：`1.8.6`
- **推荐 Python 版本**：`Python 3.8 ~ 3.10`
- **推荐 Qt 依赖**：`PyQt5==5.15.9` 是较为稳定的组合