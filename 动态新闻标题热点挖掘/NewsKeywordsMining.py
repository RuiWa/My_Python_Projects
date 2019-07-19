import jieba.posseg as pseg
import matplotlib.pyplot as plt
from os import path
import re
import requests
from scipy.misc import imread
from wordcloud import WordCloud


def fetch_sina_news():
    """
    获取新浪新闻的标题数据，并且写入subjects.txt
    """
    PATTERN = re.compile('.shtml" target="_blank">(.*?)</a><span>(.*?)</span></li>')
    
    BASE_URL = "http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_"
    
    MAX_PAGE_NUM = 10 # 设置一个最大页数
    
    with open('subjects.txt', 'w', encoding='utf-8') as f:
        for i in range(1, MAX_PAGE_NUM):
            print('Downloading page #{}'.format(i))
            r = requests.get(BASE_URL + str(i)+'.shtml')           
            r.encoding='gb2312'
            data = r.text            
            p = re.findall(PATTERN, data)            
            for s in p:
                f.write(s[0])                
            time.sleep(5)
            
            
def extract_words():
    """
    根据得到的标题文件，挖掘出其中频率最高的词，建立词云
    """
    with open('subjects.txt','r', encoding='utf-8') as f:
        news_subjects = f.readlines()
    
    # 去除停用词
    # 很多如“的”和“我们”这样的功能词对于主题分析并无帮助，因此需要使用停用词表进行词的过滤
    # stopwords.txt里面包含了常见的停用词
    stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
    
    newslist = []
    
    for subject in news_subjects:
        if subject.isspace():
            continue
        
        # 用结巴分词器对标题进行分词
        p = re.compile("n[a-z0-9]{0,2}")    # n, nr, ns, ... are the flags of nouns
        word_list = pseg.cut(subject)     
        for word, flag in word_list:
            if not word in stop_words and p.search(flag) != None:
                newslist.append(word)
    
    # 计算每个词出现的次数
    content = {}
    for item in newslist:
        content[item] = content.get(item, 0) + 1
    
    # 建立词云
    mask_image = imread('.\\mickey.png')
    wordcloud = WordCloud(font_path='.\\simhei.ttf', background_color="grey", mask=mask_image, max_words=10).generate_from_frequencies(content)
    
    # 显示图片
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('wordcloud.jpg')
    plt.show()

    
if __name__ == "__main__":
    fetch_sina_news()
    extract_words()
