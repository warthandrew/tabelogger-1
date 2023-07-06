import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as urllib3

def url_level(url):
    url = url[20:]
    if url[-1] == '/':
        url = url[:-1]
    url = url.split('/')

    return (len(url),dict(zip(range(len(url)), url)))
url_level('https://tabelog.com/osaka/')
url_level('https://tabelog.com/osaka/A2701/A270206')
url_level('https://tabelog.com/osaka/A2701/A270206/27008417/')



class KansaiSpider(scrapy.Spider):
    name = 'kansai'
    allowed_domains = ['tabelog.com']
    # start_urls = ['https://tabelog.com/osaka/',
    #               'https://tabelog.com/kyoto/',
    #               'https://tabelog.com/hyogo/',
    #               'https://tabelog.com/kanagawa/']
    start_urls = ['https://tabelog.com/osaka/']
    # start_urls = ['https://tabelog.com/osaka/A2701/A270206/27008417/']

    custom_settings = {
        'LOG_LEVEL' : 'WARN',
        'FEED_URI' : 'kansai_out.json',
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'FEED_FORMAT' : 'json'
    }

    ###notes for parse_subregion
    # pref level
    # response.xpath('//div[@id="js-leftnavi-area-panels"]/div[@id="tabs-panel-balloon-pref-area"]/div/ul/li/a')
    # regional level
    # response.xpath('//div[@id="js-leftnavi-area-balloon"]/div[@id="js-leftnavi-area-scroll"]/div/ul/li/a')
    # navi_count = int(response.css('div.navi-count a strong::text').extract()[0].replace(',',''))
    



    def parse(self, response):

        le = LinkExtractor(
            allow_domains=self.allowed_domains,
            restrict_xpaths=[
                '//div[@id="js-leftnavi-area-panels"]/div[@id="tabs-panel-balloon-pref-area"]/div/ul/li',
                # '//div[@id="js-leftnavi-area-balloon"]/div[@id="js-leftnavi-area-scroll"]/div/ul/li'
            ]
        )

        for link in le.extract_links(response):
            link_list = {}
            link_list['url'] = link.url
            yield link_list

        # entry_dict = {}

        # entry_dict['url'] = response.url
        # if response.xpath('//a[contains(@href, "dtlmenu/drink/")]'):
        #     entry_dict['has_drinks'] = True
        #     entry_dict['drinks_url'] = response.xpath('//a[contains(@href, "dtlmenu/drink/")]').attrib['href']
        #     # entry_dict['drinks_hmtl'] = response.css('div.rstdtl-menu-lst').get()
        # else:
        #     entry_dict['has_drinks'] = False

        # #### this isn't the same on pages with drinks (for some reason)
        # # entry_dict['display_name'] = response.css('h2.display-name span::text').extract()[0].strip()
        # entry_dict['display_name'] = response.css('h2.display-name > *::text').extract()[0].strip()
        # if response.css('span.alias::text'):
        #     entry_dict['display_alias'] = response.css('span.alias::text').extract()[0].strip()
        # if response.css('span.pillow-word::text'):
        #     entry_dict['display_pillow'] = response.css('span.pillow-word::text').extract()[0].strip()
        # entry_dict['rating'] = response.css('span.rdheader-rating__score-val-dtl::text').extract()[0]
        # entry_dict['reviewers'] = response.css('span.rdheader-rating__review-target .num::text').extract()[0]
        # entry_dict['savers'] = response.css('span.rdheader-rating__hozon-target .num::text').extract()[0]

        # headerbox = response.css('div.rdheader-info-box dl')
        # for row in headerbox:
        #     if row.css('div.linktree__parent'):
        #         entry_dict[row.css('dt.rdheader-subinfo__item-title::text').extract()[0].strip('：')+'_header'] = \
        #             row.css('dd').css('div.linktree__parent span.linktree__parent-target-text::text').extract_first()
        #     else:
        #         entry_dict[row.css('dt.rdheader-subinfo__item-title::text').extract()[0].strip().strip('：')+'_header'] = \
        #             BeautifulSoup(row.css('dd').get(), 'html.parser').get_text().replace('\n', ' ').strip()

        # tables = response.css('div.rstinfo-table tr')
        # for row in tables:
        #     entry_dict[row.css('th::text').extract()[0].replace('\n',' ').strip()] = \
        #         BeautifulSoup(row.css('td').get(), 'html.parser').get_text()

        # print('.',end="",flush=True)
        # yield entry_dict

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print('\n\n\tTotal run time: ', finish_time - start_time)