# -*- coding: utf-8 -*-

from scrapy import Spider, Request, Item, Field
from ..items import PersonItem
import time

class RaceItem(Item):
    year = Field()
    year_url = Field()
    winner_url = Field()
    race_map = Field()
    src_racemap = Field()
    winner_photo = Field()
    winner_flag = Field()
    winner_name = Field()
    climber_url = Field()
    climber_photo = Field()
    climber_flag = Field()
    climber_name = Field()
    sprinter_url = Field()
    sprinter_photo = Field()
    sprinter_flag = Field()
    sprinter_name = Field()
    young_url = Field()
    young_photo = Field()
    young_flag = Field()
    young_name = Field()
    # url = Field()

class MyScraper(Spider):
    name = u'myscraper'


    def start_requests(self):
        # First request
        yield Request('https://fr.wikipedia.org/wiki/Palmarès_du_Tour_de_France', self.parse,)




    def parse(self, response):
        # Find a list of div which contains a person (use CSS)
        table = response.xpath('//*[@id="mw-content-text"]/table[1]')



        for i,tr in enumerate(table.css('tr')):
            time.sleep(0.25)
            if i > 85 and i <=150:
                url = tr.xpath('td[1]//a//@href').extract()
                url_winner = tr.xpath('td[2]/a//@href | td[2]/span[@class="nowrap"]/a//@href').extract()
                winner_flag = tr.xpath('td[2]//a//img//@src').extract()
                winner_name = tr.xpath('td[2]/a//text()').extract()
                url_climber = tr.xpath('td[7]/a//@href | td[7]/span[@class="nowrap"]/a//@href').extract()
                climber_flag = tr.xpath('td[7]//a//img//@src').extract()
                climber_name = tr.xpath('td[7]/a//text() | td[7]/span/a//text()').extract()
                url_sprinter = tr.xpath('td[8]/a//@href | td[8]/span[@class="nowrap"]/a//@href').extract()
                sprinter_flag = tr.xpath('td[8]//a//img//@src').extract()
                sprinter_name = tr.xpath('td[8]/a//text() | td[8]/span/a//text()').extract()
                url_young = tr.xpath('td[9]/a//@href | td[9]/span[@class="nowrap"]/a//@href').extract()
                young_flag = tr.xpath('td[9]//a//img//@src').extract()
                young_name = tr.xpath('td[9]/a//text() | td[9]/span/a//text()').extract()
                url_str = 'https://fr.wikipedia.org' + str(url[0])
                
                if url_winner:
                    url_str_winner = 'https://fr.wikipedia.org' + str(url_winner[0])
                else:
                    url_str_winner =''
                if url_climber:
                    url_str_climber = 'https://fr.wikipedia.org' + str(url_climber[0])
                else:
                    url_str_climber =''
                if url_sprinter:
                    url_str_sprinter = 'https://fr.wikipedia.org' + str(url_sprinter[0])
                else:
                    url_str_sprinter =''
                if url_young:
                    url_str_young = 'https://fr.wikipedia.org' + str(url_young[0])
                else:
                    url_str_young =''
                year = tr.xpath('td[1]//a//text()[1]').extract()
                request = Request(url_str, callback=self.parse_url)
                request.meta['item'] = RaceItem()
                items_ = request.meta['item']
                items_['year']  = year
                items_['year_url']  = url_str
                items_['winner_url']  = url_str_winner
                items_['winner_flag']  = winner_flag
                items_['winner_name']  = winner_name
                items_['climber_url']  = url_str_climber
                items_['climber_flag']  = climber_flag
                items_['climber_name']  = climber_name
                items_['sprinter_url']  = url_str_sprinter
                items_['sprinter_flag']  = sprinter_flag
                items_['sprinter_name']  = sprinter_name
                items_['young_url']  = url_str_young
                items_['young_flag']  = young_flag
                items_['young_name']  = young_name
                yield request



    def parse_url(self, response):
        infobox = response.xpath('//*[@id="mw-content-text"]//div[@class="infobox_v3"][1]')
        race_map = infobox.xpath('//div[@class="images"][1]//a[@class="image"][1]//img')
        if response.meta['item']['winner_url'] == '':
        	request = Request(response.meta['item']['climber_url'], callback=self.parse_url_climber)
        else:
        	request = Request(response.meta['item']['winner_url'], callback=self.parse_url_winner)
        request.meta['item']  = response.meta['item']
        request.meta['item']['race_map'] = race_map.extract()
        request.meta['item']['src_racemap'] = race_map.xpath('@src').extract()
        yield request


    def parse_url_winner(self, response):
        item = response.meta['item']
        infobox = response.xpath('//*[@id="mw-content-text"]//div[@class="infobox_v3"][1]')
        winner_photo = infobox.xpath('//div[@class="images"][1]//a[@class="image"][1]//img')
        item['winner_photo'] = winner_photo.xpath('@src').extract()
        if item['climber_url'] != '' :
            request = Request(item['climber_url'], callback=self.parse_url_climber)
            request.meta['item']  = item
            yield request
        else:
            yield item

    def parse_url_climber(self, response):
        item = response.meta['item']
        infobox = response.xpath('//*[@id="mw-content-text"]//div[@class="infobox_v3"][1]')
        climber_photo = infobox.xpath('//div[@class="images"][1]//a[@class="image"][1]//img')
        item['climber_photo'] = climber_photo.xpath('@src').extract()
        if item['sprinter_url'] != '' :
            request = Request(item['sprinter_url'], callback=self.parse_url_sprinter)
            request.meta['item']  = item
            yield request
        else:
            yield item


    def parse_url_sprinter(self, response):
        item = response.meta['item']
        infobox = response.xpath('//*[@id="mw-content-text"]//div[@class="infobox_v3"][1]')
        sprinter_photo = infobox.xpath('//div[@class="images"][1]//a[@class="image"][1]//img')
        item['sprinter_photo'] = sprinter_photo.xpath('@src').extract()
        if item['young_url'] != '' :
            request = Request(item['young_url'], callback=self.parse_url_young)
            request.meta['item']  = item
            yield request
        else:
            yield item


    def parse_url_young(self, response):
        item = response.meta['item']
        infobox = response.xpath('//*[@id="mw-content-text"]//div[@class="infobox_v3"][1]')
        young_photo = infobox.xpath('//div[@class="images"][1]//a[@class="image"][1]//img')
        item['young_photo'] = young_photo.xpath('@src').extract()
        yield item