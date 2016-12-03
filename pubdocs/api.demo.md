API 格式
========

## <45>. M3  运营管理后台-F1  任务包管理-P1 查询
> 总体说明：按照用户名、任务类型、任务阶段、任务状态、领取时间、完成时间综合查询任务包，此API下有查询列表、查询详细、修改单个任务包并保存三个API

### 1. 查询任务包列表

*Method: GET*

*Url:*
 `/api/v1/admin/task_packages?format=0&username=&task_type=&task_stage=&obtain_begin_at=&obtain_end_at&finish_begin_at=&finish_end_at=`

*Parameters:*

| Field | Chinese |
|:------|:--------|
| format | 数据类型 0：表格数据；１：图表数据 |
| obtain_begin_at | 任务领取时间开始　|
| obtain_end_at | 领取时间结束 |

*Response:*
```json
[
  {"username": "xianer", "task_type": 0, "task_name": "#0001_异体字拆字", "stage": 0, "state": 0, "daily_plan": 100, "target": 200, "obtain_date": "2016-11-21", "expect_completed_at": "2016-11-20", "finished": 20 }
]
```

### 2. 查看单个任务包详细信息 #3
*Method: GET*

*Url:*
 `/api/v1/admin/task_packages/1/`

*Parameters:*

| Field | Chinese |
|:------|:--------|
|1 | 代表任务包的数据库id |
|c_t | 创建时间/入库时间 |
|obtain_at | 领取时间 |
|complete_at | 完成时间 |

*Response:*
```json
[
  {"id": 1, "hanzi_char": "", "username": "xiaoz", "c_t": "2016-11-21 10:20:32", "obtain_at": "2016-11-10 10:20:20", "complete_at": "2016-11-22 10:20:30"}
]
```
### 3. 修改单个任务包并保存
*Method: POST*

*Url:*
`/api/v1/admin/task_packages/1/`

*Post Data:*
```json
{"id": 1, "daily_plan": 10}
```

以上是API文档化的例子
==================
* <45> 代表是设计手册的45页，这样命名标题为了查询方便，其他的各位自动脑补，感恩。
 MarkDown 语法很简单，可以直接百度查询， 也可以访问如下例子
* [简书上的markdown简介](http://www.jianshu.com/p/1e402922ee32/)
* 推荐使用 atom 是github 上的专用编辑器，装个插件就可以，pycharm 也支持 markdown 插件
* 文本文档写也没意见
