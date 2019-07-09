import requests
import re

# 指定网页链接
url = 'https://www.duquanben.com/xiaoshuo/5/5823/'

# 模拟浏览器发送http请求
response = requests.get(url)

# 确定网页编码方式
response.encoding = ('gbk')

# 目标小说的网页源码
html = response.text

# 小说名字，后面的[0]表示列表
title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]

# 新建txt文件保存小说
fb = open('%s.txt' % title, 'w', encoding = 'utf-8')

# 获取每一章的 (url, 标题)，re.S表示显示空格等等
ul = re.findall(r'<ul class="mulu_list">.*?</ul>', html, re.S)[0]

chapter_info_list = re.findall(r'href="(.*?)">(.*?)<', ul)

# 循环取出每一章的url和标题
for chapter_info in chapter_info_list:
    chapter_url, chapter_title = chapter_info
    chapter_url = 'https://www.duquanben.com/xiaoshuo/5/5823/%s' % chapter_url
    
    # 下载每一章的内容
    chapter_response = requests.get(chapter_url)
    chapter_response.encoding = 'gbk'
    chapter_html = chapter_response.text
    chapter_content = re.findall(r'<div id="htmlContent" class="contentbox">(.*?)<div class="ad00"><script>show_style\(\)', chapter_html, re.S)[0]
    
    # 清洗内容（去掉空格之类的）
    chapter_content = chapter_content.replace(' ','')
    chapter_content = chapter_content.replace('&nbsp','')
    chapter_content = chapter_content.replace('<br/>','')
    chapter_content = chapter_content.replace(';;;;','')
    
    # 没有这句代码无法实现 utf-8 编码 
    chapter_content = chapter_content.replace('\ufffd','')
    
    # 保存数据
    fb.write(chapter_title)
    fb.write(chapter_content.encode('utf-8').decode('utf-8'))
    fb.write('\n')
    
    print(chapter_url)
