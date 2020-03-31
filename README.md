此次構想情境為公司已有相對應sql的分類table及需求的column，scrapy並無新增table及column(注意:mysql裡要有分類版的table和題目要求的column)

最終目的是將scrapy爬取的資料進mysql，sql看是在本地端還是雲端，只要有sql使用者擁有外部

將pttscrapyproject用python3.7或pycharm就可執行，本機端就可執行

(在有pip install scrapy
                pymysql
                的環境下)
                
在有docker-compose.yml下執行docker-compose up -d

執行docker run -it --network=develop_scrapy_mysql_net mysql mysql -uroot -p -hdb

就可執行mysql

此時將scrapy的setting檔修改相對應mysql的ip及可以從外部連結的使用者，就可將爬取的資料進docker裡的mysql

最後因為開發方便，所以mysql可以從外部連結的使用者先用root，若是公司在執行會配發個只能SELECT,INSERT,UPDATE,DELETE,CREATE,DROP權限的admin









