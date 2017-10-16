from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
import MySQLdb

class Movies(CrawlSpider):
    name = 'movies'
    start_urls = ['https://www.youtube.com/movies']

    def __init__(self, *args, **kwargs):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="Moviesdb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()


    def parse(self, response):
        sel = Selector(response)
        nodes =  sel.xpath('//ul[@id="browse-items-primary"]//li[contains(@class, "branded-page-box")]//div[@class="yt-uix-shelfslider-body"]/ul/li')
        
        for node in nodes:
            link = ''.join(node.xpath('.//div[@class="yt-lockup-thumbnail"]/a/@href').extract())
            url = 'https://www.youtube.com'+link
            yield Request(url, callback = self.parse_movie, meta={})

    def parse_movie(self, response):
        sel = Selector(response)
        title = ''.join(sel.xpath('//div[@id="watch-headline-title"]/h1[@class="watch-title-container"]/span[@id="eow-title"]/text()').extract())
        publish = ''.join(sel.xpath('//div[@id="watch-uploader-info"]/strong/text()').extract())
        descr = ''.join(sel.xpath('//div[@id="watch-description-text"]/p[@id="eow-description"]/text()').extract())
        nodes = sel.xpath('//div[@id="watch-description-extras"]//li[contains(@class, "watch-meta-item ")]')
        for node in nodes:
            
            runtime = ''.join(node.xpath('./h4[contains(text(), "Running time")]/following-sibling::ul[1]/li/text()').extract())
            
            qry = 'insert into movies(title, publish, descr, runtime, title)values (%s, %s, %s, %s, %s) on duplicate key update title = %s'
            values = (title, publish, descr, runtime, title)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()  
