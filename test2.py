# 修改zip文件头
def modify_zip_header(filename):
    print('修改zip文件头……')
    f = open(filename, 'rb+')
    f.seek(0x1e)
    f.write(b'\x00\x00')
    f.close()
    print('修改完成……')
    return
modify_zip_header('/workspaces/PixivSpider/20220530073926.zip')
