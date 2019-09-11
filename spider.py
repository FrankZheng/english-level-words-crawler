# -*- coding: UTF-8 -*-


import scrapy
import urlparse as parse


def utftxt(node):
    return node.get().encode('utf-8')


def level_urls(url_prefix):
    return [url_prefix + str(i) for i in range(1, 14)]


def parse_url_level(url):
    params = parse.parse_qs(parse.urlsplit(url).query)
    return int(params['level'][0])


class LevelWordsSpider(scrapy.Spider):
    name = "English Level Words"

    start_urls = level_urls('http://word.qsbdc.com/wl.php?level=')

    def parse(self, response):
        level = parse_url_level(response.url)
        lines = response.xpath('//table[@class="table_solid"]/tr')
        length = len(lines)
        # 0,1 header
        for i in range(2, length-1):
            line = lines[i]
            word = line.css('span.hidden_1_1::text')
            soundmark = line.css('span.hidden_2_1::text')
            explaination = line.css('span.hidden_3_1::text')
            examples = line.css('a.mytitle::attr("title")')
            yield {
                'word': utftxt(word),
                'soundmark': utftxt(soundmark),
                'explaination': utftxt(explaination),
                'examples': utftxt(examples),
                'level': level,
            }
        # the last line controls
        last = lines[-1]
        for link in last.css('a'):
            linkTxt = link.css('::text').get()
            if linkTxt == u'下一页>':
                href = link.css('::attr("href")').get()
                if href is not None:
                    yield response.follow(href, self.parse)
