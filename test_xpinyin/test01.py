from xpinyin import Pinyin

p = Pinyin()
res = p.get_pinyin("TAlk", "")
print(res)
low_res = res.lower()
print(low_res)

res2 = p.get_initial("上")
dres3 = p.get_initials("上海talk")
