from requests import RequestException, get
from urllib.parse import urljoin
import logging
from bs4 import BeautifulSoup
from agent import get_random_user_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

url = 'https://book.douban.com/top250'

def crawl_single_url(url:str):
  try:
    res = get(url, headers={
      'User-Agent': get_random_user_agent()
    })
    if res.status_code == 200:
      soup = BeautifulSoup(res.text, 'html.parser')
      items = soup.select('div.indent table tr.item')
      for item in items:
        # 封面url
        cover_url = item.find('a', { 'class': 'nbg' }).find('img')['src']
        # 书名
        raw_name = item.find('div', { 'class': 'pl2' }).find('a').get_text().strip()
        book_name = ''
        for ch in raw_name:
          if not (ch == ' ' or ch == '\n'):
            book_name += ch
        # 作者
        infos = item.find('p', { 'class': 'pl' }).get_text().split('/')
        authors = []
        for i in infos:
          if i.find('出版') != -1 or i.find('书店') != -1:
            break
          authors.append(i)
        #评分
        score = item.find('span', { 'class': 'rating_nums' }).get_text()
        # 引言
        intro_span = item.find('span', { 'class': 'inq' })
        intro = None
        if intro_span:
          intro = intro_span.get_text()
        # 详情页链接
        link = item.find('a', { 'class': 'nbg' })['href']
    elif res.status_code >= 400 and res.status_code < 500:
      logging.error('request error')
  except RequestException as e:
    logging.error('request exception: {0}'.format(e))

def crawl():
  for i in range(10):
    page_url = urljoin(url, '?start={0}'.format(i * 25))
    logging.info('start crawling {0}'.format(page_url))
    crawl_single_url(page_url)
  logging.info('finish crawling')

crawl()
