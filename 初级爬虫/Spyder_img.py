import urllib.parse
import requests
import json
import jsonpath

# 获取网页源码-->解析-->筛选-->保存

def get_web_content(url):
    #获取网页源代码
    response = requests.get(url)
    html = response.text
    return html

def analyse_web(html):
    #将json格式转为Python格式
    data = json.loads(html)
    #得到图片的url
    photos = jsonpath.jsonpath(data, '$..path')
    return photos

def save(photos):
    #保存图片
    global num
    for i in photos:
        photo = requests.get(i)
        with open(r'./pictrues/{}.jpg'.format(num), 'wb') as f:
            f.write(photo.content)
            num += 1
            
def main(label):
    num = 0
    #关键字加密，对应url中的kw={}
    label = urllib.parse.quote(label)
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}'
    #以24为间隔是通过分析网页源码得到的
    for index in range(1, 241, 24):
        #传入关键字和开始值，index对应的是url中的start={}
        urls = url.format(label, index)
        html = get_web_content(urls)
        photos = analyse_web(html)
        save(photos)
        
if __name__ == '__main__':
    #关键字可以改成别的，如'数'，'人'等
    main('天空')
