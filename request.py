import logging
from requests import RequestException, get, Session
import random
from bs4 import BeautifulSoup as bs
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# inspired by https://www.thepythoncode.com/article/using-proxies-using-requests-in-python
def get_free_proxies():
  url = "https://free-proxy-list.net/"
  res = get(
    url,
    headers={
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.5',
      'Connection': 'keep-alive',
      'Referer': 'https://www.google.com/',
      'User-Agent': get_random_user_agent(),
    },
    proxies={
      'https': '127.0.0.1:7890' # 本机的代理, 否则无法访问此 url
    },
    timeout=1.5,
  )
  # soup = bs(brotli., "html.parser")
  soup = bs(res.text, 'html.parser')
  proxies = []
  for row in soup.find("table", {"class": "table"}).find_all("tr")[1:]:
    tds = row.find_all("td")
    try:
      ip = tds[0].text.strip()
      port = tds[1].text.strip()
      host = f"{ip}:{port}"
      https = tds[6].text.strip() == 'yes'
      proxies.append({
        'host': host,
        'https': https
      })
    except IndexError:
      continue
  return proxies

def req(**kwargs):
  try:
    with Session() as session:
      proxy = random.choice(get_free_proxies())
      proxies={
        'http': proxy['host'],
      }
      if proxy['https'] == True:
        proxies.update({
          'https': proxy['host']
        })
      response = session.get(
        headers={
          'User-Agent': get_random_user_agent()
        },
        proxies=proxies,
        **kwargs,
      )
      if response.status_code == 200:
        return response
      else:
        logging.error('request error')
  except RequestException as e:
    logging.exception('exception {}'.format(e))

software_names = [SoftwareName.CHROME.value, SoftwareName.EDGE.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MACOS.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=50)

# 利用 random_user_agent 这个包获得随机的 User-Agent
def get_random_user_agent():
  return user_agent_rotator.get_random_user_agent()
