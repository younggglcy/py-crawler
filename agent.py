from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value, SoftwareName.EDGE.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MACOS.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=50)

# 利用 random_user_agent 这个包获得随机的 User-Agent
def get_random_user_agent():
  return user_agent_rotator.get_random_user_agent()
