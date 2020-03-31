# -*- coding: utf-8 -*-
import scrapy
import pymysql
from pttscrapyproject.items import PttscrapyprojectItem
import time

class PttSpider(scrapy.Spider):

    name = 'ptt'
    allowed_domains = ['ptt.cc']

    start_urls = ['https://www.ptt.cc/bbs/ios/index.html']#此為ios版需要爬蟲的主網，不同分類版，只要輸入該分類版的主網就可以

    cookies = {'over18':'1'}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    def start_requests(self):

        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, cookies=self.cookies)

    def parse(self, response):

        res = response.xpath('//*[@id="main-container"]/div[2]/div/div[2]/a//@href').extract()

        for u in res:

            urls = 'https://www.ptt.cc' + str(u)

            yield scrapy.Request(urls, self.parse_item, headers=self.headers,cookies=self.cookies)

    def parse_item(self, response):

        item = PttscrapyprojectItem()

        item['canonical_url'] = response.url.strip()

        author_list = response.xpath('//*[@id="main-content"]/div[1]/span[2]/text()').extract()
        try:
            for item['author_id'] in author_list:

                item['author_id'] = item['author_id'].split('(')[0].strip()

            for item['author_name'] in author_list:

                item['author_name'] = item['author_name'].split('(')[1].replace(')', '').strip()


            titles_list = response.xpath('//*[@id="main-content"]/div[3]/span[2]/text()').extract()

            for item['title_name'] in titles_list:

                item['title_name'] = item['title_name'].split(':')[0].strip()

                item['title_name'] = item['title_name'].split(']')[1].strip()
            item['created_time'] = time.strftime("%Y-%m-%dT%H:%M:%S.020+00:00",time.gmtime(time.time()))

            item['update_time'] = time.strftime("%Y-%m-%dT%H:%M:%S.020+00:00", time.gmtime(time.time()))

            published_time_list = response.xpath('//*[@id="main-content"]/div[4]/span[2]/text()').extract()

            for i in published_time_list:

                item['published_time'] = round(time.mktime(time.strptime(i, "%a %b %d %H:%M:%S %Y")))

            content_list = response.xpath('//*[@id="main-content"]/text()').extract()

            for ll, content in enumerate(content_list):

                content_list[ll] = content.strip()

            content_list = list(filter(None, content_list))

            ta_content = ""
            for t in content_list:

                ta_content += t

                item['content_text'] = ta_content.split('--')[0].strip()

            category_db_list = response.xpath('//*[@id="topbar"]/a[2]/text()').extract()

            for c in category_db_list:

                item['category_db'] = c.lower()

            comment_id_list = response.xpath('//*[@class="push"]/span[2]/text()')

            for b in range(len(comment_id_list)):

                comment_id_list[b] = str(comment_id_list[b]).strip()

                comment_id_list[0] = comment_id_list[0].split("='")

                comment_id_list[0] = comment_id_list[0][-1].replace("'>",'')

            item['comment_id'] = comment_id_list[0]

            comment_list = response.xpath('//*[@class="push"]/span[3]/text()')

            for a in range(len(comment_list)):

                comment_list[a] = str(comment_list[a]).replace(':', '')

                comment_list[a] = comment_list[a].strip()

                comment_list[0] = comment_list[0].split("='")

                comment_list[0] = comment_list[0][-1].replace("'>", '')

            item['comment_text'] = comment_list[0]

            comment_time_list = response.xpath('//*[@class="push"]/span[4]/text()')

            try:

                for e in range(len(comment_time_list)):

                    comment_time_list[e] = str(comment_time_list[e]).strip()

                    comment_time_list[0] = comment_time_list[0].split("=\'")

                    comment_time_list[0] = comment_time_list[0][-1].replace("\\n'>", '')

                comment_time_list[0] = comment_time_list[0] + ' ' + time.ctime(time.time()).split(' ')[4]

                item['comment_time'] = round(time.mktime(time.strptime(comment_time_list[0], " %m/%d %H:%M %Y")))

            except ValueError:

                comment_time = ' '

                for f in range(len(comment_time_list)):

                    comment_time_list[f] = str(comment_time_list[f]).strip()

                    comment_time_list[f] = str(comment_time_list[f]).split(' ')[1:3]

                    comment_time = comment_time.join(comment_time_list[f])

                    comment_time = comment_time + ' ' + time.ctime(time.time()).split(' ')[4]

                item['comment_time'] = round(time.mktime(time.strptime(comment_time, "%m/%d %H:%M %Y")))

            return item

        except IndexError:

            print('------------------------------------------此文章被刪除-----------------------------------------')

