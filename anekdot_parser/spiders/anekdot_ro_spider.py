import scrapy
import numpy as np
import pandas as pd
from urllib.parse import urlparse
import logging
import emoji


class AnekdotRuSpider(scrapy.Spider):
    name = "anekdot_ru"

    def start_requests(self):
        logging.warning(emoji.emojize("--> :thumbs_up: Reached start"))
        start_urls = []
        for i in range(1, 13):
            i = str(i)
            if len(i) == 1:
                i = '0' + i
            for j in range(1, 29):
                j = str(j)
                if len(j) == 1:
                    j = '0' + j
                start_urls.append('https://www.anekdot.ru/best/anekdot/' + i + j + '/')
        for url in start_urls:
            yield scrapy.Request(url, self.parse_date)


    # Parse particular date
    def parse_date(self, response):
        logging.warning(emoji.emojize("--> Reached data page"))
        parameters = ['']
        for i in range(2, 11):
            parameters.append("?page=" + str(i))
        for parameter in parameters:
            yield scrapy.Request((response.request.url + parameter), self.parse_page)


    # Parse particular page
    def parse_page(self, response):
        logging.warning(emoji.emojize("--> Reached page with anekdots"))
        anekdot_elements = response.css("div.text")
        logging.warning(emoji.emojize("💼 Got a pack of anekdots"))
        for anekdot in anekdot_elements:
            logging.warning(emoji.emojize("😂👌 Wrote one to CSV"))
            yield {
                    'text': ' '.join(anekdot.css("::text").extract())
            }
