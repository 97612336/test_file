list1 = [{"pinyin":"a"}, {"pinyin": "c"}, {"pinyin": "b"}]

res = list1.sort(key=lambda one_list:one_list.get("pinyin"))


print(list1)



