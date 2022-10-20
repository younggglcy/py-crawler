from crawler import crawl
from data import process
from os import path, remove
from csv import DictWriter

def init():
  if path.exists('books.csv'):
    remove('books.csv')
  if path.exists('comments.csv'):
    remove('comments.csv')
  with open('books.csv', 'x') as f1:
    writer = DictWriter(f1, (
      'authors',
      'name',
      'cover_url',
      'intro',
      'link',
      'score'
    ))
    writer.writeheader()
  with open('comments.csv', 'x') as f2:
    writer = DictWriter(f2, ('recommended_level', 'user_name', 'comment'))
    writer.writeheader()

if __name__ == '__main__':
  init()
  crawl()
  process()
