import configparser

import time
from elasticsearch import Elasticsearch
import os
import pymysql
from xpinyin import Pinyin


def get_afsaas_connection():
    home = os.environ['HOME']
    inifile = '{}/.afsaas2.cnf'.format(home)
    config = configparser.ConfigParser()
    config.read(inifile)
    user = config.get('client', 'user')
    password = config.get('client', 'password')
    host = config.get('client', 'host')
    config = {
        'host': host,
        'port': 3306,
        'user': user,
        'password': password,
        'db': 'cyx',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)
    return connection


class Insert_data():
    @staticmethod
    def do_insert():
        i = Insert_data()
        i.insert_brands()
        i.insert_series()
        # i.insert_specs()
        # i.insert_artrecomments()

    def insert_brands(self):
        con = get_afsaas_connection()
        cursor = con.cursor()
        es = Elasticsearch()
        p = Pinyin()
        table_name = "brands"
        # 查询sql数据库中brands表的总行数
        count_sql = "select count(*) from %s;" % table_name
        cursor.execute(count_sql)
        res = cursor.fetchone()
        # 得到数据库中总行数的数字
        sql_count_num = res['count(*)']
        print("品牌表中的数据量为%s" % sql_count_num)
        # 得到es搜索引擎中的数据总条数
        brands_mapping = {
            "mappings": {
                "brands_type": {
                    "properties": {
                        "id": {
                            "type": "integer",
                        },
                        "logo": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "brands_name": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "item": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "status": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "english_name": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "alias_name": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "spell": {
                            "type": "text",
                            "analyzer": "pinyin",
                            "search_analyzer": "pinyin"
                        },
                        "no_analy_spell": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }
            }
        }
        # 如果索引不存在，则创建索引
        if es.indices.exists(index='brands') is not True:
            es.indices.create(index='brands', body=brands_mapping)
            # 查询es中的cyx索引的brands类型数据的总行数
        es_res = es.count(index="brands", doc_type="brands_type")
        es_count_num = es_res["count"]
        print("es中品牌数量的个数为%s" % es_count_num)
        # 如果mysql数据库中的文件个数大于es搜索引擎中的个数，则执行MySQL数据库至es搜索引擎的插入操作
        if es_count_num < sql_count_num:
            print("执行插入es品牌索引操作")
            i = 0
            # es中的索引最大值
            brands_res = es.search(index="brands", doc_type="brands_type",
                                   body={"query": {"match_all": {}}, "aggs": {"max_age": {"max": {"field": "id"}}}})
            max_id = brands_res["aggregations"]["max_age"]["value"]
            if max_id:
                max_id = max_id
            else:
                max_id = 0
            # 循环执行插入操作
            while True:
                select_sql = "select * from brands where id>%s limit %s,10;" % (max_id, i)
                cursor.execute(select_sql)
                sql_res = cursor.fetchall()
                if i > sql_count_num:
                    break
                for one in sql_res:
                    if one:
                        es.index(index='brands', doc_type='brands_type',
                                 body={"id": one['id'], "logo": one['logo'], "brands_name": one['name'],
                                       "item": one['items'], "status": one['status'],
                                       "english_name": one['english_name'],
                                       "alias_name": one['alias_name'], "no_analy_spell": p.get_pinyin(one["name"]),
                                       "spell": one['spell']}, id=one['id'])
                i = i + 10
        cursor.close()
        con.close()

    def insert_series(self):
        con = get_afsaas_connection()
        cursor = con.cursor()
        es = Elasticsearch()
        table_name = "series"
        count_sql = "select count(*) from %s;" % table_name
        cursor.execute(count_sql)
        res = cursor.fetchone()
        sql_count_num = res['count(*)']
        print('车系表中的数据量为%s' % sql_count_num)
        series_mapping = {
            "mappings": {
                "series_type": {
                    "properties": {
                        "id": {
                            "type": "integer",
                        },
                        "series_name": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "img_url": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "brand_id": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "maxprice": {
                            "type": "integer",
                        },
                        "minprice": {
                            "type": "integer",
                        },
                        "status": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "grade": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "d_url": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "has_360": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "has_scene": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "alike": {
                            "type": "integer",
                        },
                        "series_factory": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "spell": {
                            "type": "text",
                            "analyzer": "pinyin",
                            "search_analyzer": "pinyin"
                        },
                        "no_line_spell": {
                            "type": "text",
                            "analyzer": "pinyin",
                            "search_analyzer": "pinyin"
                        },
                        "no_analy_spell": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }
            }
        }
        if es.indices.exists(index='series') is not True:
            es.indices.create(index='series', body=series_mapping)
        # 查询es中的cyx索引的brands类型数据的总行数
        es_res = es.count(index="series", doc_type="series_type")
        es_count_num = es_res["count"]
        p = Pinyin()
        print("es中车系数量的个数为%s" % es_count_num)
        if es_count_num < sql_count_num:
            print('执行插入操作')
            i = 0
            # es中的索引最大值
            series_res = es.search(index="series", doc_type="series_type",
                                   body={"query": {"match_all": {}}, "aggs": {"max_age": {"max": {"field": "id"}}}})
            max_id = series_res["aggregations"]["max_age"]["value"]
            if max_id:
                max_id = max_id
            else:
                max_id = 0
            while True:
                select_sql = "select * from series where id>%s  limit %s,10" % (
                    max_id, i)
                cursor.execute(select_sql)
                new_res = cursor.fetchall()
                if i > sql_count_num:
                    break
                for one in new_res:
                    if one:
                        es.index(index="series", doc_type="series_type",
                                 body={"id": one['id'], "series_name": one['name'], "brand_id": one['brand_id'],
                                       "grade": one['grade'], "status": one['status'], "img_url": one['img_url'],
                                       "maxprice": one['maxprice'], "minprice": one['minprice'],
                                       "no_analy_spell": p.get_pinyin(one['name']),
                                       'd_url': one['d_url'], "no_line_spell": p.get_pinyin(one['name'], splitter=''),
                                       "has_360": one['has_360'], 'has_scene': one['has_scene'], "alike": one['alike'],
                                       "series_factory": one['factory'], "spell": p.get_pinyin(one['name'])},
                                 id=one['id'])
                i = i + 10
        cursor.close()
        con.close()

    def insert_specs(self):
        con = get_afsaas_connection()
        cursor = con.cursor()
        es = Elasticsearch()
        table_name = "specs"
        count_sql = "select count(*) from %s;" % table_name
        cursor.execute(count_sql)
        res = cursor.fetchone()
        sql_count_num = res['count(*)']
        print('车型表中的数据量为%s' % sql_count_num)
        specs_mapping = {
            "mappings": {
                "specs_type": {
                    "properties": {
                        "id": {
                            "type": "integer",
                        },
                        "series_id": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "specs_name": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "specs_factory": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "specs_type": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        }
                    }
                }
            }
        }
        if es.indices.exists(index='specs') is not True:
            es.indices.create(index='specs', body=specs_mapping)
            # 查询es中的cyx索引的brands类型数据的总行数
        es_res = es.count(index="specs", doc_type="specs_type")
        es_count_num = es_res["count"]
        print("es中车型数量的个数为%s" % es_count_num)
        if es_count_num < sql_count_num:
            print('执行插入操作')
            i = 0
            # es中的索引最大值
            specs_res = es.search(index="specs", doc_type="specs_type",
                                  body={"query": {"match_all": {}}, "aggs": {"max_age": {"max": {"field": "id"}}}})
            max_id = specs_res["aggregations"]["max_age"]["value"]
            if max_id:
                max_id = max_id
            else:
                max_id = 0
            while True:
                select_sql = "select id,series_id,i1,i3,i4 from specs where id>%s  limit %s,10" % (max_id, i)
                cursor.execute(select_sql)
                new_res = cursor.fetchall()
                if i > sql_count_num:
                    break
                for one in new_res:
                    if one:
                        es.index(index="specs", doc_type="specs_type",
                                 body={"id": one['id'], "series_id": one['series_id'], "specs_name": one['i1'],
                                       "specs_factory": one['i3'],
                                       "specs_type": one['i4']}, id=one['id'])
                i = i + 10
        cursor.close()
        con.close()

    def insert_artrecomments(self):
        con = get_afsaas_connection()
        cursor = con.cursor()
        es = Elasticsearch()
        table_name = "art_recommends"
        count_sql = "select count(*) from %s;" % table_name
        cursor.execute(count_sql)
        res = cursor.fetchone()
        sql_count_num = res['count(*)']
        print('文章表中的数据量为%s' % sql_count_num)
        articles_mapping = {
            "mappings": {
                "articles_type": {
                    "properties": {
                        "id": {
                            "type": "integer",
                        },
                        "title": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "car_name": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "series_id": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "b_ref": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "author": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "comment": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "c_ref": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "atype": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "weight": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "status": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "no_analy_title": {
                            "type": "string",
                            "index": "not_analyzed"
                        }

                    }
                }
            }
        }
        if es.indices.exists(index='articles') is not True:
            es.indices.create(index='articles', body=articles_mapping)
            # 查询es中的cyx索引的brands类型数据的总行数
        es_res = es.count(index="articles", doc_type="articles_type")
        es_count_num = es_res["count"]
        print("es中文章数量的个数为%s" % es_count_num)
        if es_count_num < sql_count_num:
            print('执行插入操作')
            i = 0
            # es中的索引最大值
            article_res = es.search(index="articles", doc_type="articles_type",
                                    body={"query": {"match_all": {}}, "aggs": {"max_age": {"max": {"field": "id"}}}})
            max_id = article_res["aggregations"]["max_age"]["value"]
            if max_id:
                max_id = max_id
            else:
                max_id = 0
            while True:
                select_sql = "select id,title,car_name,series_id,b_ref,author,comment,c_ref," \
                             "atype,weight,status from art_recommends where id>%s  limit %s,10" % (
                                 max_id, i)
                cursor.execute(select_sql)
                new_res = cursor.fetchall()
                if i > sql_count_num:
                    break
                for one in new_res:
                    if one:
                        es.index(index="articles", doc_type="articles_type",
                                 body={"id": one['id'], "title": one['title'], "car_name": one['car_name'],
                                       "series_id": one['series_id'], "no_analy_title": one['title'],
                                       "b_ref": one['b_ref'], "author": one['author'], "comment": one['comment'],
                                       "c_ref": one['c_ref'],
                                       "atype": one['atype'], "weight": one['weight'], "status": one['status']},
                                 id=one['id'])
                i = i + 10
        cursor.close()
        con.close()


if __name__ == '__main__':
    i = 1
    while True:
        print('开始执行第%s次' % i)
        Insert_data.do_insert()
        print('执行完毕，需等待一小时')
        time.sleep(60 * 60)
        i = i + 1
