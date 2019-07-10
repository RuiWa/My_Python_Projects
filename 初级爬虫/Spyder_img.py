import urllib.parse
import requests
import json
import jsonpath

# 获取网页源码-->解析-->筛选-->保存

def get_web_content(url):
    response = requests.get(url)
    html = response.text
    return html

def analyse_web(html):
    data = json.loads(html)
    photos = jsonpath.jsonpath(data, '$..path')
    return photos

def save(photos):
    global num
    for i in photos:
        photo = requests.get(i)
        with open(r'./pictrues/{}.jpg'.format(num), 'wb') as f:
            f.write(photo.content)
            num += 1
            
def main(label):
    num = 0
    label = urllib.parse.quote(label)
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}'
    for index in range(1, 241, 24):
        urls = url.format(label, index)
        html = get_web_content(urls)
        photos = analyse_web(html)
        save(photos)
        
if __name__ == '__main__':
#关键字可以改
    main('天空')
