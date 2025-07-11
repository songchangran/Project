import os
import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False,
                      import_onnx_path='./num_word_1.0_23_6000_2025-04-28-08-21-47.onnx',
                      charsets_path='./charsets.json')
lists = os.listdir('./data1/')[:8610]

error_count = 0
for imgs in lists:
    code = imgs.split('_')[0]
    with open("./data1/{}".format(imgs), 'rb') as f:
        image = f.read()
    result = ocr.classification(image)
    if code!=result:
        error_count+=1
print('总错误数量：' + str(error_count))
print('总测试数量：8609')
print('错误率：' + str((error_count/8609)*100) + '%')
print('准确率：' + str(((8609-error_count)/8609)*100) + '%')