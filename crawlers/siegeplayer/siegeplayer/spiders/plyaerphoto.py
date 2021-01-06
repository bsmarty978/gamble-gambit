import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class PlyaerphotoSpider(CrawlSpider):
    name = 'plyaerphoto'
    allowed_domains = ['siege.gg']
    unique_data = set()
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://siege.gg/matches?tab=results', headers={
        'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='results']/a"), callback='parse_item', follow=True, process_request='set_user_agent'), #for every match
        Rule(LinkExtractor(restrict_xpaths="//a[@rel='next']"), process_request='set_user_agent'),    #for next page
    )

    def set_user_agent(self, request):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        # team1 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text())").get() #team 1 data left side
        # team2 = response.xpath("normalize-space(//div[@class='h1 pg-title impact__title mb-3']/text()[2])").get()

        roster = response.xpath("//div[@class='roster__player']")
        for player in roster:
            name = player.xpath("normalize-space(.//h5/text())").get()
            if name not in (self.unique_data):
                self.unique_data.add(name)  
                photo = player.xpath(".//img[@class='player__photo__img img-fluid']/@src").get()
                yield{
                    # 'name' : name,
                    # 'photo' : photo,
                    name : photo
                }

        # yield{
        #     'title': team1 + ' vs ' +  team2,
        #     'team-a': team1,
        #     'team-b': team2,
        #     'roster' : {
        #         team1 : response.xpath("//div[@class='col-12 col-md match__roster team--a']//h5/text()").getall(),
        #         team2 : response.xpath("//div[@class='col-12 col-md match__roster team--b']//h5/text()").getall()
        #         },
        # }