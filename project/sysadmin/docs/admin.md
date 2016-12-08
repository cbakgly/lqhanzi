运营管理后台API设计
==================

### 1. 操作日志类 API
> 所有的操作日志合并成一个API， 目的是减少API的量和重复

|Page| Content|
|-----|----------------------------------------|
|3  | M3  运营管理后台-F1  任务包管理-P3 操作日志 |
|7  |M3  运营管理后台-F2  任务 管理-P4 操作日志 |
|15 | M3  运营管理后台-F5  奖品管理-P3 操作日志 |
|19 |M3  运营管理后台-F6  讨论区管理-P4 操作日志 |
|23 |M3  运营管理后台-F7  用户管理-P4 操作日志 |

|logtype | Num |
|:-------:|:-----:|
| 任务包管理操作日志 | 0 |
| 任务管理操作日志 | 1 |
| 奖品管理操作日志 | 2 |
| 讨论区管理操作日志 | 3 |
| 用户管理操作日志 | 4 |

*METHOD: GET*

*URL:* `/admin/oplogs/?logtype=&starttime=&endtime=&username=&logkey=`
*URL:* `/admin/oplogs/?logtype=&starttime=&endtime=&userid=&logkey=`

*RESPONSE:*

```json
[
  {"username": "xiaoming", "logtime": "2016-11-23 09:53:00",
    "message": "xiaoming delete task 0001"},
  {"username": "xiaoli", "logtime": "2016-11-22 18:12:10",
    "message": "xiaoli delete task 0002"}
]
```

### 1. M3  运营管理后台-F1  任务包管理-P1 查询
*METHOD: GET*

*URL:* `/admin/mission_packs/sheets/?username=&task_type=&stage=&obtain_time_begin&obtain_time_end=&finish_time_begin=&finish_time_end=`

*RESPONSE:*
```json
[
  {"username": "xianer", "task_type": 0, "taskname": "#0001_异体字拆字", "stage": 0, "state": 0, "dayplan": 100, "target": 200, "obtain_date": "2016-11-21", "expect_finish_date": "2016-11-20", "finished": 20 },

  {"username": "xiansan", "task_type": 1, "taskname": "#0001_异体字拆字", "stage": 2, "state": 1, "dayplan": 108, "target": 210, "obtain_date": "2016-11-21", "expect_finish_date": "2016-11-20", "finished": 60 }
]
```
> 单个任务包的所有信息

*METHOD: GET*

*URL:* `/admin/mission_packs/sheets/1/`

*RESPONSE:*

```json
[
  {"mission_packs_id": 1, "charhead": "", "username": "xiaoz", "indb_time": "2016-11-21 10:20:32", "obtain_time": "2016-11-10 10:20:20", "finish_time": "2016-11-22 10:20:30"},
  {"mission_packs_id": 2, "charhead": "", "username": "xiaoz", "indb_time": "2016-11-21 11:20:32", "obtain_time": "2016-11-10 10:20:20", "finish_time": "2016-11-22 10:20:30"}
]
```

> 修改任务包信息

*METHOD: POST*

*URL:* `/admin/mission_packs/sheets/1/`

*POST DATA:*
> 只能修改每日计划而已

```json
{"mission_pack_id": 1, "dayplan": 10}
```

> 接下来的更详细的跳转此处未定

### 2. M3  运营管理后台-F1  任务包管理-P2 统计
| querytype | code |
|:---------------:|:------:|
|初次任务| 1 |
|回查任务 | 2 |
|审查任务 | 3 |

*METHOD: GET*

*URL:* `/admin/mission_packs/charts/?querytype=`

> 具体返回结果是什么样子的， 最后应该和前台商议

*RESPONSE:*
```json
{"querytype": 1, "done": 70, "ongoing": 30}
```

### 4. M3  运营管理后台-F2  任务管理-P1 查询

*MEDTHOD: GET*

| mission_type | num | # | stage | num | # | state | num |
|:------------:|:---:|:--:|:----:|:---:| :-----:|:--------:|
| 录入         | 0   |---| 初次   | 0   |---| 进行中 | 0 |
|拆字          | 1   |---| 回查   | 1   |---| 未完成 | 1 |
|去重          | 2   |---| 审查   | 2   |---| # |  # |


*URL:* `/admin/missions/sheets/?&username=&mission_id=&state=&stage=&mission_type=&indb_time_begin=&indb_time_end=&obtain_time_begin=&obtain_time_end=&finish_time_begin=&finish_time_end=`

*RESPONSE:*

```json
[
  {"mission_id": 1, "username": "xiansan", "stage": 0, "state": 1, "points": 50, "indb_time": "2016-12-13 20:13:00", "obtain_time": "2016-11-01 11:00:00", "finish_time": "2016-12-20 12:20:10" },
  {"mission_id": 2, "username": "xianz", "stage": 1, "state": 5, "points": 50, "indb_time": "2016-12-13 20:13:00", "obtain_time": "2016-11-01 11:00:00", "finish_time": "2016-12-20 12:20:10" },
  {"mission_id": 3, "username": "xianin", "stage": 3, "state": 2, "points": 50, "indb_time": "2016-12-13 20:13:00", "obtain_time": "2016-11-01 11:00:00", "finish_time": "2016-12-20 12:20:10" }
]
```

#### 4.1 删除未分配任务
> 建议此功能取消， 可以直接由系统定时删除, 但可以留出 API 接口

*METHOD: DELETE*

*URL:* `/admin/missions/sheets/1/`

#### 4.2 查看任务详细信息
> 没看到有图表之类的东东， 所以此API暂时不写， 但可以设置下URL

*METHOD: GET*

*URL:* `/admin/missions/sheets/1/`

### 5. M3  运营管理后台-F2  任务管理-P2 统计
*METHOD: GET*

*URL:* `/admin/missions/charts/bars/?mission_type=`

*URL:* `/admin/missions/charts/lines/?finish_time_begin=&finish_time_end=&username=&stage=`

*RESPONSE:*
> TBD

### 6. M3  运营管理后台-F2  任务管理-P3 回收站
*METHOD: GET/POST*

*URL GET:* `/admin/missions/recycle/?time_begin=&time_end=&keyword=`

*URL POST:* `/admin/missions/recycle/1/drop/`

*URL POST:* `/admin/missions/recycle/1/rollback/`

### 8. M3  运营管理后台-F3  打卡管理-P1 查询
*METOD: GET*

*URL:* `/admin/sign/sheets/?username=&begin_time=&end_time=&logkey=`

*RESPONSE:*

```json
[
  {"username": "adam", "signtime": "2016-11-10 10:11:20", "message": "hello world"},
  {"username": "iaa", "signtime": "2016-11-10 10:11:20", "message": "hello world"},
  {"username": "ann", "signtime": "2016-11-10 10:11:20", "message": "hello world"},
]
```
### 9. M3  运营管理后台-F3  打卡 管理-P2 统计
*METHOD: GET*

*URL:* `/admin/sign/charts/lines/?username=&begin_time=&end_time=`

*RESPONSE:*
> TBD

### 10. M3  运营管理后台-F4  积分管理-P1 查询
*METHOD: GET*

*URL:* `/admin/points/sheets/&total_points_from=&total_points_to=&remain_points_from=&remain_points_to=&username=`

*RESPONSE:*

```json
[
  {"username": "wangz", "total_points": 100, "split_points": 50, "remove_dup_points": 20, "remain_points": 30},

  {"username": "liu", "total_points": 100, "split_points": 50, "remove_dup_points": 20, "remain_points": 30}
]
```
### 11. M3  运营管理后台-F4  积分管理-P2 统计

#### 11.1 当前积分统计
*METHOD: GET*

*URL:* `/admin/points/sheets/current_points/`

*RESPONSE:*

```json
{"total_points": 80000, "split_points": 40000, "remove_dup_points": 20000, "input_points": 20000, "unexchanged_points": 32000}
```

#### 11.2 积分兑换情况统计
*METHOD: GET*

*URL:* `/admin/points/sheets/exchage_statistics/`

*RESPONSE:*

```json
{"applying": 7, "accepting": 3, "done": 16}
```
### 11.3 积分兑换情况折线图
*METHOD: GET*

*URL:* `/admin/points/charts/lines/?begin_time=&end_time=`

*RESPONSE:*
```json
# tbd Give what kind which u want
```
### 12. M3  运营管理后台-F4  积分管理-P3 积分设置

#### 12.1 积分设置查询
*METHOD: GET*

*URL:* `/admin/points/settings/unit_points/`

*RESPONSE:*
```json
[
  {"id": 0, "mission_type": 0, "stage": 0, "unit_points": 1},
  {"id": 1, "mission_type": 1, "stage": 2, "unit_points": 2},
  {"id": 2, "mission_type": 2, "stage": 3, "unit_points": 3},
  {"id": 3, "mission_type": 3, "stage": 1, "unit_points": 4},
  {"id": 4, "mission_type": 2, "stage": 2, "unit_points": 2},
  {"id": 5, "mission_type": 1, "stage": 1, "unit_points": 2},
  {"id": 6, "mission_type": 1, "stage": 3, "unit_points": 2},
  {"id": 7, "mission_type": 2, "stage": 2, "unit_points": 1},
  {"id": 8, "mission_type": 3, "stage": 1, "unit_points": 1}
]
```

#### 12.2 积分设置

*METHOD: POST*

*URL:* `/admin/points/settings/1/`

*POST DATA:*

```json
{"mission_type": 0, "stage": 1, "unit_points": 5}
```

### 12.3 单位积分更改历史查询

*METHOD: GET*

*URL:* `/admin/points/settings/unit_points/1/`

*RESPONSE:*

```json
[
  {"setting_time": "2016-11-01 12:12:01", "unit_points": 2, "notes": "lacks of volunteers"},
  {"setting_time": "2016-12-11 22:05:16", "unit_points": 5, "notes": "lacks of volunteers"}
]
```
#### 13. M3  运营管理后台-F4  积分管理-P4 积分兑换
#### 13.1 查询积分兑换情况
*METHOD: GET*

*URL:* `/admin/points/exchanges/?username=&giftname=&state=`

*RESPONSE:*

```json
[
  {"id": 12, "username": "xiaoli", "state": 1, "giftname": "<life>", "consume": 1000, "applied_time": "2016-11-10 10:20:20", "accepted_time": "2016-11-11 11:20:30", "finish_time": "2016-11-12 12:10:10", "admin":  "xianbai" },

  {"id": 15, "username": "yang", "state": 2, "giftname": "<life>", "consume": 3000, "applied_time": "2016-11-10 10:20:20", "accepted_time": "2016-11-11 11:20:30", "finish_time": "2016-11-12 12:10:10", "admin":  "xianbai" }
]
```

#### 13.2 修改奖品

*METHOD: POST*

*URL:* `/admin/points/exchanges/1/`

*POST DATA:*
```json
{"id": 1, "giftname": "<baifa>"}
```

#### 13.3 受理兑换申请， 受理后奖品不可更改，同时发邮件给用户
> 只需要POST一个URL， 不需要额外数据

*METHOD: POST*

*URL:* `/admin/points/exchanges/1/accept/`

#### 13.4 查看邮件通知内容

*METHOD: GET*

*URL:* `/admin/points/exchanges/1/emails/`

*RESPONSE:*

```json
{"subject": "###", "message": "------"}
```
### 14. M3  运营管理后台-F5  奖品管理-P1 查询
#### 14.1 管理-奖品查询
*METHOD: GET*

*URL:* `/admin/gift/`

*RESPONSE:*
```json
[
  {"id": 1, "giftname": "<life call back>", "state": 0, "stock": 200, "exchanged":  100, "exchange_points": 1000},
  {"id": 2, "giftname": "<a cat>", "state": 0, "stock": 200, "exchanged":  100, "exchange_points": 1000}
]
```
#### 14.2 管理-新增奖品
*METHOD: POST*

*URL:* `/admin/gift/`

*RESPONSE:*
```json
{"giftname": "<HI>", "exchange_points": 500, "stock": 200, "state": 1}
```
#### 14.3 管理-删除奖品
> just use delete

*URL:* `/admin/gift/1/`
#### 14.4 管理-修改奖品
*METHOD: PUT*

*URL:* `/admin/gift/`

```json
{"id": 5, "giftname": "<HI>", "exchange_points": 500, "stock": 200, "state": 1}
```
### 讨论区的管理员管理建议和用户管理合并成一个API
> 目的是减少API的量和重复

|Page | Content                                
|-----|----------------------------------------
|16   |M3  运营管理后台-F6  讨论区管理-P1 查询   
|18   |M3  运营管理后台-F6  讨论区管理-P3 回收站
|20   |M3  运营管理后台-F7  用户管理-P1 查询     
|22   |M3  运营管理后台-F7  用户管理-P3 回收站   

#### 01. 管理 管理员/用户
##### a. 查询管理员或者用户
*METHOD: GET*

> 调用者的用户名和组名是隐含的，权限在此也是隐含的, begin_time or end_time 可以没有
*URL:* `/admin/user_management/?username=&usertype=&begin_time=&end_time=`

*RESPONSE:*

```json
{"userid": 123, "username": "somebody", "empower_time": "2016-11-07 11:20:14"}
{"userid": 456, "username": "bae", "empower_time": "2016-10-08 12:10:28"}
```

#### b. 查看管理员的操作日志
> 同第一个API

#### c. 新增讨论区管理员
> tbd 这个准备和用户管理的管理员做到一起

### 17. M3  运营管理后台-F6  讨论区管理-P2 统计
*METHOD: GET*
> 讨论区帖子， 板块数， 回复数量等等

*URL:* `/admin/forum/sheets/`

*RESPONSE:*

```json
{
  "posting_count": {"input": 352, "split": 1274, "remove_dup": 253},
  "ans_count": {"input": 1468, "split": 1274, "remove_dup": 253},
  "ques_count": {"input": 1468, "split": 1274, "remove_dup": 253},
  "ques_count": {"input": 1468, "split": 1274, "remove_dup": 253},
}
```
> 以下两个主题先放一放
### 21. M3  运营管理后台-F7  用户管理-P2 统计
### 24. M3  运营管理后台-F8  权限管理-P1 查询

> 下面两个主题比较容易些
### 25. M3  运营管理后台-F9  数据 字典-P1 部件集
#### 25.1 查询部件
*METHOD: GET*
`/admin/data_dict/strokes/?stroke=&`

### 26. M3  运营管理后台-F9  数据 字典-P2 部首集

`/admin/data_dict/busu/`
