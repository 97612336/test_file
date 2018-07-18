import base64
import hashlib
import pickle
import time

start_time = time.time()


# 获取数字列表中的最多的重复元素
def get_the_most_repeat_element(num_list):
    count = {}
    for one_num in num_list:
        if str(one_num) in count.keys() and str(one_num) != "0":
            count[str(one_num)] = count[str(one_num)] + 1
        else:
            count[str(one_num)] = 1
    larger_value = 0
    larger_value_key = 0
    for one_key in count.keys():
        if count[one_key] > larger_value:
            larger_value = count[one_key]
            larger_value_key = one_key
    return int(larger_value_key)


# 删除最多的重复元素
def pop_repeat_num_list(one_list, repeat_element):
    i = 0
    new_list = []
    for one in one_list:
        if one == repeat_element:
            new_list.append(0)
        else:
            # 如果不等于重复元素,就执行重新赋值操作
            new_list.append(one)
        i = i + 1
    return new_list


# 计算列表中不为0元素的个数
def count_list_not_zore(one_list):
    i = 0
    for one in one_list:
        if one != 0:
            i = i + 1
    return i


with open('1231234.jpg', 'rb') as f1:
    img_bytes = f1.read()

# 压缩
# 将文件进行base64编码
img = base64.b64encode(img_bytes).decode()

# 把base64编码转化为数字组成的列表
num_list = []
for one in img:
    num_list.append(ord(one))
# 得到列表的最大重复元素
repeat_element = get_the_most_repeat_element(num_list)
# 重新处理num_list,把最大的重复元素pop掉,得到一个新列表
new_list = pop_repeat_num_list(num_list, repeat_element)

new_base64=''
for one in new_list:
    if one!=0:
        new_base64=new_base64+chr(one)

# 解压缩
# 将base64编码的字符串解码
img_bytes = base64.b64decode(img)
with open("test.jpg", 'wb') as f2:
    res = f2.write(img_bytes)

end_time = time.time()

cost_time = end_time - start_time
print(cost_time)
