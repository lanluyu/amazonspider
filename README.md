amazonspider说明文档
介绍
 - 
amazonspider是一个爬取亚马逊所有电子书信息的爬虫。该爬虫分别爬取了中文电子书和外文原版电子书信息，总计70万+条电子书信息。<br>

代码说明
--
### 运行环境
* Windows 10 专业版<br>
* Python 3.5/Scrapy 1.5.0/MongoDB 3.4.7/比特代理<br>

### 依赖包
* Requests<br>
* Pymongo<br>
* Faker(随机切换User-Agent)<br>

### 其它
* 亚马逊的所有电子书分为35个大类，660个子类和分类页面，据亚马逊自己网站统计有60余万册的电子书，实际获取的结果在消重后数量有80万。在每一个大类和子类分类的页面，每一页都只显示16条电子书信息，最大显示页数为400页，总计6400条。有一小部分的没有子类别的一些类别，电子书总数超过6400条的，其下的电子书信息无法完全获取。<br>另外
* 亚马逊有严格的IP检测防爬虫措施。个人测试的结果为同一IP最大的信息获取量大约为11K.之后就会被拒绝请求。这里我采用的是比特代理客户端，能够对本机实现定时自动切换IP。设置2S的下载延迟，五分钟切换一次IP，分别爬取的时间在15小时以上。<br>
* 亚马逊的网页元素路径略显复杂，好在子页面和父页面的类似元素的xpath路径相同。浏览器获得的和爬虫获取的子页面url不一样，但是都能到达同一页面。

## 流程




爬取结果
-
* 整个爬取过程持续了80个小时，总共获取了1140727条数据，结果存储在MongoDB中。再导出为Excle文件。部分数据如下截图:<br>
![部分问答信息](https://github.com/lanluyu/zhihu/blob/master/pic/mongodb.PNG)
* 根据2974个问题制作的词云如下：<br>
![词云](https://github.com/lanluyu/zhihu/blob/master/pic/lanluyu%E8%AF%8D%E4%BA%91%E5%9B%BE20180711.png)
