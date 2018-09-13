from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class HtmlParser(object):
    
    
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile('http://news.qq.com/a/20180905'), target='_blank') #\d+\.htm
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        
        return new_urls
    
    def _get_new_data(self, page_url, soup):
        res_data = {}

        res_data['url'] = page_url
        try:
            title_node = soup.find('div',class_="article-intro").find('h1')
            res_data['title'] = title_node.get_text()

            #基本信息
            detail_node = soup.find('div', class_= "article-body")
            res_data['detail_node'] = detail_node

            summary_node = soup.find('div',class_="article-intro").find('p')
            res_data['summary_node'] = summary_node
        except:
            res_data['title']=None
            res_data['detail_node']=None
            res_data['summary_node']=None

        return res_data

    def parse(self,page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='UTF-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls, new_data
    
    
