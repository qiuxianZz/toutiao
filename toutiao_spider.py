import json
import time

import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from Loggeer import Logger
from models import SpiderDBSession
from pipeline import get_user_list, get_item_id, update_con

log_obj = Logger('toutiao.log', level='debug')
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))


class TouTiao():
    def __init__(self):
        self.list_url = "https://profile.zjurl.cn/api/feed/profile/v1/?category=profile_all&visited_uid={}&stream_api_version=82&" \
                        "request_source=1&offset={}&version_code=755&version_name=70505&user_id={}&media_id=3759989547&" \
                        "active_tab=dongtai&device_id=65&app_name=news_article"
        self.article_url = "https://a6.pstatp.com/article/full/24/1/{}/{}/1/0/0/0/?iid=106932394204&device_id=56392426097&" \
                           "ac=wifi&mac_address=da%3A51%3A2e%3A03%3A62%3Aa3&channel=baidu_0411&aid=13&app_name=news_article&version_code=755&" \
                           "version_name=7.5.5&device_platform=android&ab_version=1527881%2C662176%2C801968%2C1419041%2C668775%2C1462526%2C1469462" \
                           "%2C1529246%2C1190525%2C1157750%2C11" \
                           "" \
                           "57634%2C1419598%2C1493796%2C1439625%2C1469498%2C668779%2C662099%2C1542396%2C668774" \
                           "%2C1545689%2C857804%2C660830%2C1526646%2C1479497%2C1446849&ab_feature=102749%2C94563&ssmix=a" \
                           "&device_type=SM-G925F&device_brand=samsung&language=zh&os_api=22&os_version=5.1.1" \
                           "&uuid=867653234280434&openudid=2062042228145894&manifest_version_code=7550&resolution=720*1280" \
                           "&dpi=192&update_version_code=75515&_rticket=1584407914013&plugin=18762&tma_jssdk_version=1.46.0.12" \
                           "&rom_version=22&cdid=b7423b30-0d79-44e9-86ac-a799c705da8a"
        self.offset = 0
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    def get_article_list(self, user_id):
        """
        获取文章列表
        :param user_id:
        :return:
        """
        print(user_id)
        try:
            result = s.get(self.list_url.format(user_id, self.offset, user_id), headers=self.headers, timeout=30).text
            print(result)
            if result and json.loads(result)["data"] != []:
                self.offset = json.loads((result)["offset"])
                return json.loads(result)["data"]
        except Exception as e:
            log_obj.logger.info(e)

    def get_item_id(self, data):
        item_id_list = []
        for item in data:
            content = item["content"]
            try:
                content = json.loads(content)
                group_id = "group_id" in content
                item_id = "item_id" in content
                id = "id" in content
                if group_id:
                    item_id_list.append((content["group_id"]))
                elif item_id:
                    item_id_list.append((content["item_id"]))
                else:
                    item_id_list.append((content["id"]))

            except Exception as e:
                print(e)
        return item_id_list

    def get_article(self, item_id):
        res = s.get(self.article_url.format(item_id, item_id), headers=self.headers, timeout=30).text
        data = json.loads(res)
        content = data["data"]["content"]
        if content == "" or content == None:
            sql = "update jrtt_daily_data set content = \'{}\' where item_id =\'{}\'"
            return sql.format(content, item_id)

        tree = etree.HTML(content)
        # con = tree.xpath('//article/p/strong/text()')
        con = tree.xpath('string(.)').strip()
        con = str(con)
        print(con.strip('[]'))
        sql = "update jrtt_daily_data set content = \'{}\' where item_id =\'{}\'"
        return sql.format(con, item_id)


def run(self):
    res = get_user_list()
    for item in res:
        data = self.get_article_list(item[0])
        item_id_list = self.get_item_id(data)
        for item_id in item_id_list:
            self.get_article(item_id)
        time.sleep(10)


if __name__ == '__main__':
    tt = TouTiao()
    # tt.run()
    aa = tt.get_article(6828527676492349959)
    print(aa)
    # ids = get_item_id()
    # for id in ids:
    #     sql = tt.get_article(id[0])
    #     update_con(sql)
