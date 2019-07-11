import requests
import re

class NovelDownload(object):

    def __init__(self, url):
        self.url = url

    def get_content(self):
        #请求url的响应
        response = requests.get(self.url)
        #设置编码方式是gbk，注意大部分网站的编码方式其实是utf-8
        response.encoding = 'gbk'
        #返回网页源代码
        html = response.text
        #正则表达式提取小说名
        title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]
        #以写的方式创建一个txt文件，也可以用with open ... as
        fb = open('%s.txt' % title, 'w', encoding = 'utf-8')
        #正则表达式提取网页源代码中的目录
        ul = re.findall(r'<ul class="mulu_list">.*?</ul>', html, re.S)[0]
        #目录中包含章节名和对应的超链接
        chapter_info_list = re.findall(r'href="(.*?)">(.*?)<', ul)
        for chapter_info in chapter_info_list:
            chapter_url, chapter_title = chapter_info
            chapter_url = self.url + chapter_url
            chapter_response = requests.get(chapter_url)
            chapter_response.encoding = 'gbk'
            chapter_html = chapter_response.text
            #获取每一章的内容
            chapter_content = re.findall(r'<div id="htmlContent" class="contentbox">(.*?)<div class="ad00"><script>show_style\(\)', chapter_html, re.S)[0]
            #清洗数据
            chapter_content = chapter_content.replace(' ','')
            chapter_content = chapter_content.replace('&nbsp','')
            chapter_content = chapter_content.replace('<br/>','')
            chapter_content = chapter_content.replace(';;;;','')
            chapter_content = chapter_content.replace('\ufffd','')
            #将标题和内容写入txt文件
            fb.write(chapter_title)
            fb.write(chapter_content.encode('utf-8').decode('utf-8'))
            fb.write('\n')
