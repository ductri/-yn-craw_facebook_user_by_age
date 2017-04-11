import scrapy
from scrapy import FormRequest
from scrapy import log
from scrapy.http import Request

import config


class FacebookSpider(scrapy.Spider):
    name = 'fb_spider'
    start_urls = ['https://www.facebook.com/login.php']
    age = 22

    def parse(self, response):
        return [FormRequest.from_response(response,
                                          formdata={'email': config.get_email(), 'pass': config.get_pass()}, callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.DEBUG)
            return
        else:
            self.log('Login successfully', level=log.DEBUG)
            yield Request(url="https://www.facebook.com/search/%s/users-age" % self.age, callback=self.search_user)

    def search_user(self, response):
        filename = 'fb_search_age.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(response.css('body').extract_first(), level=log.DEBUG)