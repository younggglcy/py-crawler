from requests import RequestException
from urllib.parse import urljoin
import logging
from bs4 import BeautifulSoup as bs
from request import req
from data import process
from csv import DictWriter
from os import path, remove
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

url = 'https://book.douban.com/top250'

def crawl_comments(_url:str):
  for i in range(25):
    page_url = urljoin(_url, '?start={0}'.format(20 * i))
    try:
        logging.info('start crawling comments for {0}'.format(page_url))
        res = req(url=page_url)
        if res:
          with open('comments.csv', 'a') as f:
            writer = DictWriter(f, ('recommended_level', 'user_name', 'comment'))
            writer.writeheader()
            soup = bs(res.text, 'html.parser')
            comments_lists = soup.find_all('div', { 'class': 'comment' })
            for item in comments_lists:
              # 推荐等级
              recommended_level = item.find('span', { 'class': 'comment-vote' }).find('a').text
              # 用户名
              user_name = item.find('span', { 'class': 'comment-info' }).find('a').text
              # 短评
              comment = item.find('span', { 'class': 'short' }).text
              dict = {
                'recommended_level': recommended_level,
                'user_name': user_name,
                'comment': comment
              }
              writer.writerow(dict)
        else:
          break
    except RequestException as e:
      logging.error('request exception: {0}'.format(e))
    finally:
      sleep(2)

def crawl_single_url(_url:str):
  try:
    res = req(
      url = _url,
    )
    if res:
      with open('books.csv', 'a') as book_f:
        writer = DictWriter(book_f, (
          'authors',
          'name',
          'cover_url',
          'intro',
          'link',
          'score'
        ))
        writer.writeheader()
        soup = bs(res.text, 'html.parser')
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
          authors = ''
          for i in infos:
            if i.find('出版') != -1 or i.find('书店') != -1:
              break
            authors += ' '
            authors += i
          #评分
          score = item.find('span', { 'class': 'rating_nums' }).get_text()
          # 引言
          intro_span = item.find('span', { 'class': 'inq' })
          intro = None
          if intro_span:
            intro = intro_span.get_text()
          # 详情页链接
          link = item.find('a', { 'class': 'nbg' })['href']
          dict = {
            'authors': authors,
            'name': book_name,
            'cover_url': cover_url,
            'intro': intro,
            'link': link,
            'score': score
          }
          writer.writerow(dict)
          crawl_comments(urljoin(link, 'comments/'))   
    else:
      return
  except RequestException as e:
    logging.error('request exception: {0}'.format(e))
  finally:
    sleep(2)

def crawl():
  for i in range(10):
    page_url = urljoin(url, '?start={0}'.format(i * 25))
    logging.info('start crawling {0}'.format(page_url))
    crawl_single_url(page_url)
  logging.info('finish crawling')

if __name__ == '__main__':
  if path.exists('books.csv'):
    remove('books.csv')
  if path.exists('comments.csv'):
    remove('comments.csv')
  crawl()
  process()
