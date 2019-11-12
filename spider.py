# import time
# import json
# import requests
# import re
# import pandas as pd
# #
# class Amazonspider(object):
#     def __init__(self,offset):
#         # self.url = "https://www.amazon.co.jp/gp/product/4832244485/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1"
#         self.url = "https://www.amazon.co.jp/%E3%80%8C%E3%81%94%E6%B3%A8%E6%96%87%E3%81%AF%E3%81%86%E3%81%95%E3%81%8E%E3%81%A7%E3%81%99%E3%81%8B-%E3%80%8D%E7%94%BB%E9%9B%86-Cafe-Lapin-" \
#                    "%E3%81%BE%E3%82%93%E3%81%8C%E3%82%BF%E3%82%A4%E3%83%A0KR%E3%82%B3%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9/product-reviews/4832244485/ref=cm_cr_arp_d_paging_btm_prev_4?ie" \
#                    "=UTF8&reviewerType=all_reviews&pageNumber=" + str(offset)
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#             # 'cookie':"
#         }
#         self.offset = 5
#         self.file = open("amazon.json", "w", encoding='utf-8')
#
#     def start_request(self):
#         print("正在爬取第%d页"  % self.offset)
#         content = requests.get(self.url, headers = self.headers).content.decode()
#         # print(content)
#         time.sleep(1)
#         self.content_re(content)
#         self.offset += 1
#         if self.offset == 20:
#             return None
#         self.content_re(content)
#         self.start_request()
#
#     def content_re(self, content):
#         reviewClass = re.findall('<span class="a-icon-alt">(.*?)</span>',content)
#         reviewDate = re.findall('<span data-hook="review-date" class="a-size-base a-color-secondary review-date">(.*?)</span>', content)
#         reviewTitle = re.findall('<a data-hook=.*?ASIN=4832244485"><span class="">(.*?)</span>', content)
#         reviewText = re.findall('<span data-hook="review-body" class="a-size-base review-text review-text-content"><span class="">(.*?)</span>', content)
        # print(reviewClass, reviewDate, reviewText)
#         for classes, date, title, text in zip(reviewClass,reviewDate, reviewTitle, reviewText):
#             # items = {"评星": classes, "时间": date, "标题": title, "内容": text}
#             # i = json.dumps(items, ensure_ascii=False) + "\n"
#             yield {
#                 "class": classes,
#                 "date": date,
#                 "title": title,
#                 "text": text
#             }
#             # print(items)
#             # self.file.write(i)
#
#
#     def write_to_file(content):
#         with open("amazon.json", "w", encoding="utf-8") as f:
#             f.write(json.dumps(content, ensure_ascii=False) + "\n")
#
# if __name__ == '__main__':
#     spider = Amazonspider(i for i in range(10))
#     spider.start_request()

# url = "https://rate.tmall.com/list_detail_rate.htm?itemId=561498041581&spuId=903530411&sellerId=2318796651&order=3&currentPage=1"
# headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
#         }
# myweb = rq.get(url, headers = headers)
# myjson = re.findall('"rateContent":"(.*?)"', myweb.text)[0]
# print(myjson)
# mytable = pd.read_json(myjson)
# mytable.to_csv('mytable.txt')
# mytable.to_excel('mytable.xls')

import json
import requests
from requests.exceptions import  RequestException
import re

def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # reviewClass = re.findall('<span class="a-icon-alt">(.*?)</span>', re.S)
    reviewDate = re.findall( '<span data-hook="review-date" class="a-size-base a-color-secondary review-date">(.*?)</span>', html)
    reviewTitle = re.findall('<a data-hook=.*?ASIN=4832244485"><span class="">(.*?)</span>', html)
    reviewText = re.findall('<span data-hook="review-body" class="a-size-base review-text review-text-content"><span class="">(.*?)</span>',html)
    # pattern = re.compile('<a data-hook=.*?ASIN=4832244485"><span class="">(.*?)</span>',re.S)
    # items = re.findall(pattern, html)

    for date, title, text in zip(reviewDate, reviewTitle, reviewText):
        yield {
                # "class": classes,
                "date": date,
                "title": title,
                "text": text
            }

def write_to_file(content):
    with open("result.text", "a", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")

def main(offset):
    url = "https://www.amazon.co.jp/%E3%80%8C%E3%81%94%E6%B3%A8%E6%96%87%E3%81%AF%E3%81%86%E3%81%95%E3%81%8E%E3%81%A7%E3%81%99%E3%81%8B-%E3%80%8D%E7%94%BB%E9%9B%86-Cafe-Lapin-" \
          "%E3%81%BE%E3%82%93%E3%81%8C%E3%82%BF%E3%82%A4%E3%83%A0KR%E3%82%B3%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9/product-reviews/4832244485/ref=cm_cr_arp_d_paging_btm_prev_4?ie" \
          "=UTF8&reviewerType=all_reviews&pageNumber=" + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == "__main__":
    for i in range(1,20):
        main(i)