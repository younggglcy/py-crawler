import re
from typing import Any, List, Dict
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from csv import DictReader
from nltk import FreqDist
from math import log
from wordcloud import WordCloud

def process():
  comments = get_all_comments()
  s = comments['content']
  nums = comments['nums']
  reader = comments['reader']
  # 分词
  # tokens = word_tokenize(s, 'chinese')  # 暂时没有支持 chinese
  tokens = word_tokenize(s)
  # 清除标点、空白字符，统一小写
  tokens = standardize(tokens)
  # 去除停用词
  tokens = clear_stopwords(tokens)
  # 词干提取
  tokens = process_stem(tokens)
  # 基于 TF-IDF 提取关键词, 暂定为前100个
  keywords = extract_keywords(tokens, reader, nums)
  # 词云
  process_wordcloud(keywords)
  return 

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

def process_stem(tokens: List[str]) -> List[str]:
  s = PorterStemmer()
  return [s.stem(token) for token in tokens]

def get_all_comments() -> Dict[str, Any]:
  ret = ''
  nums = 0
  with open('comments.csv', 'r') as f:
    reader = DictReader(f)
    for row in reader:
      ret += row['comment']
      ret += '\n'
      nums += 1
  return {
    'content': ret,
    'nums': nums,
    'reader': reader
  }

def extract_keywords(tokens: List[str], reader, nums) -> List[str]:
  # 计算 TF
  freq = FreqDist(tokens)
  # 计算 IDF
  # 总文件(评论)数目除以包含该词语之文件(评论)的数目，再将得到的商取对数得到

  def calc(s: str) -> float:
    comments_nums = 0
    for row in reader:
      if row['comment'].find(s) != -1:
        comments_nums += 1
    return log(nums / comments_nums)

  res = {}
  for key, val in freq.items():
    res.update({
      key: val * calc(key)
    })
  res = sorted(res.items, key=lambda item:item[1], reverse=True)

  ret = {}
  for key, val in ret.items():
    if len(ret) <= 100:
      ret.update({ key: val})
    else:
      break

  return list(ret.keys())

def process_wordcloud(keywords: List[str]):
  wc = WordCloud().generate(keywords).to_file('workcloud')
