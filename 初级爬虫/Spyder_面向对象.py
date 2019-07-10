import requests
import re

class NovelDownload(object):

    def __init__(self, url):
        self.url = url

    def get_content(self):
        response = requests.get(self.url)
        response.encoding = 'gbk'
        html = response.text
        title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]
        fb = open('%s.txt' % title, 'w', encoding = 'utf-8')
        ul = re.findall(r'<ul class="mulu_list">.*?</ul>', html, re.S)[0]
        chapter_info_list = re.findall(r'href="(.*?)">(.*?)<', ul)
        for chapter_info in chapter_info_list:
            chapter_url, chapter_title = chapter_info
            chapter_url = self.url + chapter_url
            chapter_response = requests.get(chapter_url)
            chapter_response.encoding = 'gbk'
            chapter_html = chapter_response.text
            chapter_content = re.findall(r'<div id="htmlContent" class="contentbox">(.*?)<div class="ad00"><script>show_style\(\)', chapter_html, re.S)[0]
            chapter_content = chapter_content.replace(' ','')
            chapter_content = chapter_content.replace('&nbsp','')
            chapter_content = chapter_content.replace('<br/>','')
            chapter_content = chapter_content.replace(';;;;','')
            chapter_content = chapter_content.replace('\ufffd','')
            fb.write(chapter_title)
            fb.write(chapter_content.encode('utf-8').decode('utf-8'))
            fb.write('\n')
