import json

import demjson

str1 = '''
    [{"comment": "      [汽车之家 新闻]    距离日内瓦车展开幕不足24小时，汽车之家前方报道团队在探馆时，提前拍摄到了梅赛德斯-AMG GT四门版（暂称）的实车，该车将是未来保时捷Panamera最大的竞争对手。", "type": "text"}, {"font": {"height": 465, "width": 620}, "type": "img"}, {"comment": "      作为一款大型四门Coupe车型，梅赛德斯-AMG GT四门版延续了AMG GT概念车的设计思路，采用溜背式设计风格，这一点与保时捷Panamera有异曲同工之妙，不过相比之出自梅赛德斯-AMG之手的它将在风格上完全体现出高性能的特性。", "type": "text"}, {"font": {"height": 348, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__wKgHH1qa_GGADRuHAAc-_ktJBek828.jpg", "type": "img"}, {"comment": "      尤其在尾部设计上，夸张的底部扩散器与双边共四出排气融为一体，同时在溜背式尾门的后方还将设计有一块主动式扰流板。", "type": "text"}, {"font": {"height": 410, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_0_autohomecar__wKgHIFqci9eADdJhAAI9bo_vJdQ639.jpg", "type": "img"}, {"comment": "      虽然探馆当中我们没能拍到新车前脸，但从提前曝光的官图来看，新车采用AMG家族最新的进气格栅，同时辅以夸张的前包围造型，使得其流露出异常凶狠的风格。", "type": "text"}]

'''

res1 = demjson.decode(str1)
# print(type(res1))
# print(res1)

str2 = '''[{"comment": "      [汽车之家 技术]    在本届日内瓦车展上，一台重磅新车吸引了大家的注意，那就是奔驰推出的AMG GT四门Coupe车型。
相比现有的AMG GT，四门Coupe变得更加实用，车身线条也更加舒展和流畅，相信很多喜欢AMG GT，但又纠结于双座跑车实用性太差的朋友们要开心地跳起来了。
不过大家先不要高兴得太早，这台“加长”的AMG GT还算是“真正的”AMG GT吗？换句话说，这台车的真实身份是否和你所期待的一样呢？", "type": "text"},
 {"font": {"height": 684, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_0_autohomecar__
 wKgHH1qlJ4GAOjJXAA2Kop_sP28631.jpg", "type": "img"}, 
 {"comment": "- 外观内饰设计上的"蛛丝马迹"", "font": {"fontWeight": "bold"}, "type": "text"}, 
 {"comment": "      不知道有多少人和我一样，在看过AMG GT四门Coupe（以下简称‘四门GT’）的车侧造型之后，想到了另外一款刚刚问世没多久的车型：
 第三代奔驰CLS级。毕竟，奔驰自家的轿跑车气质相似还是很正常的。", "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 ChcCr1qkzruAUVFYAApTLj_wABQ940.jpg", "type": "img"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIlqkzr2AaUSEAAfP0B8_vPQ181.jpg", "type": "img"}, 
 {"comment": "      当坐进四门GT的车内之后，作为E级车主的我一下子就找到了归属感：仪表台整个造型基本是从E级车上“端过来”的，不过，
 空调出风口采用了奔驰最新的、最先出现在E级Coupe/Cabriolet上的造型。当然了，由于CLS级与E级同出自奔驰MRA平台，
 因此第三代CLS级的内饰与E级也十分接近。另外，车型的整体宽度也和E级非常相似，只是从AMG GT上移植过来的下部中控台显得有点宽，
 占据了不小的空间。", "type": "text"}, 
 {"font": {"height": 529, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIlqk1HKATjFKAAq6cOlenCM684.jpg", "type": "img"}, 
 {"font": {"height": 614, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIlqk2NKAD4NlAA2QoGjqhf8531.jpg", "type": "img"}, 
 {"comment": "- 底盘结构中找到证据！", "font": {"fontWeight": "bold"}, "type": "text"}, 
 {"comment": "      我们都知道，梅赛德斯-AMG GT双门版是一台发动机前中置的高性能跑车，也是由AMG独立打造的第二款纯粹的跑车。之所以说纯粹，
 意味着这台车并不和任何轿车车型共用平台，难道这一次AMG可以在一个纯跑车平台上打造出一款四门轿跑车吗？从底盘结构中就可以收获很多相关的信息。", 
 "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHH1qk2qiAc8yIAAmvTkpRgmI020.jpg", "type": "img"}, {"comment": "前悬架：与两门车型不同", "font": {"fontWeight": "bold"}, 
 "type": "text"}, 
 
 {"comment": "      说到性能跑车的前悬架结构，大家肯定会脱口而出：双叉臂！双叉臂的好处我们不多说了，
 不论是物美价廉的MX-5，超跑级别的迈凯伦570S，还是两门版AMG GT车型，都采用了这一结构。", "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIFqk40iAfPdFAAb4Q4-OBVw438.jpg", "type": "img"}, 
 {"comment": "      而我们在车展上看到的GT四门版前悬架，与两门版车型的那种典型的双叉臂还是有着一定差异。它们之间最明显的特征差异在于，
 GT四门版前悬架的下控制臂分为了两根，而不是一个完整的A型控制臂。严谨的叫法可以称之为双横臂式结构，同时也可以笼统地称之为多连杆结构。", 
 "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIlqk5WCAbBbBAAki4F0P-PY349.jpg", "type": "img"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHH1qlNZWAItHzAAkGUtgXQY4053.jpg", "type": "img"}, 
 {"comment": "      这样的结构大多数用于中高端轿车上，比如……奔驰E级和CLS级，当然在细节和调校上还是会有一些差别，但本质上是趋于一致的。
 所以在GT四门版上出现并不会有什么失格之处，毕竟我并不会觉得E级的底盘有什么不好，你说对吧？不过GT四门版的身份已经有了一些眉目。", 
 "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIVqk5kWAerDjAAivSTNUjn8131.jpg", "type": "img"}, 
 {"comment": "后悬架：与E级、CLS级相同", "font": {"fontWeight": "bold"}, "type": "text"}, 
 {"comment": "      我们都知道，此前的两门版AMG GT跑车承袭了前辈SLS AMG的底盘架构，为了追求更加极致的重量分配，两款纯粹的跑车都将变速箱
 放在了车辆后部。此外，两门版AMG GT的后悬架采用了双叉臂式结构，这样的结构也在很多超级跑车上出现过。", "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 wKgHIlqk40aAbIUiAAbiZpqfdk8934.jpg", "type": "img"}, 
 {"comment": "      再看GT四门版的后悬架，两者的差别就一目了然了：依旧是我们熟悉的、在奔驰E级上出现过的多连杆式结构，这也是奔驰轿车典型的后
 悬架形式。当然，在一些细节的设置和调校上还会体现出AMG的功力。", "type": "text"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 ChcCr1qlAWCAH296AAkTxfxILUM427.jpg", "type": "img"}, 
 {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__
 ChcCr1qlAWGAQlRMAAfYjRCsTyc844.jpg", "type": "img"}, 
 {"comment": "总结：", "font": {"fontWeight": "bold"}, "type": "text"}]

'''

str3='''[  {"comment": "      不知道有多少人和我一样，在看过AMG GT四门Coupe（以下简称‘四门GT’）的车侧造型之后，想到了另外一款刚刚问世没多久的车型：第三代奔驰CLS级。毕竟，奔驰自家的轿跑车气质相似还是很正常的。", "type": "text"}, {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__ChcCr1qkzruAUVFYAApTLj_wABQ940.jpg", "type": "img"}, {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__wKgHIlqkzr2AaUSEAAfP0B8_vPQ181.jpg", "type": "img"}, {"comment": "      当坐进四门GT的车内之后，作为E级车主的我一下子就找到了归属感：仪表台整个造型基本是从E级车上“端过来”的，不过，空调出风口采用了奔驰最新的、最先出现在E级Coupe/Cabriolet上的造型。当然了，由于CLS级与E级同出自奔驰MRA平台因此第三代CLS级的内饰与E级也十分接近。另外，车型的整体宽度也和E级非常相似，只是从AMG GT上移植过来的下部中控台显得有点宽，占据了不小的空间。", "type": "text"}, {"font": {"height": 529, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__wKgHIlqk1HKATjFKAAq6cOlenCM684.jpg", "type": "img"}, {"font": {"height": 614, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__wKgHIlqk2NKAD4NlAA2QoGjqhf8531.jpg", "type": "img"}, {"comment": "- 底盘结构中找到证据！", "font": {"fontWeight": "bold"}, "type": "text"}, {"comment": "      我们都知道，梅赛德斯-AMG GT双门版是一台发动机前中置的高性能跑车，也是由AMG独立打造的第二款纯粹的跑车。之所以说纯粹，意味着这台车并不和任何轿车车型共用平台，难道这一次AMG可以在一个纯跑车平台上打造出一款四门轿跑车吗？从底盘结构中就可以收获很多相关的信息。", "type": "text"}, {"font": {"height": 465, "width": 620}, "url": "http://cdn.autoforce.net/cyx/images/recommends/620x0_1_autohomecar__wKgHH1qk2qiAc8yIAAmvTkpRgmI020.jpg", "type": "img"}, {"comment": "前悬架：与两门车型不同", "font": {"fontWeight": "bold"}, "type": "text"}]

'''

res2 = json.loads(str3)
# print(type(res2))
# print(res2)


str4='{"comment": "- 外观内饰设计上的"蛛丝马迹"", "font": {"fontWeight": "bold"}, "type": "text"}'
json.loads(str4)