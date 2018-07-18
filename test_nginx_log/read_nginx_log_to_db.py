import configparser
import os
import re
import time
import datetime
import pymysql


class Analysis_log(object):
    def __init__(self):
        self.month_dict = {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
            "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
            "Nov": "11", "Dec": "12"
        }

    @staticmethod
    def run():
        al = Analysis_log()
        # 获取当前文件夹下的所有文件
        log_path_list = al.get_all_files_path()
        for one_file_path in log_path_list:
            if '-' in one_file_path:
                # 读取日志文件,获取所有符合条件的日志信息
                cyx_data_list = al.read_nginx_log(one_file_path)
                # 解析符合条件的日志文件
                data_dict_list = al.analysis_log_list(cyx_data_list)
                # 进行存入数据库的操作
                al.save_to_db(data_dict_list)

    # 获取当前路径下的所有文件的绝对路径
    def get_all_files_path(self):
        file_name_list = os.listdir('.')
        # 获取当前文件的路径
        # 获取当前文件除文件名外的路径
        file_path = os.getcwd() + '/'
        all_file_path = []
        for one in file_name_list:
            # 如果文件名是以"l.access.log"开头,就会执行拼接操作
            if one.startswith("l.access.log"):
                file_complete_path = file_path + one
                all_file_path.append(file_complete_path)
        return all_file_path

    # 读取日志文件
    def read_nginx_log(self, log_file_path):
        with open(log_file_path, 'r') as f1:
            res = f1.read()
        re_plex = r'\d.*?/_\.gif\?app=cyx&.*?"'
        cyx_list = re.findall(re_plex, res)
        return cyx_list

    # 解析日志文件
    def analysis_log_list(self, log_list):
        tmp_list = []
        for one in log_list:
            if '/_.gif?app=cyx&shareTo=' in one:
                tmp = {}
                one_list = str(one).split("/_.gif?")
                # 得到此次行为的名称
                res_one = one_list[-1]
                # print(res_one)
                params = res_one.split(' ')[0]
                shareTo = params.split("&")[-1]
                shareTo_str = shareTo.split("=")[-1]
                # 得到行为的时间
                res_zore = one_list[0]
                time_res = res_zore.split(' ')[3]
                one_res = time_res.split('[')[-1]
                # 拆分时间,得到日期和月份
                time_list = one_res.split("/")
                # 天数
                day = time_list[0]
                english_month = time_list[1]
                # 年份和时间的集合
                other = time_list[2]
                # 月份
                month = self.month_dict[english_month]
                # 继续拆分,得到年份和时间
                times = other.split(':')
                # 得到年份
                year = times[0]
                # 得到时分秒
                hour = times[1]
                minute = times[2]
                seconds = times[3]
                time_str = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(
                    minute) + ':' + str(seconds)
                # 保存进字典中
                tmp["time"] = time_str
                tmp["action"] = shareTo_str
                tmp_list.append(tmp)
        return tmp_list

    # 得到连接数据库的connection
    def get_afsaas_connection(self):
        home = os.environ['HOME']
        inifile = '{}/.afsaas.cnf'.format(home)
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

    # 执行存入数据库的操作
    def save_to_db(self, tmp_list):
        conn = self.get_afsaas_connection()
        cursor = conn.cursor()
        if len(tmp_list) > 0:
            date_do_time = tmp_list[0]["time"]
            date = str(date_do_time).split(' ')[0]
            # 根据date查询user_info表,如果查询得到结果,则不继续往下执行,直接return
            select_sql = 'select * from user_info WHERE do_time LIKE "%s%%" AND uuid="cyx";' % (date)
            cursor.execute(select_sql)
            res = cursor.fetchall()
            if len(res) > 0:
                print("%s的数据在数据库中已经存在,不再执行存入操作" % (date))
                return
        for one in tmp_list:
            is_login = 0
            uuid = "cyx"
            do_time = one["time"]
            # 执行查询,如果do_time和cyx的uuid同时存在数据库中,则跳出本次循环
            location = "POINT(1 1)"
            operate_name = one["action"]
            insert_sql = "INSERT into user_info (is_login,uuid,do_time,location,operate_name) " \
                         "VALUES(%s,\"%s\",\"%s\",ST_GEOMFROMTEXT(\"%s\"),\"%s\");" % (
                             is_login, uuid, do_time, location, operate_name)
            cursor.execute(insert_sql)
            try:
                conn.commit()
            except:
                conn.rollback()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    while True:
        Analysis_log.run()
        print('执行完毕，需等待一天')
        time.sleep(60 * 60 * 24)
