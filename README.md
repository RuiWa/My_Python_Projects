## 我的Python项目

> 作者：汪瑞
>
> 说明：为了让自己学习Python更加有条理性和产出感，我将自己学习Python时实现的一些小项目记录下来，有些可能还不够完善，需要后续的补充...，最近还补充了闲谈系列，主要是自己在学习Python中的一些有意思的体会

### 项目1--飞机大战
- 说明：
- 1.使用Python中的Pygame包实现
- 2.目前的主要功能包括：创建窗口、创建飞机、控制飞机、发射子弹
- 3.还需要补充：子弹碰到飞机后摧毁飞机、计分...
- 4.feiji文件夹中是游戏所需要的资源

### 项目2--小说爬虫
- 说明：
- 1.非常简单的一个爬虫，用于爬取一本小说，并将小说下载到本地的txt文件中
- 2.爬取的小说网站是笔趣阁小说网站
- 3.注意到小说网站链接是https开头的，程序使用jupyter notebook编写运行没有问题，但是在pycharm上出现了问题，目前还未解决（换了一个解释器之后就好了）
- 4.以面向对象的方式改写之前的程序（改的不太好）

### 项目3--图片爬虫
- 说明：
- 1.爬取图片网站为[堆糖网](https://www.duitang.com/)
- 2.理解爬虫逻辑：获取网页源码-->解析-->筛选-->保存
- 3.图片网站为动态加载，不同于小说网站(静态加载)
- 4.程序中url的获取方式：在搜索框输入关键字-->按F12-->点击network-->下滑网页-->左下角出现图片-->右侧的Request URL即为所需url

### 闲谈1--神奇的递归
- 1.汉诺塔游戏
- 2.斐波那契数列
- 3.求一个数的二进制

### 项目4--财经数据GUI编程（取自[南京大学公开课‘用Python玩转数据’](https://www.icourse163.org/course/NJU-1001571005#/info)）
- 说明：
- 1.能够显示30支道指成份股最近一年的数据，主要涉及到界面的设计，是一个综合编程项目
- 2.具备绘图功能
- 3.使用面向对象编程
