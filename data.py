import re
from typing import List
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from csv import DictReader

def process():
  s = get_all_comments()
  # 分词
  # tokens = word_tokenize(s, 'chinese')  # 暂时没有支持 chinese
  tokens = word_tokenize(s)
  # 清除标点，统一小写
  tokens = standardize(tokens)
  # 去除停用词
  tokens = clear_stopwords(tokens)
  # 词干提取
  tokens = process_stem(tokens)
  return tokens

def standardize(tokens: List[str]) -> List[str]:
  punctuation_pattern = re.compile('[%s]' % re.escape(punctuation))
  ret = []
  for token in tokens:
    if not (token == ' ' or re.match(punctuation_pattern, token)):
      ret.append(token.lower())
  return ret

def clear_stopwords(tokens: List[str]) -> List[str]:
  words: List[str] = stopwords.words('chinese') + stopwords.words('english')
  return [token for token in tokens if not token in words]

def process_stem(tokens: List[str]) -> List[str]:
  s = PorterStemmer()
  return [s.stem(token) for token in tokens]

def get_all_comments() -> str:
  ret = ''
  with open('comments.csv', 'r') as f:
    reader = DictReader(f, 'comment')
    for row in reader:
      ret += row
  return ret
