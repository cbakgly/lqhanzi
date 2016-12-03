运营管理后台
============

## 操作日志合集
> 为了避免重复，多个操作日志合并成一个API
> 对日志类型进行了数字索引，但表意不清楚，具体到项目代码时候
> 也可以更改为字符串。这些具体再议。

|Page | Content                                     |
|-----|---------------------------------------------|
|3    |M3  运营管理后台-F1  任务包管理-P3 操作日志  |
|7    |M3  运营管理后台-F2  任务 管理-P4 操作日志   |
|15   |M3  运营管理后台-F5  奖品管理-P3 操作日志    |
|19   |M3  运营管理后台-F6  讨论区管理-P4 操作日志  |
|23   |M3  运营管理后台-F7  用户管理-P4 操作日志    |

|Logtype             | Num |
|--------------------|-----|
| 任务包管理操作日志 | 0   |
| 任务管理操作日志   | 1   |
| 奖品管理操作日志   | 2   |
| 讨论区管理操作日志 | 3   |
| 用户管理操作日志   | 4   |

*Method: GET*

*Url:* `/api/v1/sysadmin/oplogs/?logtype=&begin_at=&end_at=&username=&logkey=`

*Url:* `/api/v1/sysadmin/oplogs/?logtype=&begin_at=&end_at=&user_id=&logkey=`

*Response:*

```json
[
  {"username": "xiaoming", "logtime": "2016-11-23 09:53:00",
    "message": "xiaoming delete task 0001"},
  {"username": "xiaoli", "logtime": "2016-11-22 18:12:10",
    "message": "xiaoli delete task 0002"}
]
```

## <45>. M3  运营管理后台-F1  任务包管理-P1 查询
> 总体说明：按照用户名、任务类型、任务阶段、任务状态、领取时间、完成时间综合查询任务包，此API下有查询列表、查询详细、修改单个任务包并保存三个API

### 1. 查询任务包列表

*Method: GET*

*Url*
 `/api/v1/sysadmin/task_packages?format=0&username=&task_type=&task_stage=&obtain_begin_at=&obtain_end_at&finish_begin_at=&finish_end_at=`

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
 `/api/v1/sysadmin/task_packages/1/`

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
`/api/v1/sysadmin/task_packages/1/`

*Post Data:*
```json
{"id": 1, "daily_plan": 10}
```
### 3. #8 查看单个任务的详细信息，点击会跳转至 “M2 用户工作台-F2 我的任务”
> 待定，跨APP操作的[tbd]

## <47>. M3  运营管理后台-F1  任务包管理-P2 统计
*Method: GET*

*Url:* `/api/v1/sysadmin/task_packages?format=1&querytype=`

*Response:*
> 只是示例，具体待定
```json
{"querytype": 1, "done": 70, "ongoing": 30}
```

## <47>. M3 运营管理后台-F1  任务包管理-P3 操作日志
> 请查看 *操作日志*

## <48>. M3 运营管理后台-F1 任务管理-P1 查询
### 1. 查询任务
*Method: GET*

| task_type  | num | # | stage| num | # | state |num|
|:----------:|:---:|:-:|:----:|:---:|:-:|:-----:|:--|
|录入        | 0   |---| 初次 | 0   |---| 进行中| 0 |
|拆字        | 1   |---| 回查 | 1   |---| 未完成| 1 |
|去重        | 2   |---| 审查 | 2   |---| #     | # |

*Url:*
`/api/v1/sysadmin/tasks?format=0&username=&task_id=&state=&stage=&task_type=&indb_begin_at&indb_end_at&obtain_begin_at&obtain_end_at&complete_begin_at=&complete_end_at=`

*Response:*

```json
[
  {"task_id": 1, "username": "xiansan", "stage": 0, "state": 1, "points": 50, "indb_at": "2016-12-13 20:13:00", "obtain_time": "2016-11-01 11:00:00", "finish_time": "2016-12-20 12:20:10" },
  {"task_id": 3, "username": "xianin", "stage": 3, "state": 2, "points": 50, "indb_at": "2016-12-13 20:13:00", "obtain_time": "2016-11-01 11:00:00", "finish_time": "2016-12-20 12:20:10" }
]
```

### 2. 查看单个任务详细信息

*Method: GET*

*Url:*
`/api/v1/sysadmin/tasks/1/`

*Response:*

> 没有具体页面，可视情况而定 [tbd]

### 3. 删除未分配任务
> 建议此功能取消， 可以直接由系统定时删除, 但可以留出 API 接口

*METHOD: DELETE*

*URL:* `/api/v1/sysadmin/tasks/1/`

## <49> M3 运营管理后台-F2任务管理-P2统计

### 1. 任务整体情况

*Method: GET*

*Url:*
`/api/v1/sysadmin/tasks?format=1&task_type=0`

*Response:*
> 具体返回格式另行商议

### 2. 日完成量

*Method: GET*

*Url:* `/api/v1/sysadmin/tasks/daily?format=1&complete_begin_at=&complete_end_at=&username=&stage=`

*Response:*
> 具体返回格式另行商议

## <51> M3运营管理后台-F2任务管理-P3回收站

### 1. 查询回收站内的回收任务

*Method: GET*

| Field            | Chinese             |
|------------------|---------------------|
| 查询回收时间开始 | begin_at            |
| 查询回收时间结束 | end_at              |

*Url:* `/api/v1/sysadmin/tasks/trash?username=&begin_at=&end_at=`

*Response:*

```json
[
  {"id": 1, "username": "贤一", "task_type": "拆字", "task_id": 1000, "stage": "初次", "state": "未分配", "in_db_at":
  "2016-11-01 11:30:32", "obtain_at": "2016-11-11 11:30:35", "trash_at": "2016-11-11 11:30:32"}
]
```

### 2. 还原任务

*Method: POST*

*Url:* `/api/v1/sysadmin/tasks/trash/1/restore/`

### 3. 彻底删除任务

*Method: DELETE*

*Url:* `/api/v1/sysadmin/tasks/trash/1/`

## <51> M3运营管理后台-F2任务管理-P4操作日志
> 见 操作日志

## <52> M3运营管理后台-F3打卡管理-P1查询

*Method: GET*

*Url:* `/api/v1/sysadmin/diaries?format=0&username=&begin_at=&end_at=`

*Response:*

```json
[
  {"id": 1, "username": "soby", "logtime": "2016-11-11 12:33:42", "Hello World"}
]
```

## <53> M3运营管理后台-F3打卡管理-P2统计

> 与上面的查询共用一个API，只是返回结果不同罢了, 用format 区别查询内容, 用户名字段应该没啥
> 用处，因为做的是统计，查一个人意义不大，或者可能多次签到。

*Method: GET* 

*Url:* `/api/v1/sysadmin/diaries?format=0&username=&begin_at=&end_at=`

*Response:*
> TBD

## <54> 运营管理后台-F4积分管理-P1查询

*Method: GET*

*Url:*
`/api/v1/sysadmin/credits?username=&total_credits_from=&total_credits_to=&rest_credits_from=&rest_credits_to=&credits_type=`

*Response:*

```json
[
  {"username": "wangxiaoer", "total_credicts": 1100, "split_credits": 10, "input_credits": 20, "remove_dup_credits":
  1070, "rest_credits": 100}
]
```
## <55> 运营管理后台-F4积分管理-P2统计

### 1. 当前积分统计表

*Method: GET*

| Field            | Chinese             |
|------------------|---------------------|
| 总积分           | total_credits       |
| 拆分积分         | total_credits       |
| 输入积分         | input_credits       |
| 去重积分         | remove_dup_credits  |


*Url:* `/api/v1/sysadmin/credits/current/?format=0&type=0`

*Response:*

```json
{"total_credits": 80000, "split_credits": 40000, "remove_dup_credits": 20000, "input_credits": 20000,
"credits_unchanged": 32000}
```

### 2. 当前积分兑换统计表

*Method: GET*

*Url:* `/api/v1/sysadmin/credits/current/?format=0&type=1`

*Method: GET*

*Response:*

```json
[
    {"applying": 7, "accepting": 3, "done": 16}
]
```

### 3. 积分兑换情况，按时段查询

*Method: GET*

*Url:* `/api/v1/sysadmin/credits?begin_at=&end_at=`

*Response:*

#### <56> M3运营后台-F4积分管理-P3积分设置

### 1. 查询积分设置

*Method: GET*

*Url:* `/api/v1/sysadmin/credits/settings/`

*Response:* 

```json
[ {"id": 1, "task_type": 0, "stage": 0, "unit_credits": 1} ]
```

### 2. 修改积分设置

*Method: POST*

*Url:* `/api/v1/sysadmin/credits/settings/1/`

*Post Data:*

```json
{"task_type": 0, "stage": 1, "unit_credits": 5}
```

### 3. 查看历史

*Method: GET*

*Url:* `/api/v1/sysadmin/credits/settings/1/`

*Response:*

```json
[ {"id": 1, "setting_at": "2016-11-01 11:12:13", "unit_credits": 2, "note": "hello world"} ]
```

## <56> M3运营后台-F4积分管理-P4积分兑换

### 1. 查询兑换申请或者受理情况

*Method: GET*

*Url:* `/api/v1/sysadmin/credits/shop?username=&reward_name=&stage=`

*Response:*

```json
[ {"id": 1, "username": "zhangming", "state": 1, "reward_name": "<abc>", "consume_credits": 1000, "applied_at":
"2016-11-12 12:20:10", "accepted_at": "2016-11-12 13:10:15", "complete_at": "2016-11-12 15:10:10", "sysadmin": "xianmm"} ]
```

> 下面几个API是否可以尝试用一个？POST DATA 类型表示不同的操作？

| Action   | Num |
|----------|-----|
| 修改奖品 | 0   |
| 受理申请 | 1   |

### 2. 修改奖品

*Method: POST*

*Url:* `/api/v1/sysadmin/credits/shop/1/`

*Post Data:*

```json
{"action": 0, "reward_name": "<zm>" }
```

### 3. 受理

*Method: POST*

*Post Data:*

```json
{"action": 1 }
```
### 4. 完成

*Method: POST*

*Post Data:*

```json
{"action": 2}
```

### 4. 查看

*Method: GET*

*Url:* `/api/v1/sysadmin/credits/shop/1/`

*Response:*

```json
{"message": "Hello World"}
```

## <57> M3运营管理后台-F5奖品管理-P1查询

### 1. 查询库存奖品

*Method: GET*

*Url:* `/api/v1/sysadmin/rewards/`

*Response:*

```json
[{"id": 1, "reward_name": "<GWRS>", "state": 0, "stocks": 120, "exchanged": 30, "exchange_credits": 1000}]
```

### 2. 修改库存奖品

*Method: POST*

*Url:* `/api/v1/sysadmin/rewords/1/`

*Post Data:*

```json
{"reward_name": "something", "exchange_credits": 1500, "stocks": 80}
```

### 3. 删除某库存

*Method: DELETE*

*Url:* `/api/v1/sysadmin/rewords/1/`

## 以下建议合并成一个API，就是关于用户管理或者管理员管理的，最后只用一个即可。

## <59> M3运营管理后台-F6讨论区管理-P1查询

### 1. 查询讨论区管理员

*Method: GET*

*Url:* `/api/v1/sysadmin/forum/sysadmin/`

## 剩下几个API 可以参考老的稍后写
