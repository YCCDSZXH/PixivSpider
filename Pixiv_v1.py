
from distutils.file_util import write_file
import requests
import re

import os
import datetime

import asyncio
import aiohttp
import time
import aiofiles
start = time.time()

async def write_data(path, data):
  # 异步方式执行with操作,修改为 async with


  async with aiofiles.open(path, "wb") as fp:
    await fp.write(data)



headers = {
    'referer': 'https://www.pixiv.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def getList():
  url = "https://www.pixiv.net/ranking.php"
  res = requests.get(url)
  # print(res.text)
  res = res.text.translate(str.maketrans({
      "\n": None,
      "\r": None,
      " ": None
  }))
  list = re.findall(r'<sectionid="(.*?)</span></a></section>', res)
  print(len(list))
  return list


def getDetailInfo(relist):
  allInfoList = []
  for i in relist:
    res = re.findall(
        'data-rank="(.*?)"data-rank-text=".*?"data-title="(.*?)"data-user-name="(.*?)"data-date="(.*?)"data-view-count=".*?"data-rating-count=".*?"data-attr=".*?"data-id="(.*?)"', i)[0]
    allInfoList.append(res)
  return allInfoList


async def downloadSingalImgInfo(PInfo, session, basePath='OutPut'):
  print("耗时1", time.time() - start)
  url = 'https://www.pixiv.net/en/artworks/' + PInfo[4]
  async with await session.get(url) as resp:
    res = await resp.text()
    originImgLink = re.findall(r'"original":"(.*?)"', res)[0]
    print("耗时2", time.time() - start)
    async with await session.get(originImgLink, headers=headers) as resp:
      await write_data(basePath + str("%04d" % int(PInfo[0]))+f'{PInfo[4]}.jpg', await resp.read())


def mkdir(path):
  path = path.strip()
  path = path.rstrip("\\")
  isExists = os.path.exists(path)
  if not isExists:
    os.makedirs(path)
    return True
  else:
    return False
# 获取当前日期


def getNowDate():
  return datetime.datetime.now().strftime('%Y%m%d')


async def main():
  originInfoList = getList()
  delailInfoList = getDetailInfo(originInfoList)
  # print(delailInfoList)

  async with aiohttp.ClientSession() as session:
    basePath = f"OutPut/{ getNowDate()}/"
    mkdir(basePath)
    for i in delailInfoList:
      await downloadSingalImgInfo(i, session, basePath)

  print()
# 主函数
if __name__ == "__main__":
  start = time.time()
  asyncio.run(main())
  print('耗时', time.time()-start)
