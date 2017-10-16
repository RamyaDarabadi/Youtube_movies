from scrapy.spider import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector

class Movies(CrawlSpider):
    name = 'baahubali'
    start_urls = ['https://www.youtube.com/watch?v=GXCVvEskIvo&list=PLVEfGofYqKTThj7lngW5r_DfRlMu-8Kxg']

def parse(self, response):
    sel = Selector(response)
    nodes= sel.xpath('//div[@id="body-container"]//div[@id="page-container"]//div[@id="page"]//div[@id="content"]/')
    for node in nodes:
        title = ''.join(node.xpath('//div[@id="watch7-container"]//div[@id="watch7-main-container"]//div[@id="watch7-main"]//div[@id="watch-header"]//div[@id="watch7-headline"]//div[@id="watch-headline-title"]//h1[@class="watch-title-container"]//span[@id="eow-title"]//text()')).extract()
        link = ''.join(node.xpath('//div[@class="yt-lockup clearfix  yt-lockup-movie yt-lockup-grid"]/div[@class="yt-lockup-thumbnail"]/a/@href')).extract()
        image = ''.join(node.xpath('//div[@class="yt-lockup clearfix  yt-lockup-movie yt-lockup-grid"]/div[@class="yt-lockup-thumbnail"]/span[@class="video-thumb  yt-thumb yt-thumb-196"]/span[@class="yt-thumb-poster"]/span[@class="yt-thumb-clip"]/img/@src')).extract()
        time = ''.join(node.xpath('//div[@class="yt-lockup clearfix  yt-lockup-movie yt-lockup-grid"]/div[@class="yt-lockup-thumbnail"]/span[@class="video-thumb  yt-thumb yt-thumb-196"]/span[@class="yt-thumb-poster"]/span[@class="yt-thumb-clip"]//span[@class="video-time"]')).extract()
        print (title, link, image, time)
