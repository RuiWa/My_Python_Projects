import re 
import os

def preprocessing(filename): 
    """
    文本预处理：只保留字母，去掉空格、标点符号、数字等
    """
    file = open(filename) 
    content = file.read()
    word = re.compile(r'[^a-zA-Z]') # 找到所有非字母的符号
    content = word.sub('', content) # 将非字母的符号全部去掉
    content = content.lower() # 全部变成小写

    return content
    
    
def generate_n_gram(content, n): 
    """
    构建n元模型
    """
    n_gram = []
    for i in range(len(content)-n+1): 
        n_gram.append(content[i:i+n])
    return n_gram
    
    
def rolling_hashing(n_gram, Base, n): 
    """
    计算分片的哈希值，n与n_gram中的n相同
    Base：确定值
    """
    hashlist = []
    hash = 0
    initial = n_gram[0]
    #初始化：Base 基数一般设置为素数
    #initial:第一个分片的 hash 值需要手动计算
    
    for i in range(n):
        hash += ord(initial[i])*(Base**(n-i-1))
        hashlist.append(hash)

    for i in range(1,len(n_gram)): 
        pre = n_gram[i-1] 
        present = n_gram[i]
        hash = (hash-ord(pre[0])*(Base**(n-1)))*Base + ord(present[n-1]) 
        hashlist.append(hash)

    return hashlist
    
    
def winnowing(hashlist, t, n): 
    """
    winnowing算法计算每个哈希值的指纹，t为检测阈值
    """
    window = t-n+1 # 确定窗口大小，确保在长度超过t的特征能够被检测到至少一个
    minValue = minPos = 0 
    fingerprint = {}
    for i in range(len(hashlist)-window+1): 
        temp = hashlist[i:i+window] 
        minValue = temp[0]
        minPos = 0
        for j in range(window):
            if temp[j] <= minValue: 
                minValue = temp[j] 
                minPos = j
        if (i+minPos) not in fingerprint.keys(): 
            fingerprint[i+minPos] = minValue
    return fingerprint
    
    
def comparison(fingerprint_1, fingerprint_2): 
    """
    比较两个字典的相似性
    """
    count = 0
    size = min(len(fingerprint_1),len(fingerprint_2)) 
    for i in fingerprint_1.values():
        for j in fingerprint_2.values(): 
            if i == j:
                count += 1 
                break
                
                
if __name__== '__main__':
    print('分片大小为 5')
    print('检测阈值为 9') 
    dirpath = os.getcwd()
    path_1 = dirpath + "\\text_1.txt" 
    path_2 = dirpath + "\\text_2.txt" 
    fingerprint_1 = winnowing(rolling_hashing(generate_n_gram(preprocessing(path_1), 5),17, 5),9,5) 
    fingerprint_2 = winnowing(rolling_hashing(generate_n_gram(preprocessing(path_2), 5),17, 5),9,5)
    print(" 相 似 度 ：") 
    print(comparison(fingerprint_1,fingerprint_2)) 
    return count/size
