import jieba.posseg as pseg
import matplotlib.pyplot as plt
from os import path
import re
import requests
from scipy.misc import imread
from wordcloud import WordCloud

def fetch_sina_news():
    PATTERN = re.compile('"title":(.*?),')
    #
    BASE_URL = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1&r=0.07257693576113322&callback=jQuery11120328721464028469_1556541915945&_=1556541915947'
    with open('subjects.txt', 'w', encoding='utf-8') as f:
        r = requests.get(BASE_URL)
        data = r.text.encode('utf-8').decode('unicode-escape')         
        p = re.findall(PATTERN, data)           
        for s in p:            
           f.write(s)
         
    
def extract_words():
    with open('subjects.txt','r', encoding='utf-8') as f:
        news_subjects = f.readlines()
    
    stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
    
    newslist = []
    
    for subject in news_subjects:
        if subject.isspace():
            continue
        
        # segment words line by line
        p = re.compile("n[a-z0-9]{0,2}")    # n, nr, ns, ... are the flags of nouns
        word_list = pseg.cut(subject)     
        for word, flag in word_list:
            if not word in stop_words and p.search(flag) != None:
                newslist.append(word)
    
    content = {}
    for item in newslist:
        content[item] = content.get(item, 0) + 1
    
    
    mask_image = imread('.\\mickey.png')
    wordcloud = WordCloud(font_path='.\\simhei.ttf', background_color="grey", mask=mask_image, max_words=10).generate_from_frequencies(content)
    # Display the generated image:
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('wordcloud.jpg')
    plt.show()
    
if __name__ == "__main__":
    fetch_sina_news()
    extract_words()
