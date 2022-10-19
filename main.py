from crawler import crawl
from data import process
from os import path, remove

if __name__ == '__main__':
  if path.exists('books.csv'):
    remove('books.csv')
  if path.exists('comments.csv'):
    remove('comments.csv')
  crawl()
  process()
