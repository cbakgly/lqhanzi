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


##<产品图第21页> M2 用户工作台-F2 我的任务-P1 进行中-拆字-查看详情

### 1 获取进行中的拆字任务列表

*Method GET*


`/api/v1/workbench/tasks?user_id=&business_type=2&task_status=1&page=&page_size=&hanzi=&source=&split=&similar_parts=&task_package_id=`

*Parameters*

| Field | Desc |
|:------|:-----|
| user_id | 用户ID |
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| task_status | 任务状态 1:进行中; 2:完成 |
| page_size | 分页大小（default 20） |
| page | 页序号，从1开始（default） |
| 搜索参数 |以下作为搜索时参数；无搜索参数按照任务编号生序排列
| hanzi | 汉字编码  unicode/图片id |
| source | 来源 0:Unicode; 1:台湾异体字; 2:汉语大字典;3:高丽异体字;4:敦煌俗字典;5:其他|
| split | 拆分序列 |
| similar_parts | 相似部件 |
| task_package_id | 任务包ID |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/tasks/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "录",
			"hanzi_pic_id": "",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		},
		{
			"id": 2,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "焰",
			"hanzi_pic_id": "回1",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		},
		{
			"id": 3,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "我",
			"hanzi_pic_id": "查2",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第21页> M2 用户工作台-F2 我的任务-P1 进行中-录入-查看详情

### 1 获取进行中的录入任务列表


*Method GET*


`/api/v1/workbench/tasks?user_id=&business_type=1&task_status=1&page=&page_size=&hanzi=&variant_type=&input_page=&remark=&task_package_id=`

*Parameters*

| Field | Desc |
|:------|:-----|
| user_id | 用户ID |
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| task_status | 任务状态 1:进行中；2:完成 |
| page_size | 分页大小（default 20） |
| page | 页序号，从1开始（default） |
| 搜索参数 |以下作为搜索时参数；无搜索参数按照任务编号生序排列 |
| hanzi | 汉字编码  unicode/图片id |
| variant_type | 汉字正异类型  0:纯正字;1:狭义异体字;2:广义且正字;3:广义异体字;4:狭义且正字;5:特定异体字;6:特定且正字;7:误刻误印;8:其他不入库类型;9:其他入库类型|
| input_page | 原始图片对应页码 |
| remark | 备注 |
| task_package_id | 任务包ID |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/tasks/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "录",
			"hanzi_pic_id": "",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		},
		{
			"id": 2,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "焰",
			"hanzi_pic_id": "回1",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		},
		{
			"id": 3,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "我",
			"hanzi_pic_id": "查2",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第22页> M2 用户工作台-F2 我的任务-P1 进行中-去重-查看详情

### 1 获取进行中的去重任务列表


*Method GET*


`/api/v1/workbench/tasks?user_id=&business_type=3&task_status=1&page=&page_size=`

*Parameters*

| Field | Desc |
|:------|:-----|
| user_id | 用户ID |
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| task_status | 任务状态 0:未开始；1:进行中；2:完成 |
| page_size | 分页大小（default 20） |
| page | 页序号，从1开始（default） |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/tasks/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"source": "高丽异体字",
			"hanzi_char": "录",
			"hanzi_pic_id": "",
		},
		{
			"id": 2,
			"source": "高丽异体字",
			"hanzi_char": "焰",
			"hanzi_pic_id": "回1",
		},
		{
			"id": 3,
			"source": "高丽异体字",
			"hanzi_char": "我",
			"hanzi_pic_id": "查2",
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第22页> M2 用户工作台-F2 我的任务-P2 已完成

###1 获取已完成的任务列表

*Method GET*



`/api/v1/workbench/tasks?user_id=&page=&page_size=`

*Parameters*

| Field | Desc |
|:------|:-----|
| user_id | 用户ID |
| page_size | 分页大小（default 5） |
| page | 页序号，从1开始（default） |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"business_type": "录入",
			"business_stage": "初次",
			"task_package_id": 100,
			"task_create_date": "2016-11-10",
			"task_done_date": "2016-11-20",
		},
		{
			"id": 2,
			"business_type": "拆字",
			"business_stage": "回查",
			"task_package_id": 100,
			"task_create_date": "2016-11-10",
			"task_done_date": "2016-11-20",
		},
		{
			"id": 3,
			"business_type": "去重",
			"business_stage": "审查",
			"task_package_id": 100,
			"task_create_date": "2016-11-10",
			"task_done_date": "2016-11-20",
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第23页> M2 用户工作台-F2 我的任务-P3 领任务

### 1 添加任务包

*Method POST*



`/api/v1/workbench/task_packages?business_type=&business_stage=&size=&daily_plan=`

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| size | 任务包大小 |
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

##<产品图第24页> M2 用户工作台-F2 我的任务-F1 拆字-P1 初次-未发帖
##<产品图25页> M2 用户工作台-F2 我的任务-F1 拆字-P3 拆字综合信息页面
##<产品图第27页> M2 用户工作台-F2 我的任务-F1 拆字-P4 回查/P5 审查

### 1 获取一个待拆字信息

>注意：
>与进行中的拆字查看API，差别在是否进行分页。
>如果有分页参数，就是批量。
>没有分页参数，就是单字。

>“太难，跳过” 直接调用此API获取新字

>拆字详情，同此API

*Method GET*

`/api/v1/workbench/tasks?business_type=2&task_status=1`

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| task_status | 任务状态 1:进行中; 2:已完成 |
| user_id | 用户ID|
| task_package_id | 任务包ID |

*Response*

```json
成功 Code 200
{
	"id": 1025,
	"source": "高丽异体字",
	"hanzi_type": "文字且图片",
	"hanzi_char": "明",
	"hanzi_pic_id": "初1",

	"is_hard_draft": "",
	"init_split_draft": "",
	"other_init_split_draft": "",
	"deform_split_draft": "",
	"similar_parts_draft": "",
	"dup_id_draft": "",

	"is_hard_review": "",
	"init_split_review": "",
	"other_init_split_review": "",
	"deform_split_review": "",
	"similar_parts_review": "",
	"dup_id_review": "",

	"is_hard_final": "",
	"init_split_final": "",
	"other_init_split_final": "",
	"deform_split_final": "",
	"similar_parts_final": "",
	"dup_id_final": "",

	"user_id": 23,
	"task_package_id": 10
}

失败 Code >= 400
{
	"detail": ""
}
```


### 2 提交一个（存疑）待拆字，并转下一条

> 存疑提交时，自动发送求助帖。

*Method PUT*

`/api/v1/workbench/tasks/{id}`

*Post Data*

```Content-type: application/json
{
	"user_id": 12
	"task_package_id": 10
	"business_type": 2,
	"business_stage": 1,
	"task_status": 2
	"is_hard": "",
	"init_split": "",
	"other_init_split": "",
	"deform_split": "",
	"similar_parts": "",
	"dup_id": "",
	"doubt" : 0
}
```

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| user_id | 用户ID|
| task_package_id | 任务包ID |
| task_status | 任务状态 0:未开始；1:进行中；2:已完成 |
| is_hard | 是否是难字 0=否； 1=是|
| init_split | 初次拆分序列 |
| other_init_split | 再次拆分序列 |
| deform_split | 调笔拆分序列 |
| similar_parts | 相似部件 |
| dup_id | 重复字ID |
| doubt | 是否对拆字结果存疑  0:无; 1:是 |

*Response*

```json
成功 Code 200,  返回待拆字数据
{
	"id": 1027,
	"source": "高丽异体字",
	"hanzi_type": "文字且图片",
	"hanzi_char": "日",
	"hanzi_pic_id": "月1",

	"is_hard_draft": "",
	"init_split_draft": "",
	"other_init_split_draft": "",
	"deform_split_draft": "",
	"similar_parts_draft": "",
	"dup_id_draft": "",

	"is_hard_review": "",
	"init_split_review": "",
	"other_init_split_review": "",
	"deform_split_review": "",
	"similar_parts_review": "",
	"dup_id_review": "",

	"is_hard_final": "",
	"init_split_final": "",
	"other_init_split_final": "",
	"deform_split_final": "",
	"similar_parts_final": "",
	"dup_id_final": "",
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第27页> M2 用户工作台-F2 我的任务-F2 去重-P1 初次-未发帖
##<产品图第29页> M2 用户工作台-F2 我的任务-F2 去重-P3 回查
##<产品图第30页> M2 用户工作台-F2 我的任务-F2 去重-P4 审查

> 这里的去重，只包括字典间去重（目前是台湾字典和高丽字典）。
>
> 高丽内部去重已经完成。表中数据做为回查用。

### 1 获取待去重字信息

*Method GET*


`/api/v1/workbench/tasks?business_type=3& business_stage=&task_status=1`

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| task_status | 任务状态 1:进行中; 2:已完成 |
| user_id | 用户ID|
| task_package_id | 任务包ID |

*Response*

>以下关系中，id为112的汉字‘白’作为其他字中，字段std_hanzi搜索的结果就是variants数组。

```json
成功 Code 200
{
	"taiwan_variants" : {
		"id": 112,
		"std_hanzi": "白",
		"variants": [
			{"id":100, "hanzi_char": "百", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "所2"},
			{"id":101, "hanzi_char": "曰", "hanzi_pic_id": "了1", "inter_dict_dup_hanzi": ""}
		]
	},

	"korean_variants" : {
		"id": 321,
		"std_hanzi": "洗1",
		"variants": [
			{"id": 200, "hanzi_char": "先2", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "百"},
			{"id": 300, "hanzi_char": "和2", "hanzi_pic_id": "人2", "inter_dict_dup_hanzi": ""}
		]
	}
}

失败 Code >= 400
{
	"detail": ""
}
```

### 2 提交一个（存疑）去重字

> 存疑提交时，自动发送求助帖

*Method PUT*

`/api/v1/workbench/tasks/{id}`

*Post Data*

```Content-type: application/json
{
	"user_id": 12
	"task_package_id": 10
	"business_type": 3,
	"business_stage": 1,
	"task_status": 2,
	"doubt" : 0,

	"connections": [
		{
			"taiwan_variants": {"id":100, "hanzi_char": "百", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "所2"},
			"korean_variants": [{"id": 200, "hanzi_char": "", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "百"}]
		}
	]
}
```

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| user_id | 用户ID|
| task_package_id | 任务包ID |
| task_status | 任务状态 0:未开始；1:进行中；2:已完成 |
| doubt | 是否对拆字结果存疑  0:无; 1:是 |

*Response*

```json
成功 Code 200,  返回待拆字数据
{
	"taiwan_variants" : {
		"id": 112,
		"std_hanzi": "白",
		"variants": [
			{"id":100, "hanzi_char": "百", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "所2"},
			{"id":101, "hanzi_char": "曰", "hanzi_pic_id": "了1", "inter_dict_dup_hanzi": ""}
		]
	},

	"korean_variants" : {
		"id": 321,
		"std_hanzi": "洗1",
		"variants": [
			{"id": 200, "hanzi_char": "先2", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "百"},
			{"id": 300, "hanzi_char": "和2", "hanzi_pic_id": "人2", "inter_dict_dup_hanzi": ""}
		]
	}
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第30页> M2 用户工作台-F2 我的任务-F3 录入-P1 初次-未发帖
##<产品图第33页> M2 用户工作台-F2 我的任务-F3 录入-P3 回查/P4 审查


### 1 获取待校对的录入字信息

*Method GET*


`/api/v1/workbench/tasks?business_type=3& business_stage=&task_status=1&page_num=`

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| task_status | 任务状态 1:进行中; 2:已完成 |
| user_id | 用户ID|
| task_package_id | 任务包ID |

*Response*

>以下关系中，id为112的汉字‘白’作为其他字中，字段std_hanzi搜索的结果就是variants数组。

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	Models: [
		{
			"id": 123,
			"volume_num": 2,
			"page_num" : 890,
			"seq_num_draft": "",
			"hanzi_char_draft": "",
			"hanzi_pic_id_draft": "",
			"variant_type_draft": "",
			"std_hanzi_draft": "",
			"notes_draft": "",
			"is_del_draft": "",
			"seq_num_review": "",
			"hanzi_char_review": "",
			"hanzi_pic_id_review": "",
			"variant_type_review": "",
			"std_hanzi_review": "",
			"notes_review": "",
			"is_del_review": "",
			"seq_num_final": "",
			"hanzi_char_final": "",
			"hanzi_pic_id_final": "",
			"variant_type_final": "",
			"std_hanzi_final": "",
			"notes_final": "",
			"is_del_final": "",
			"remark": ""
		},
		{
			"id": 150,
			"volume_num": 2,
			"page_num" : 890,
			"seq_num_draft": "",
			"hanzi_char_draft": "",
			"hanzi_pic_id_draft": "",
			"variant_type_draft": "",
			"std_hanzi_draft": "",
			"notes_draft": "",
			"is_del_draft": "",
			"seq_num_review": "",
			"hanzi_char_review": "",
			"hanzi_pic_id_review": "",
			"variant_type_review": "",
			"std_hanzi_review": "",
			"notes_review": "",
			"is_del_review": "",
			"seq_num_final": "",
			"hanzi_char_final": "",
			"hanzi_pic_id_final": "",
			"variant_type_final": "",
			"std_hanzi_final": "",
			"notes_final": "",
			"is_del_final": "",
			"remark": ""
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

### 2 提交一个（存疑）校对录入字

> 存疑提交时，自动发送求助帖

*Method PUT*

`/api/v1/workbench/tasks/{id}`

*Post Data*

```Content-type: application/json
{
	"user_id": 12
	"task_package_id": 10
	"business_type": 3,
	"business_stage": 1,
	"task_status": 2,
	"doubt" : 0,
	"volumn_num": 2,
	"page_num": 230,
	"seq_num": "",
	"hanzi_char": "",
	"hanzi_pic_id": "",
	"variant_type": "",
	"std_hanzi": "",
	"notes": "",
	"is_del": "",
}
```

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| business_stage | 任务阶段  1:初次，2:回查，3:审核 |
| user_id | 用户ID|
| task_package_id | 任务包ID |
| task_status | 任务状态 0:未开始；1:进行中；2:已完成 |
| doubt | 是否对拆字结果存疑  0:无; 1:是 |
| volumn_num | 汉语大字典册序号 |
| page_num | 汉语大字典页码 |



*Response*

```json
成功 Code 200
{
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图第33页> M2 用户工作台-F3 字库检索-P1 龙泉字库
##<产品图第35页> M2 用户工作台-F3 字库检索-P1 龙泉字库-详情

### 1 龙泉字库查询

*Method GET*

`/api/v1/workbench/hanzilib?hanzi=&hanzi_type=&hanzi_code=&source=&variant_type=&std_hanzi=&strokes=&dup_count=&dup_hanzi=&split=&similar_parts=`

*Parameters*

| Field | Desc |
|:------|:-----|
| hanzi | 汉字编码  unicode |
| hanzi_type | 图片id |
| hanzi_code | 字形编码（图片字编码，兼正字码，位置统一码）
| source | 来源 0:Unicode; 1:台湾异体字; 2:汉语大字典;3:高丽异体字;4:敦煌俗字典;5:其他|
| variant_type | 汉字正异类型  0:纯正字;1:狭义异体字;2:广义且正字;3:广义异体字;4:狭义且正字;5:特定异体字;6:特定且正字;7:误刻误印;8:其他不入库类型;9:其他入库类型|
| split | 拆分序列 |
| std_hanzi | 所属正字编码 |
| strokes | 笔画数 |
| dup_count | 重复次数 |
| dup_hanzi | 重复字编码，对应inter_dict_dup_hanzi和korean_dup_hanzi |
| split | 拆分信息 |
| similar_parts | 相似部件 |


*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"source": 0,
			"hanzi_char": "录",
			"hanzi_pic_id": "",
			"variant_type": "",
			"std_hanzi": "",
			"seq_id" : 123,
			"pinyin" : "lu",
			"radical" : "",
			"strokes": "",
			"zheng_code": "FSKI",
			"is_redundant": 0,
			"dup_count": 0,
			"inter_dict_dup_hanzi": "",
			"korean_dup_hanzi": "",
			"is_hard": 0
			"similar_parts": "",
			"min_split": "",
			"max_split": "",
			"mix_split": "",
			"deform_split": "",
			"similar_parts": "",
			"stroke_serial": ""
		},
		{
			"id": 2,
			"source": 2,
			"hanzi_char": "对",
			"hanzi_pic_id": "",
			"variant_type": "",
			"std_hanzi": "",
			"seq_id" : 31,
			"pinyin" : "lu",
			"radical" : "",
			"strokes": "",
			"zheng_code": "FSKI",
			"is_redundant": 0,
			"dup_count": 1,
			"inter_dict_dup_hanzi": "",
			"korean_dup_hanzi": "",
			"is_hard": 0
			"similar_parts": "",
			"min_split": "",
			"max_split": "",
			"mix_split": "",
			"deform_split": "",
			"similar_parts": "",
			"stroke_serial": ""
		},
		{
			"id": 10,
			"source": 3,
			"hanzi_char": "是",
			"hanzi_pic_id": "",
			"variant_type": "",
			"std_hanzi": "",
			"seq_id" : 12,
			"pinyin" : "lu",
			"radical" : "",
			"strokes": "",
			"zheng_code": "FSKI",
			"is_redundant": 0,
			"dup_count": 1,
			"inter_dict_dup_hanzi": "",
			"korean_dup_hanzi": "",
			"is_hard": 0
			"similar_parts": "",
			"min_split": "",
			"max_split": "",
			"mix_split": "",
			"deform_split": "",
			"similar_parts": "",
			"stroke_serial": ""
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

### 2 更改字库数据
*Method PUT*

`/api/v1/workbench/hanzilib/{id}`

*Post Data*

```Content-type: application/json
{
	"user_id": 12
	"source": 3,
	"hanzi_type": "是",
	"hanzi_char": "是",
	"hanzi_pic_id": "",
	"variant_type": "",
	"std_hanzi": "",
	"seq_id" : 12,
	"pinyin" : "lu",
	"radical" : "",
	"strokes": "",
	"zheng_code": "FSKI",
	"is_redundant": 0,
	"dup_count": 10,
	"inter_dict_dup_hanzi": "",
	"korean_dup_hanzi": "",
	"is_hard": 0
	"similar_parts": "",
	"min_split": "",
	"max_split": "",
	"mix_split": "",
	"deform_split": "",
	"similar_parts": "",
	"stroke_serial": ""
}
```

*Parameters*

| Field | Desc |
|:------|:-----|
| hanzi | 汉字编码  unicode |
| hanzi_type | 图片id |
| hanzi_code | 字形编码（图片字编码，兼正字码，位置统一码）
| source | 来源 0:Unicode; 1:台湾异体字; 2:汉语大字典;3:高丽异体字;4:敦煌俗字典;5:其他|
| variant_type | 汉字正异类型  0:纯正字;1:狭义异体字;2:广义且正字;3:广义异体字;4:狭义且正字;5:特定异体字;6:特定且正字;7:误刻误印;8:其他不入库类型;9:其他入库类型|
| split | 拆分序列 |
| std_hanzi | 所属正字编码 |
| strokes | 笔画数 |
| dup_count | 重复次数 |
| dup_hanzi | 重复字编码，对应inter_dict_dup_hanzi和korean_dup_hanzi |
| split | 拆分信息 |
| similar_parts | 相似部件 |



*Response*

```json
成功 Code 200
{
}

失败 Code >= 400
{
	"detail": ""
}
```



##<产品图36页> M2 用户工作台-F3 字库检索-P2 异体字拆字
### 1 拆字查询

*Method GET*

`/api/v1/workbench/split?hanzi=3&pic_id=&source=&stage=&split=&similar_parts=`

*Parameters*

| Field | Desc |
|:------|:-----|
| hanzi | 汉字编码  unicode |
| pic_id | 图片id |
| source | 来源 0:Unicode; 1:台湾异体字; 2:汉语大字典;3:高丽异体字;4:敦煌俗字典;5:其他|
| split | 拆分序列 |
| similar_parts | 相似部件 |
| stage | 阶段  1:初次 2:回查 3:审查 |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "录",
			"hanzi_pic_id": "",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		},
		{
			"id": 2,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "焰",
			"hanzi_pic_id": "回1",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		},
		{
			"id": 3,
			"task_package_id": 123,
			"source": "高丽异体字",
			"hanzi_char": "我",
			"hanzi_pic_id": "查2",
			"is_hard": "",
			"init_split": "",
			"other_init_split": "",
			"deform_split": "",
			"similar_parts": "",
			"dup_id": "",
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图37页> M2 用户工作台-F3 字库检索-P3 高丽台湾异体字去重

### 1 查询去重字头表
> 这里查询的是 korean\_dup\_characters 表

*Method GET*

`/api/v1/workbench/inter_dict_dedup?tw_hanzi=&kr_hanzi=&stage=`

*Parameters*

| Field | Desc |
|:------|:-----|
| tw_hanzi | 台湾汉字编码  unicode |
| kr_hanzi | 高丽汉字编码 unicode 或 图片id |
| stage | 阶段  1:初次 2:回查 3:审查 |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"korean_variant": "",
			"unicode": "字",
			"stage": 1,
		},
		{
			"id": 23,
			"korean_variant": "",
			"unicode": "",
			"stage": 1,
		},
		{
			"id": 44,
			"korean_variant": "",
			"unicode": "",
			"stage": 1,
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

### 2 详细去重信息


##<产品图38页> M2 用户工作台-F3 字库检索-P4 高丽异体字去重

### 1 查询

*Method GET*

`/api/v1/workbench/korean_dedup?&kr_hanzi=`

*Parameters*

| Field | Desc |
|:------|:-----|
| kr_hanzi | 高丽汉字编码 unicode 或 图片id |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	"results": [
		{
			"id": 1,
			"korean_variant": "",
			"unicode": "字",
			"stage": 1,
		},
		{
			"id": 23,
			"korean_variant": "",
			"unicode": "",
			"stage": 1,
		},
		{
			"id": 44,
			"korean_variant": "",
			"unicode": "",
			"stage": 1,
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

##<产品图39页> M2 用户工作台-F3 字库检索-P4 高丽异体字去重-详情
> 按：这里的详情页，会移到我的任务中。本质上是高丽字典内部去重的一个工作页面。

### 1 查询
>此查询表为korean_dup_zheng_codes。通过郑码将同页数据列出来。

*Method GET*

`/api/v1/workbench/tasks?business_type=4&zheng_code=&page_num=`

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| zheng_code | 指定郑码搜索 |
| page_num | 指定页码 |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	""results"" :[
		{
			"zheng_code": "BUGQ",
			"variants": [
				{"id":100, "hanzi_char": "百", "hanzi_pic_id": "所2", "korean_dup_hanzi": "了1"},
				{"id":101, "hanzi_char": "曰", "hanzi_pic_id": "了1", "korean_dup_hanzi": "百"}
			]
		},

		{
			"zheng_code": "BZB",
			"variants": [
				{"id": 200, "hanzi_char": "先2", "hanzi_pic_id": "所2", "korean_dup_hanzi": ""},
				{"id": 300, "hanzi_char": "和2", "hanzi_pic_id": "人2", "korean_dup_hanzi": ""}
			]
		}
	]
}

失败 Code >= 400
{
	"detail": ""
}
```

### 2 提交一个高丽内部去重字关系

*Method PUT*

`/api/v1/workbench/tasks/{id}`

*Post Data*

```Content-type: application/json
{
	"user_id": 12
	"business_type": 4,
	"zheng_code": "FSIX",
	"connections": [
			{"id":100, "hanzi_char": "百", "hanzi_pic_id": "发2", "inter_dict_dup_hanzi": "所2"},
			{"id": 200, "hanzi_char": "", "hanzi_pic_id": "所2", "inter_dict_dup_hanzi": "百"}
		}
	]
}
```

*Parameters*

| Field | Desc |
|:------|:-----|
| business_type | 任务类型  1:录入, 2:拆字，3:去重 4:高丽内部去重 |
| zheng_code | 郑码 |

*Response*

```json
成功 Code 200
{
}

失败 Code >= 400
{
	"detail": ""
}
```



##<产品图40页> M2 用户工作台-F3 字库检索-P5 异体字录入

*Method GET*

`/api/v1/workbench/input?hanzi=&page_num=&variant_type=&stage=`

*Parameters*

| Field | Desc |
|:------|:-----|
| hanzi | 汉字编码  unicode或图片ID |
| page_num | 汉字大字典的页码 |
| variant_type | 汉字正异类型  0:纯正字;1:狭义异体字;2:广义且正字;3:广义异体字;4:狭义且正字;5:特定异体字;6:特定且正字;7:误刻误印;8:其他不入库类型;9:其他入库类型|
| stage | 录入校对的阶段 1:初次，2:回查，3:审核 |

*Response*

```json
成功 Code 200
{
	"count": 954,
    "next": "http://localhost:8000/api/v1/workbench/{action}/?limit=5&offset=5",
    "previous": null,

	"Models": [
		{
			"volumn_num": 2,
			"page_num": 230,
			"seq_num": "",
			"hanzi_char": "",
			"hanzi_pic_id": "",
			"variant_type": "",
			"std_hanzi": "",
			"notes": "",
			"is_del": "",
		},
		{
			"volumn_num": 2,
			"page_num": 230,
			"seq_num": "",
			"hanzi_char": "",
			"hanzi_pic_id": "",
			"variant_type": "",
			"std_hanzi": "",
			"notes": "",
			"is_del": "",
		},
	]
}

失败 Code >= 400
{
	"detail": ""
}
```


##<产品图41页> M2 用户工作台-F4 讨论区-P1 拆字
