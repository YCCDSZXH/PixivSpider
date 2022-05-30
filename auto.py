import os
import datetime
# 获取日期
def getNowDate():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
print(getNowDate())


# os.system('zip -r OutPut.zip OutPut')