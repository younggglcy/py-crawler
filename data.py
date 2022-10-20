import re
from typing import Any, List, Dict
from string import punctuation
from nltk.corpus import stopwords
from csv import DictReader
from wordcloud import WordCloud
from jieba import cut
from jieba.analyse import extract_tags

def process():
  comments = get_all_comments()
  s: str = comments['content']
  # 分词
  tokens = tokenize(s)
  # 清除标点、空白字符，统一小写
  tokens = standardize(tokens)
  # 去除停用词
  tokens = clear_stopwords(tokens)
  # 基于 TF-IDF 提取关键词, 暂定为前100个
  keywords = extract_tags(" ".join(tokens), topK = 100)
  # 词云
  process_wordcloud(keywords)
  return 

def tokenize(s: str):
  return list(','.join(cut(s)).split(','))

def standardize(tokens: List[str]) -> List[str]:
  punctuation_pattern = re.compile('[%s]' % re.escape(punctuation))
  ret = []
  for token in tokens:
    if not (token.lstrip() == '' or re.match(punctuation_pattern, token)):
      ret.append((re.sub('\s', '', token)).lower())
  return ret

def clear_stopwords(tokens: List[str]) -> List[str]:
  words: List[str] = stopwords.words('chinese') + stopwords.words('english')
  return [token for token in tokens if not token in words]

def get_all_comments() -> Dict[str, Any]:
  ret = ''
  nums = 0
  with open('comments.csv', 'r') as f:
    reader = DictReader(f)
    for row in reader:
      ret += row['comment']
      # ret += '\n'
      nums += 1
  return {
    'content': ret,
    'nums': nums,
  }

def process_wordcloud(keywords: List[str]):
  print(keywords)
  WordCloud(
    background_color='white',
  ).generate(' '.join(keywords)).to_file('wordcloud.png')
