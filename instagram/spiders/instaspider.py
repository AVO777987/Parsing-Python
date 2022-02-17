import scrapy
from scrapy.http import HtmlResponse
import re


class InstaspiderSpider(scrapy.Spider):
    name = 'instaspider'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'dronru777'
    inst_pass = '#PWD_INSTAGRAM_BROWSER:10:1644948001:AYFQAGiGihvwObRb+mFM/htSvnpVRJp7aUE7Y7hy/ST+DfogR7OKkanw3K8Gr+/2t6Tlqv7uWWq2qd6HozAejwRxvdL7nQzYAI12tyKqmehCEeg6HVwT56NTH5+WqZ+85EZXnS3ZRU8z5Z0W'
    user_parse = ['fcsm_official', 'pfc_cska']

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pass},
                                 headers={'X-CSRFToken': csrf_token}
                                 )
        pass

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            for user in self.user_parse:
                yield response.follow(
                    f'/{user}/',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        print()

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
