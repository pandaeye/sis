# coding:utf-8
import scrapy
from sis_spider.items import SisSpiderItem
import logging

logger = logging.getLogger('url')
formatter = logging.Formatter('%(message)s')
fh = logging.FileHandler('url.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.ERROR)

class sis_for(scrapy.Spider):
    name = "sis_for"
    allowed_domains = ['38.103.161.157']
    
    """开始抓取"""
    def start_requests(self):
        print '======================================'
        
        #url_list = []
        nPageStart =1
        nPageEnd = 3001
        for i in range(nPageStart,nPageEnd+1):
            sUrl = 'http://38.103.161.157/forum/forum-230'+ str(i) +'.html'
            yield scrapy.Request(url=sUrl,callback=self.parse)
    def parse(self, response):
        if response.status == 404:
            logger.error(response.url)
        sUrl = response.url
        sUrl = sUrl[0:sUrl.rfind('/')] + '/'
        papers1 = response.xpath("//tbody")
        print '+++++++++++++++++++++++++++++++++++++++'
        print response.url
        i = 0
        for paper in papers1:
            #print paper
            i = i +1
            #print '-------------------------------------------'
            #print paper
            papers2 = paper.xpath(".//span[not(@class)]")
            if papers2:
                #print papers2
                title = papers2[0].xpath(".//a/text()").extract()
                addr = papers2[0].xpath(".//a/@href").extract()
                #    print i,title[0]
                #    print i,sAddr
                if addr and title:
                    sAddr = sUrl+addr[0].encode("utf8")
                    item = SisSpiderItem(title = title[0],addr = sAddr)#.encode("utf8")
                    yield item
    def closed(self, response):
        pass
class sis_spider(scrapy.Spider):
  name = "sis"
  allowed_domains = ["38.103.161.157"]
  handle_httpstatus_list = [301,302,204,206,404,500]
  start_urls = ["http://38.103.161.157/forum/forum-143-1.html"]
  #http://38.103.161.157/forum/forum-230-1.html
  #http://38.103.161.157/forum/forum-58-1.html
  #http://38.103.161.157/forum/forum-25-1.html
  def parse(self, response):
    if response.status == 404:
        print '=================================='
    sUrl = response.url
    sUrl = sUrl[0:sUrl.rfind('/')] + '/'
    #print sUrl
    papers1 = response.xpath("//tbody")
    #print '+++++++++++++++++++++++++++++++++++++++'
    i = 0
    for paper in papers1:
        #print paper
        i = i +1
        #print '-------------------------------------------'
        #print paper
        papers2 = paper.xpath(".//span[not(@class)]")
        if papers2:
            #print papers2
            title = papers2[0].xpath(".//a/text()").extract()
            addr = papers2[0].xpath(".//a/@href").extract()
            #    print i,title[0]
            #    print i,sAddr
            if addr and title:
                sAddr = sUrl+addr[0].encode("utf8")
                item = SisSpiderItem(title = title[0],addr = sAddr)#.encode("utf8")
                yield item
    next_page = response.xpath("//a[@class='next']/@href").extract()
    if next_page:
        strNextPage = sUrl + next_page[0]
        print '-------------------------------------------'
        print strNextPage
        yield scrapy.Request(url=strNextPage,callback=self.parse,errback=self.Error_info)
  def Error_info(self, failure):
      response = failure.value.response
      print '++++++++++++++++++++++++++++++++++++++'
      print response.url
