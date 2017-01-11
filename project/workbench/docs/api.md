工作台 Workbench API 列表
=======
> 基于产品图v1/workbench.2 20161124


##<产品图第16页> M2 用户工作台-F1 导航点-P1 工作打卡

### 1 获取时间线记录
*Method: GET*

`/api/workbench/diaries/?user=&c_t_0=&c_t_1=

*Parameters*

| Field | Chinese |
|:------|:--------|
| user| 指定用户ID |
| c_t_0 | 起始日期 |
| c_t_1 | 结束日期 |
示例：/api/workbench/diaries/?user=2&c_t_0=2015-11-04&c_t_1=2015-11-05
*Response 200*

```json
成功 Code 200
{
    "models": [
        {
            "id": 1,
            "tag": 2,
            "work_types": "拆字 录入",
            "work_brief": "拆子100个，录入100个",
            "content": "今天天气不错，干活也不错，感恩三宝加持！",
            "c_t": "2015-11-04T02:34:00Z",
            "u_t": "2016-12-25T08:58:49.474569Z",
            "user": 2
        }
    ],
    "html_context": {
        "previous_url": null,
        "page_links": [
            [
                "http://localhost:8000/api/workbench/diaries/",
                1,
                true,
                false
            ]
        ],
        "next_url": null
    }
}
注："html_context" 可用于分页，此后所有api都有此部分，不再赘述
previous_url:上一页链接
page_links:所有页面链接
    url:页面链接
    page:页码
    is_active:是否为当前页
    is_break:是否最后一页
next_url:下一页链接


失败 Code >= 400
{
	"detail": ""
}
```

### 2 提交日记
*Method: POST*

`/api/v1/workbench/diaries?&tag=&content=`

*Parameters*

| Field | Chinese   |
|:------|:----------|
| user  | 指定用户ID |
| tag   | 标签       |
| content | 日记内容 |

*Response 200*

```json
成功 Code 200
{
	"id": 30,
    "tag": 0,
    "work_types": "拆字",
    "work_brief": "拆字3个 ",
    "content": "有一个天，一个老外来到了龙泉寺，他获得了一个银杏果，他觉得很好吃，所以他每年秋天都会来，直到他遇到了学诚法师，他就留在了龙泉寺。",
    "c_t": "2016-12-30T07:57:11Z",
    "u_t": "2016-12-30T07:57:10.878680Z",
    "user": 2
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第17页> M2 用户工作台-F1 导航点-P2 积分-积分排行榜

> 说明：
>> 页面上的我的积分和我的排名，与页面一起出，不做API。
>> 带用户名搜索后，排名页跳到指定用户名开始的位置，同时分页导航也同时显示指定页码。


### 1. 查询积分排行榜

*Method: GET*


`/api/workbench/credits/?sort__id=1&user__username=wangwei&page=&page_size=`

*Parameters*

| Field | Chinese |
|:------|:--------|
| sort__id  | 积分榜类型 1: 总积分(default)；2: 拆字积分；3: 去重积分； 4: 录入积分； 5:互助积分|
| user__username | 指定用户  空值：排名从1开始（default）；"name"：积分榜跳到指定用户开始的5个排名|
| page_size | 分页大小（default 5） |
| page | 页序号，从1开始（default） |

示例：/api/workbench/credits/?sort__id=1&user__username=wangwei
*Response 200*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://xxx:8000/api/v1/workbench/{model}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"rank": 1,
			"user_id": 10,
			"user_name": "张三",
			"credits": 1800
		},

		{
			"rank": 2,
			"user_id": 100,
			"user_name": "张三feng",
			"credits": 1000
		},
		{
			"rank": 3,
			"user_id": 50,
			"user_name": "张三yu",
			"credits": 800
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

##<产品图第18页> M2 用户工作台-F1 导航点-P2 积分-积分详情

>说明
>>总积分，各项指标占比和兑换积分，与页面一起出。不做API。

###1 查询某个用户的积分详情

*Method: GET*


`/api/v1/workbench/credits?sort=&page=&page_size`

*Parameters*

| Field | Desc |
|:------|:-----|
| sort | 积分类型  0：总积分(default)；1: 去重；2:拆字；3:录入 |
| page_size | 分页大小（default 5） |
| page | 页序号，从1开始（default 1） |

*Response 200*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://xxx:8000/api/v1/workbench/{model}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"type": "拆字",
			"credits": 1800，
			"package_id": 123,
			"package_name": "异体字拆字"
		},

		{
			"id": 2,
			"user_name": "去重",
			"credits": 1000
			"package_id": 123,
			"package_name": "高丽去重"
		},
		{
			"id": 3,
			"user_name": "录入",
			"credits": 800
			"package_id": 123,
			"package_name": "汉语大字典录入"
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

##<产品图第19页> M2 用户工作台-F1 导航点-P2 积分-我的兑换

>说明：
>总积分，各项指标占比和兑换积分，与页面一起出。不做API。

>兑换状态：1:申请中，2:已受理，3:已兑换，0:已取消

### 1 获取兑换记录

*Method： GET*

`/api/v1/workbench/redeems?order_by=&page_size=&page=`

*Parameters*

| Field | Desc |
|:------|:-----|
| order_by | 时间排序  0=asc（default）; 1=desc |
| page_size | 分页大小（default 5） |
| page | 页序号，从1开始（default） |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://xxx:8000/api/v1/workbench/{model}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"datetime": "2016-01-01 14:00:02",
			"reward": "感悟人生"，
			"cost_credits": 1200,
			"status": "已领取",
			"remark": "希望法师签名"
		},

		{
			"id": 2,
			"datetime": "2016-02-04 14:00:02",
			"reward": "感悟人生"，
			"cost_credits": 1200,
			"status": "已受理",
			"remark": "希望法师签名"
		},
		{
			"id": 3,
			"datetime": "2016-01-02 14:00:02",
			"reward": "文集"，
			"cost_credits": 1000,
			"status": "申请中",
			"remark": "希望法师签名"
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

### 2 申请兑换

*Method： POST*

`/api/v1/workbench/redeems?cost=&reward_id=`

*Parameters*

| Field | Desc |
|:------|:-----|
| cost | 兑换积分 |
| reward_id | 奖品名ID |

*Response*

```json
成功 Code 200
{
	"id": 3,
	"datetime": "2016-01-02 14:00:02",
	"reward": "文集"，
	"cost_credits": 1000,
	"status": "申请中",
	"remark": "希望法师签名"
}

失败 Code >= 400
{
	"detail": "credits not enough"
}
```

### 3 取消兑换

*Method： PUT*

`/api/v1/workbench/redeems/{id}/cancel`
`/api/v1/workbench/redeems/{id}?status=0`


*Parameters*

| Field | Desc |
|:------|:-----|
| id | 积分兑换条目ID |
| status | 领取状态：0:取消，1:进行中，2:受理中，3:完成 |

*Response*

```json
成功 Code 200
{
	"id": 3,
	"datetime": "2016-01-02 14:00:02",
	"reward": "文集"，
	"cost_credits": 1000,
	"status": "已取消",
	"remark": "希望法师签名"
}

失败 Code >= 400
{
	"detail": ""
}
```

### 4 奖品列表

*Method GET*


`/api/v1/workbench/rewards`

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://xxx:8000/api/v1/workbench/{model}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"name": "感悟人生"，
			"cost_credits": 1200
		},
		{
			"id": 2,
			"name": "感悟人生"，
			"cost_credits": 1200
		},
		{
			"id": 3,
			"name": "文集"，
			"cost_credits": 1000
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第20页> M2 用户工作台-F2 我的任务-P1 进行中

### 1 任务包概要列表

*Method GET*


`/api/v1/workbench/task_packages?status=1`

*Parameters*

| Field | Desc |
|:------|:-----|
| status | 任务包状态  0:未开始；1:进行中； 2：已完成 |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://xxx:8000/api/v1/workbench/{model}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"business_type": "录入",
			"task_package_id": 100,
			"business_stage": "初次",
			"task_size": 100,
			"daily_plan": 20,
			"today_progress": 5,
			"total_progress": 60,
			"task_create_date": "2016-11-10",
			"est_due_date": "2016-11-20",
		},
		{
			"id": 2,
			"business_type": "拆字",
			"task_package_id": 100,
			"business_stage": "回查",
			"task_size": 100,
			"daily_plan": 20,
			"today_progress": 5,
			"total_progress": 60,
			"task_create_date": "2016-11-10",
			"est_due_date": "2016-11-20",
		},
		{
			"id": 3,
			"business_type": "去重",
			"task_package_id": 100,
			"business_stage": "审查",
			"task_size": 100,
			"daily_plan": 20,
			"today_progress": 5,
			"total_progress": 60,
			"task_create_date": "2016-11-10",
			"est_due_date": "2016-11-20",
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

###2 修改每日计划
*Method PUT*


`/api/v1/workbench/task_packages/{id}?daily_plan=`

*Parameters*

| Field | Desc |
|:------|:-----|
| id | 任务包ID |
| daily_plan | 每日计划工作量（多少个字） |

*Response*

```json
成功 Code 200
{
	"id": 1025,
	"business_type": "录入",
	"task_package_id": 100,
	"business_stage": "初次",
	"task_size": 100,
	"daily_plan": 20,
	"today_progress": 5,
	"total_progress": 60,
	"task_create_date": "2016-11-10",
	"est_due_date": "2016-11-20",
}

失败 Code >= 400
{
	"detail": ""
}
```


###3 任务列表查询API
根据参数包括以下功能：
#获取进行中拆字、录入、去重 不同阶段的任务
视图文件	/lqhanzi/project/backend/views/api_tasks.py
示例链接	GET /api/v1/tasks/?business_type=1&business_stage=2&task_status=0
参数名称及取值解释
business_type
0	拆字
1	录入
2	高丽去重
3	高台去重

business_stage
0	初次
1	回查
2	审查

task_status
0   未开放
1   待分配
2	进行中
3	已完成
page 页数
page_size 每页返回值个数

返回值,此处为 拆字任务 示例
成功
HTTP 200 OK
Allow: GET, POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "models": [
        {
            "id": 6,
            "task_ele": {
                "source": 1,
                "hanzi_type": 1,
                "hanzi_char": "菩",
                "hanzi_pic_id": "",
                "variant_type": 0,
                "std_hanzi": "",
                "as_std_hanzi": "",
                "seq_id": "",
                "is_redundant": false,
                "skip_num_draft": 0,
                "init_split_draft": "",
                "other_init_split_draft": "",
                "deform_split_draft": "",
                "similar_parts_draft": "",
                "dup_id_draft": "",
                "skip_num_review": 0,
                "init_split_review": "",
                "other_init_split_review": "",
                "deform_split_review": "",
                "similar_parts_review": "",
                "dup_id_review": "",
                "skip_num_final": 0,
                "init_split_final": "",
                "other_init_split_final": "",
                "deform_split_final": "",
                "similar_parts_final": "",
                "dup_id_final": "",
                "is_draft_equals_review": false,
                "is_review_equals_final": false,
                "is_checked": false,
                "is_submitted": false,
                "remark": "",
                "c_t": "2017-01-02T18:10:52.860670Z",
                "u_t": "2017-01-04T07:12:12.189054Z"
            },
            "business_type": 1,
            "business_stage": 2,
            "task_status": 0,
            "credits": 2,
            "remark": "2",
            "assigned_at": "2017-01-03T02:13:00Z",
            "completed_at": null,
            "c_t": "2017-01-02T07:12:00Z",
            "u_t": "2017-01-07T06:55:24.159348Z",
            "object_id": 1,
            "user": 2,
            "task_package": 1,
            "content_type": 26,
            "business_type_display": "拆字",
            "business_stage_display": "审查",
            "task_status_display": "进行中"
        }
    ],
    "html_context": {
        "previous_url": null,
        "page_links": [
            [
                "http://localhost:8000/api/v1/tasks/?business_stage=2&business_type=1&task_status=0",
                1,
                true,
                false
            ]
        ],
        "next_url": null
    }
}
失败 Code >= 400
{
	"detail": ""
}

###4 拆字详细信息API
文件	/lqhanzi/project/backend/views/api_variants_split.py
链接	/api/v1/splits/{id}/
示例	GET /api/v1/splits/1/

返回值
成功
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "source": 1,
    "hanzi_type": 1,
    "hanzi_char": "菩",
    "hanzi_pic_id": "",
    "variant_type": 0,
    "std_hanzi": "",
    "as_std_hanzi": "",
    "seq_id": "",
    "is_redundant": false,
    "skip_num_draft": 0,
    "init_split_draft": "",
    "other_init_split_draft": "",
    "deform_split_draft": "",
    "similar_parts_draft": "",
    "dup_id_draft": "",
    "skip_num_review": 0,
    "init_split_review": "",
    "other_init_split_review": "",
    "deform_split_review": "",
    "similar_parts_review": "",
    "dup_id_review": "",
    "skip_num_final": 0,
    "init_split_final": "",
    "other_init_split_final": "",
    "deform_split_final": "",
    "similar_parts_final": "",
    "dup_id_final": "",
    "is_draft_equals_review": false,
    "is_review_equals_final": false,
    "is_checked": false,
    "is_submitted": false,
    "remark": "",
    "c_t": "2017-01-02T18:10:52.860670Z",
    "u_t": "2017-01-04T07:12:12.189054Z"
}
失败 Code >= 400
{
	"detail": ""
}

###5 提交拆字API
路径:/api/v1/splits/{id}/submit/
视图文件:/lqhanzi/project/backend/views/api_variants_input.py
示例：PATCH /api/v1/splits/1/submit
返回值
成功
HTTP 200 OK
Allow: GET, PUT, PATCH, OPTIONS
Content-Type: application/json
Vary: Accept
{
  "source": null,
  "hanzi_type": null,
  "hanzi_char": "",
  "hanzi_pic_id": "",
  "variant_type": null,
  "std_hanzi": "",
  "as_std_hanzi": "",
  "seq_id": "",
  "is_redundant": false,
  "skip_num_draft": null,
  "init_split_draft": "jinjin",
  "other_init_split_draft": "",
  "deform_split_draft": "",
  "similar_parts_draft": "",
  "dup_id_draft": "",
  "skip_num_review": null,
  "init_split_review": "",
  "other_init_split_review": "",
  "deform_split_review": "",
  "similar_parts_review": "",
  "dup_id_review": "",
  "skip_num_final": null,
  "init_split_final": "",
  "other_init_split_final": "",
  "deform_split_final": "",
  "similar_parts_final": "",
  "dup_id_final": "",
  "is_draft_equals_review": false,
  "is_review_equals_final": false,
  "is_checked": false,
  "is_submitted": false,
  "remark": "",
  "c_t": "2017-01-02T10:10:52.860670Z",
  "u_t": "2017-01-11T05:50:53.226665Z",
  "task": {
    "0": 6,
    "1": 7,
    "2": 9
  }
}
失败 Code >= 400
{
	"detail": ""
}
###6 提交并转下一条拆字API
路径:/api/v1/splits/{id}/submit_and_next/
视图文件:/lqhanzi/project/backend/views/api_variants_input.py
示例：PATCH /api/v1/splits/5/submit_and_next/
数据：
{
    "source": 1,
    "hanzi_type": 0,
    "hanzi_char": "",
    "hanzi_pic_id": "",
    "variant_type": 0,
    "std_hanzi": "",
    "as_std_hanzi": "",
    "seq_id": "",
    "is_redundant": false,
    "skip_num_draft": null,
    "init_split_draft": "yyy",
    "other_init_split_draft": "",
    "deform_split_draft": "",
    "similar_parts_draft": "",
    "dup_id_draft": "",
    "skip_num_review": null,
    "init_split_review": "",
    "other_init_split_review": "",
    "deform_split_review": "",
    "similar_parts_review": "",
    "dup_id_review": "",
    "skip_num_final": null,
    "init_split_final": "",
    "other_init_split_final": "",
    "deform_split_final": "",
    "similar_parts_final": "",
    "dup_id_final": "",
    "remark": ""
 }

返回值
1）成功
HTTP 200 OK
Allow: GET, PUT, PATCH, OPTIONS
Content-Type: application/json
Vary: Accept
{
  "source": 1,
  "hanzi_type": 1,
  "hanzi_char": "菩",
  "hanzi_pic_id": "",
  "variant_type": 0,
  "std_hanzi": "",
  "as_std_hanzi": "",
  "seq_id": "",
  "is_redundant": false,
  "skip_num_draft": 9,
  "init_split_draft": "哈哈哈",
  "other_init_split_draft": "",
  "deform_split_draft": "",
  "similar_parts_draft": "",
  "dup_id_draft": "",
  "skip_num_review": null,
  "init_split_review": "",
  "other_init_split_review": "",
  "deform_split_review": "",
  "similar_parts_review": "",
  "dup_id_review": "",
  "skip_num_final": null,
  "init_split_final": "",
  "other_init_split_final": "",
  "deform_split_final": "",
  "similar_parts_final": "",
  "dup_id_final": "",
  "is_draft_equals_review": false,
  "is_review_equals_final": false,
  "is_checked": false,
  "is_submitted": false,
  "remark": "",
  "c_t": "2017-01-06T05:50:55.016723Z",
  "u_t": "2017-01-11T05:31:51.136171Z",
  "task": {
    "0": 10,
    "1": 22,
    "2": 23
  }
}
2）任务包已完成
HTTP 100 CONTINUE
任务包已完成，请领取新任务

3）HTTP 204 NO CONTENT
没有更多任务了，请明天再来吧。

失败 Code >= 400
{
	"detail": ""
}
##<产品图第23页> M2 用户工作台-F2 我的任务-P3 领任务

### 1 添加任务包
路径:/api/v1/backend/task_packages/
视图文件:/lqhanzi/project/backend/views/api_task_packages.py
方法:POST
Content-Type: application/json
数据：
{
    "user": null,
    "business_type": null,
    "business_stage": null,
    "size": null,
    "status": null,
    "daily_plan": null,
    "due_date": null,
    "completed_num": null,
    "completed_at": null,
    "c_t": null
}
字段说明参见模型文件/backend/models.py
TaskPackages