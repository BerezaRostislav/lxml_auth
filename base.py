# -*- coding: utf-8 -*-

import requests
from lxml import html
from lxml import cssselect
from lxml.etree import ElementTree
from urllib.request import urlopen


class BaseSpider(object):
    USERNAME = 'mechdrives'
    PASSWORD = 'MEC002'
    USERAGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 \
    Safari/537.36'
    base_url='http://store.climaxmetal.com/'
    def __init__(self, username='', password='', **kwargs):
        self.logged_in = False
        self._session = None
        if username and password:
            self.USERNAME = username
            self.PASSWORD = password
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            self._session.verify = False
            self._session.headers = {'User-Agent': self.USERAGENT}
        return self._session

    def get(self, url, *args, **kwargs):
        resp = self.session.get(url, *args, **kwargs)
        return resp

    def get_x(self, url, *args, **kwargs):
        kwargs.setdefault('timeout', 60)
        page = self.get(url, *args, **kwargs)
        if page.status_code == 200:
            x = html.fromstring(page.content)
            x.make_links_absolute(url)
            return x
        return None

    def post(self, url, data, *args, **kwargs):
        kwargs.setdefault('timeout', 60)
        resp = self.session.post(url, data, *args, **kwargs)
        return resp

    def post_x(self, url, data, *args, **kwargs):
        page = self.post(url, data, *args, **kwargs)
        x = html.fromstring(page.content)
        x.make_links_absolute(url)
        return x

    def get_form_data(self, x, form_xpath):
        res = {}
        for el in x.xpath(form_xpath + "//input"):
            name = el.attrib.get('name')
            if name:
                res[name] = el.attrib.get('value', '')
        return res


    #__EVENTVALIDATION:!!!! value

    def login(self, *args, **kwargs):
        url = self.base_url+'Default.aspx'
        login_elems = self.get(url)
        elems = html.fromstring(login_elems.text)
        view_stage = elems.find('.//input[@name="__VIEWSTATEGENERATOR"]').value
        event_validation = elems.find('.//input[@name="__EVENTVALIDATION"]').value
        view_state = elems.find('.//input[@name="__VIEWSTATE"]').value
        event_argument = elems.find('.//input[@name="__EVENTARGUMENT"]').value
        event_target = elems.find('.//input[@name="__EVENTTARGET"]').value
        params = {
            '__EVENTTARGET' : event_target,
            '__EVENTARGUMENT' : event_argument,
            '__VIEWSTATE' : view_state,
            '__VIEWSTATEGENERATOR' : view_stage,
            '__EVENTVALIDATION' : event_validation,
            'ctl00$cntMain$TXTGLOBALUSERNAME3':'mechdrives',
            'ctl00$cntMain$TXTGLOBALPASSWORD2':'MEC002',
            'ctl00$cntMain$BTNGLOBALLOGIN1':'Login'

        }
        auth=self.post(url,params)
        # catalog = 'http://store.climaxmetal.com/ProductDetails.aspx?item_no=RC-150-S++++++++++++++++++++++++++++++++++++++++++'
        # raw_catalog = self.get(catalog).text
        # print(raw_catalog)
        # return auth

    def product_catalog(self, *args, **kwargs):
         self.login()
         # catalog = 'http://store.climaxmetal.com/ProductDetails.aspx?item_no=RC-150-S++++++++++++++++++++++++++++++++++++++++++'
         catalog = 'http://store.climaxmetal.com/productlisting.aspx'
         raw_catalog = self.get(catalog)
         elems_catalog = html.fromstring(raw_catalog.text)
         raw_data = elems_catalog.find_class('rgMasterTable')
         print(raw_catalog.text)

if __name__ == '__main__':
    BaseSpider = BaseSpider()
    BaseSpider.product_catalog()
