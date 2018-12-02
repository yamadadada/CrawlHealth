import requests
import pymysql
import time
from lxml import etree

url = "http://tzcs.gdut.edu.cn/spQuery"
url_params = {'method': 'healthscore', 'schoolid': '100001'}


def crawl(sno, db):
    params = url_params
    params['stuNo'] = sno
    r = requests.get(url, params)
    response = etree.HTML(r.text)
    data_dict = dict()
    data_dict['height'] = float(response.xpath('/html/body/table/tbody/tr[1]/td[2]/text()')[0])
    data_dict['weight'] = float(response.xpath('/html/body/table/tbody/tr[2]/td[2]/text()')[0])
    data_dict['lung_capacity'] = float(response.xpath('/html/body/table/tbody/tr[3]/td[2]/text()')[0])
    data_dict['m50'] = float(response.xpath('/html/body/table/tbody/tr[4]/td[2]/text()')[0])
    data_dict['standing_jump'] = float(response.xpath('/html/body/table/tbody/tr[5]/td[2]/text()')[0])
    data_dict['sit_reach'] = float(response.xpath('/html/body/table/tbody/tr[6]/td[2]/text()')[0])
    item7 = float(response.xpath('/html/body/table/tbody/tr[7]/td[2]/text()')[0])
    item8 = float(response.xpath('/html/body/table/tbody/tr[8]/td[2]/text()')[0])
    if sno[1] == '1':
        data_dict['sex'] = 'm'
        data_dict['pull_up'] = item7
        data_dict['m1000'] = item8
    else:
        data_dict['sex'] = 'f'
        data_dict['sit_ups'] = item7
        data_dict['m800'] = item8
    cursor = db.cursor()
    for key, value in data_dict.items():
        if key == 'sex':
            sql = "update student set %s='%s' where sno=%s" % (key, value, sno)
        else:
            sql = "update student set %s=%f where sno=%s" % (key, value, sno)
        cursor.execute(sql)
        db.commit()


db = pymysql.connect("localhost", "root", "3116004646", "student_health", charset='utf8')
cur = db.cursor()
select_sql = "select sno from student"
cur.execute(select_sql)
results = cur.fetchall()
sno_list = []
for row in results:
    sno_list.append(row[0])
for sno in sno_list:
    print("正在遍历：" + sno + "...")
    crawl(sno, db)
    time.sleep(3)
db.close()
