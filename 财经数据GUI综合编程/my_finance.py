import json
import re
import requests

def retrieve_dji_list():
    """
    获取道指成份股的代码、名称、价格
    :return: 一个列表dji_list，列表元素为字典，字典包含{code，name，price}
    """
    try:
        r = requests.get('http://money.cnn.com/data/dow30/')
    except ConnectionError as err:
        print(err)

    search_pattern = re.compile('class="wsod_symbol">(.*?)<\/a>.*<span.*">(.*?)<\/span>.*\n.*class="wsod_stream">(.*?)<\/span>')
    dji_list_in_text = re.findall(search_pattern, r.text)
    dji_list = []
    for item in dji_list_in_text:
        dji_list.append({'code':item[0], 'name':item[1], 'price':item[2]})
    return  dji_list


def retrieve_quotes_historical(stock_code):
    """
    获取stock_code对应的道指成份股的最近一年的数据
    :param stock_code: 股票代码
    :return:一个列表，列表元素为字典，字典中包含{date，open，high，low，close，volume，adjclose}
    """
    url = 'https://finance.yahoo.com/quote/{}/history?p={}'.format(stock_code, stock_code)
    quotes = []

    try:
        r = requests.get(url)
    except ConnectionError as err:
        print(err)

    m = re.findall('"HistoricalPriceStore":{"prices":(.*?),"isPending"', r.text)
    if m:
        quotes = json.loads(m[0]) # 解码json数据，返回python字段的数据类型
        quotes = quotes[::-1] # 将最近的数据放在列表quotes的最前面

    return [item for item in quotes]
