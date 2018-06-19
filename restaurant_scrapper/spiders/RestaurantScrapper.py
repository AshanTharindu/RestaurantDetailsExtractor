#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 16:47:53 2018

@author: ashan
"""

import scrapy

class RestaurantScraper(scrapy.Spider):
    name = "restaurants"

    def start_requests(self):
        urls = [
            'https://www.yamu.lk/place/restaurants?page=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for restaurant in response.css(
                'a.front-group-item::attr(href)').extract():
            yield response.follow(restaurant, self.parse_restaurant)

        next_page = response.css('li.active+li a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    
    def parse_restaurant(self, response):
        
        restaurant_name = response.css('div.place-title-box h2::text').extract_first()
        address = response.css('div.place-title-box p.addressLine::text').extract_first()
        call = response.css('div.time-range a.closed::text').extract_first()
        if(call[0]=="C"):
            call = call[5:]
        excerpt = response.css('div.place-title-box p.excerpt::text').extract_first()
        
        yield {
            'Restaurant_name': restaurant_name,
            'Address': address,
            'Call': call,
            'Excerpt': excerpt,
            'Cuisine / Price / Dishes': response.css('div.row div.col-md-6:nth-child(2) a.lbl::text').extract(),
            'Open_Time': response.css('p.open::text').extract_first()
        }
        

        
