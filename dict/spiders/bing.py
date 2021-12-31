import scrapy


class BingSpider(scrapy.Spider):
    name = 'bing'
    allowed_domains = ['cn.bing.com']

    def start_requests(self):
        url = 'https://cn.bing.com/dict/search?q={}'.format(self.search, callback=self.parse)
        yield scrapy.Request(url=url)

    def parse(self, response):
        pronunciation = ', '.join([i.strip().replace('\xa0',' ') for i in response.css(".hd_p1_1 .b_primtxt::text").getall()])
        paraphrase = '\n'.join([':'.join(i.css("::text").getall()) for i in response.css(".qdef li")])
        extra = response.css(".hd_if").xpath("string()").get().replace('\xa0\xa0','\n')
        yield {
            # 'search': response.css("h1::text").get(),
            'pronunciation': pronunciation,
            'paraphrase': paraphrase,
            'extra': extra,
        }
