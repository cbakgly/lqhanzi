龙泉字库
========

|Page | Content                                     |
|-----|---------------------------------------------|
|3    |M1 龙泉字库-F1 部件笔划检字法-P1 初始页面  |
|4    |M1 龙泉字库-F1 部件笔划检字法-P2 检索结果   |
|5   |M1 龙泉字库-F1 部件笔划检字法-P3 字头综合页面-台湾异体字字典    |
|7   |M1 龙泉字库-F1 部件笔划检字法-P3 字头综合页面-高丽异体字字典  |
|8   |M1 龙泉字库-F1 部件笔划检字法-P3 字头综合页面-汉语大字典    |
|9   |M1 龙泉字库-F2 异体字检索-P1 初始页面|
|9   |M1 龙泉字库-F2 异体字检索-P2 检索结果|
|10  |M1 龙泉字库-F3 字典-F1 台湾异体字字典-P0 初始页面|
|12  |M1 龙泉字库-F3 字典-F1 台湾异体字字典-P2 检字结果|
|13  |M1 龙泉字库-F3 字典-F1 台湾异体字字典-P3 结果展示|
|14  |M1 龙泉字库-F3 字典-F2 汉语大字典-P4 目录索引结果|
## <3>. M1 龙泉字库-F1 部件笔划检字法-P1 初始页面
    总体说明：用户可以通过本页面的输入框,按照部件笔划检字法的规则进行检字，包含两个API，1，异体字检索API，2，部件面板部件检索API

### 1. 异体字检索API

*Method: GET*

*Url*
 `/api/v1/hanzi?q=&page_size=&page=`

*Parameters*

| Field | Chinese |
|:------|:--------|
| q | 部件查询语句：明3,6 |
| page_size | 页面大小|
| page | 第几页 |

*Response*
```js
{
models: [{
id: 1,
hanzi_type: 2, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00001',
hanzi_pic_url: '',
origin: 'tw',
}，
{
id: 2,
hanzi_type: 1, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00002',
hanzi_pic_url: '',
origin: 'tw',
}
{
id: 3,
hanzi_type: 0, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: '',
hanzi_pic_url: '',
origin: 'gl',
}
],
pagination: {
previous_page: 1,
next_page: 3,
start_index: 531,
end_index: 630,
total_entries: 5111,
total_pages: 20,
page: 2,
}
}
```

### 2. 部件面板部件检索API
有些部件是不方便输入的，所以提供搜索输入，比如5，代表5划，hspn，代码笔顺首笔横竖撇捺；比如5s，就意味着搜索5划首笔是竖的部件

*Method: GET*

*Url*
 `/api/v1/stroke?q=`

 *Parameters*

 | Field | Chinese |
 |:------|:--------|
 | q | 部件查询语句：5h/8s |

*Response*
```json
[
  {"id": 1, "hanzi_char": "未"},
  {"id": 2, "hanzi_char": "马"},
  ...
]
```
## <4>.  M1 龙泉字库-F1 部件笔划检字法-P2 检索结果
    用户可以浏览检索结果,点击字头可跳转该字的综合信息页面

### 1. 文字信息搜索API
根据hanzi_char或者hanzi_pic_id信息搜索文字信息
*Method: POST*

*Url*
`/api/v1/hanzi/search`

 *Parameters*

 | Field | Chinese |
 |:------|:--------|
 | hanzi_char | 汉字字符：5h/8s |
 | hanzi_pic_id | 汉字统一图像编码：A00001 |

*Response*
```json
{
  dicts: [
  { name: 'unicode', value: ['U+6DE8'] },
  { name: '台湾', value: ['A00001/明', 'A02758-005/盲', 'A02398-001/盟'] },
  { name: '汉语', value: ['hy-8-0001-01'] },
  { name: '高丽', value: ['明2/盲'] },
  { name: '敦煌', value: ['dh-001-01'] }
  ],
  similar_parts: '水爪川', //相似部件
  mix_split: '', //混合拆分
}
```
## <5>.  M1 龙泉字库-F1 部件笔划检字法-P3 字头综合页面-台湾异体字字典
## <6>.  M1 龙泉字库-F1 部件笔划检字法-P3 字头综合页面-高丽异体字字典
## <8>.  M1 龙泉字库-F1 部件笔划检字法-P3 字头综合页面-汉语大字典
    展示正字或异体字在四部字典(台湾异体字字典、汉语大字典、高丽异体字字典、 敦煌俗字典)中的综合信息。台湾异体字网站的静态页面已经抓取到服务器本地。汉语大字 典、敦煌俗字典书籍以图片形式存储在服务器上。高丽异体字字典的正异关系以数据库形式 存储在服务器上

  由于信息来源于外部网站，采用传统view进行显示更加合适，所以这里不合适提供API的接口

## <9>.  M1 龙泉字库-F2 异体字检索-P1 初始页面
    通过该页面,用户可以按照部首索引的方式浏览台湾异体字字典,还可以通过部件 笔划检字法的方式检索台湾异体字字典。

### 1. 异体字符检索API

*Method: GET*

*Url*
 `/api/v1/variants_char?q=&page_size=&page=`

 *Parameters*

| Field | Chinese |
|:------|:--------|
| q | 部件查询语句：明/A00002|
| page_size | 页面大小|
| page | 第几页 |

*Response*
```js
{
models: [{
id: 1,
hanzi_type: 2, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00001',
hanzi_pic_url: '',
origin: 'tw',
}，
{
id: 2,
hanzi_type: 1, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00002',
hanzi_pic_url: '',
origin: 'tw',
}
{
id: 3,
hanzi_type: 0, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: '',
hanzi_pic_url: '',
origin: 'gl',
}
],
pagination: {
previous_page: 1,
next_page: 3,
start_index: 531,
end_index: 630,
total_entries: 5111,
total_pages: 20,
page: 2,
}
}
```
## <9>.  M1 龙泉字库-F2 异体字检索-P2 检索结果
    与<4> API设计相同，略

## <10>.  M1 龙泉字库-F3 字典-F1 台湾异体字字典-P0 初始页面
    通过该页面,用户可以按照部首索引的方式浏览台湾异体字字典,还可以通过部件 笔划检字法的方式检索台湾异体字字典。

### 1. 字典异体字检索API

*Method: GET*

*Url*
 `/api/v1/hanzi/dict?q=&strokes=&page_size=&page=`

*Parameters*

| Field | Chinese |
|:------|:--------|
| q | 部件查询语句：明3,6 |
|strokes| 笔划数（可选，用于基于笔划的分页显示）|
| page_size | 页面大小|
| page | 第几页 |

*Response*
```js
{
models: [ {stroke_num: 6, [{
id: 1,
hanzi_type: 2, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00001',
hanzi_pic_url: '',
origin: 'tw',
}，
{
id: 2,
hanzi_type: 1, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00002',
hanzi_pic_url: '',
origin: 'tw',
}
{
id: 3,
hanzi_type: 0, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: '',
hanzi_pic_url: '',
origin: 'gl',
}
]},{
stroke_num: 8, [{
id: 1,
hanzi_type: 2, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00001',
hanzi_pic_url: '',
origin: 'tw',
}，
{
id: 2,
hanzi_type: 1, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: 'A00002',
hanzi_pic_url: '',
origin: 'tw',
}
{
id: 3,
hanzi_type: 0, //【文字： 0， 图片： 1， 文字且图片： 2】
hanzi_char: '明',
hanzi_pic_id: '',
hanzi_pic_url: '',
origin: 'gl',
}
]}
]
}
```

## <12>.  M1 龙泉字库-F3 字典-F1 台湾异体字字典-P2 检字结果
    根据笔划的部件搜索，部件unicode，笔划数，使用字典异体字检索API。其他同上

## <13>.  M1 龙泉字库-F3 字典-F1 台湾异体字字典-P3 结果展示
    信息内容与<5>.<6>.<8>.相同，页面布局外部url资源的使用，优先采用view显示解决，这里不提供内部API。

## <14>.  M1 龙泉字库-F3 字典-F2 汉语大字典-P4 目录索引结果
    汉语大字典增加一个目录索引的方式,可以按照大字典原书的目录对页 面进行浏览。


### 1. 汉语大字典总索引API

*Method: GET*

*Url*
 `/api/v1/dict/origin=&page_size=&page=`

*Parameters*

| Field | Chinese |
|:------|:--------|
| origin | 字典查询语句：'hanyu' |
| page_size | 页面大小|
| page | 第几页 |

*Response*
```js
{
models: [{
id: 1,
page_info: 'p1',
token_id: 1,
level: 1,
page_title: '第二版修订说明',
}，
{
id: 2,
page_info: 'p2',
token_id: 2,
level: 1,
page_title: '前言',
}，
{
id: 3,
page_info: 'p3',
token_id: 3,
level: 1,
page_title: '第一章，一部',
}，
{
id: 4,
page_info: 'p4',
token_id: 3,
level: 2,
page_title: '第一章，二部',
}，
{
id: 5,
page_info: 'p4',
token_id: 3,
level: 2,
page_title: '第一章，儿部',
}，
{
id: 689,
page_info: 'p633',
token_id: 8,
level: 1,
page_title: '附录',
}
],
pagination: {
previous_page: 1,
next_page: 3,
start_index: 531,
end_index: 630,
total_entries: 5111,
total_pages: 20,
page: 2,
}
}
```

### 2. 汉语大字典页面信息

*Url*
 `/api/v1/dict/origin=&page_info=&page_size=&page=`

 | Field | Chinese |
|:------|:--------|
| origin | 字典查询语句：'hanyu' |
|page_info| 字典页面信息：'p3' |
| page_size | 页面大小|
| page | 第几页 |

*Response*
```js
{ page_title: '第一章',
  prev_page: 'p2',
  next_page: 'p4',
  image_url: ''
  }
```