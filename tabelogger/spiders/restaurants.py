import scrapy
import pandas as pd
from bs4 import BeautifulSoup
import glob
import urllib.request as urllib3

####
## This is all from home only
####
# # rest_list = pd.read_csv(r'C:\Users\Andrew\Projects\tabelogger\restaurant_lists\_JP_ 店舗リスト_食べログ_A1301.csv')
# # rest_list = rest_list[:50]['Restaurant_URL'].values.tolist()
# all_files = glob.glob(r'C:\Users\Andrew\Projects\tabelogger\restaurant_lists\_JP*.csv')
# li = []
# for filename in all_files:
#     tmp = pd.read_csv(filename, header=0)
#     li.append(tmp)
# rest_list = pd.concat(li, axis=0, ignore_index=False)
# rest_list = rest_list['Restaurant_URL'].values.tolist()

class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"
    start_urls = [
        'https://tabelog.com/tokyo/A1301/A130101/13143905/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13250239/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13231610/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13170967/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13174746/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13132332/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13098946/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13072926/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13240717/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13096555/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13143836/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13272534/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13235525/dtlmenu/drink/',
        'https://tabelog.com/tokyo/A1301/A130101/13183412/dtlmenu/drink/'
    ]
    # start_urls = [x+'dtlmenu/drink/' for x in rest_list]
    # start_urls.append('https://tabelog.com/tokyo/A1301/A130101/13154719/dtlmenu/drink/')

    # start_urls = rest_list
    custom_settings = {
        'LOG_LEVEL' : 'WARN',
        'FEED_URI' : 'test.json',
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'FEED_FORMAT' : 'json'
    }

    # def start_requests(self):
    #     for URL in self.start_urls:
    #         try:
    #             urllib3.urlopen(URL)
    #         except urllib3.HTTPError:
    #             URL = URL.strip('dtlmenu/drink/')
    #         yield scrapy.Request(url=URL, callback=self.parse)

    #### This doesn't work.
    # def response_parser(self, response):
    #     if response.status == 200:
    #         yield scrapy.Request(url=response.url, callback=self.parse)
    #     else:
    #         yield scrapy.Request(url=response.url.rstrip('dtlmenu/drink/'), callback=self.parse)
            

    def parse(self, response):
        entry_dict = {}

        entry_dict['url'] = response.url

        if response.xpath('//a[contains(@href, "dtlmenu/drink/")]'):
            entry_dict['has_drinks'] = True
            entry_dict['drinks_url'] = response.xpath('//a[contains(@href, "dtlmenu/drink/")]').attrib['href']
            # entry_dict['drinks_hmtl'] = response.css('div.rstdtl-menu-lst').get()
        else:
            entry_dict['has_drinks'] = False

        #### this isn't the same on pages with drinks (for some reason)
        # entry_dict['display_name'] = response.css('h2.display-name span::text').extract()[0].strip()
        entry_dict['display_name'] = response.css('h2.display-name > *::text').extract()[0].strip()
        if response.css('span.alias::text'):
            entry_dict['display_alias'] = response.css('span.alias::text').extract()[0].strip()
        if response.css('span.pillow-word::text'):
            entry_dict['display_pillow'] = response.css('span.pillow-word::text').extract()[0].strip()
        entry_dict['rating'] = response.css('span.rdheader-rating__score-val-dtl::text').extract()[0]
        entry_dict['reviewers'] = response.css('span.rdheader-rating__review-target .num::text').extract()[0]
        entry_dict['savers'] = response.css('span.rdheader-rating__hozon-target .num::text').extract()[0]

        headerbox = response.css('div.rdheader-info-box dl')
        for row in headerbox:
            if row.css('div.linktree__parent'):
                entry_dict[row.css('dt.rdheader-subinfo__item-title::text').extract()[0].strip('：')+'_header'] = \
                    row.css('dd').css('div.linktree__parent span.linktree__parent-target-text::text').extract_first()
            else:
                entry_dict[row.css('dt.rdheader-subinfo__item-title::text').extract()[0].strip().strip('：')+'_header'] = \
                    BeautifulSoup(row.css('dd').get(), 'html.parser').get_text().replace('\n', ' ').strip()

        tables = response.css('div.rstinfo-table tr')
        for row in tables:
            entry_dict[row.css('th::text').extract()[0].replace('\n',' ').strip()] = \
                BeautifulSoup(row.css('td').get(), 'html.parser').get_text()

        #### add code for getting the raw html of full page
        # entry_dict['raw_html'] = response.body.get()

        print('.',end="",flush=True)
        yield entry_dict

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print('\n\n\tTotal run time: ', finish_time - start_time)
