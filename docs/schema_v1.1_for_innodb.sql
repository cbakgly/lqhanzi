--1)
--MySQL的timestamp类型是4个字节，最大值是2的31次方减1，也就是2147483647，转换成北京时间就是2038-01-19 11:14:07。
--UNIX_TIMESTAMP 支持转换的最大时间 2038-1-19 11:14:7
--SELECT UNIX_TIMESTAMP('2038-1-19 11:14:7');  #正常
--SELECT UNIX_TIMESTAMP('2038-1-19 11:14:8'); #失败
--FROM_UNIXTIME支持转换的最大时间时间戳 2147483647
--SELECT FROM_UNIXTIME(2147483647); #正常
--SELECT FROM_UNIXTIME(2147483648); #失败
--so c_t int NOT NULL convert to c_t datetime NOT NULL,
--so u_t int NOT NULL convert to u_t datetime NOT NULL,
--2) add AUTO_INCREMENT
--3) index按原来收集的信息加的，后续再测试/运行阶段的时候统一收集一次慢查询日志，分析后更新索引。
--4) add CHARSET COLLATE COMMENT
  
/* 龙泉字库表 */
CREATE TABLE IF NOT EXISTS hanzi_set (
  id INT  NOT NULL AUTO_INCREMENT,

  -- 字典信息
  source tinyint DEFAULT NULL, -- '来源'
  hanzi_type tinyint DEFAULT NULL, -- '字形类型：文字、图片、文字且图片'
  hanzi_char varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi varchar(64) DEFAULT NULL, -- '所属正字'
  as_std_hanzi varchar(32) DEFAULT NULL, -- '兼正字号'
  seq_id varchar(32) DEFAULT NULL, -- ‘字的位置统一编码’
  pinyin varchar(64) DEFAULT NULL, -- '拼音'
  radical varchar(8) DEFAULT NULL, -- '部首'
  strokes tinyint DEFAULT NULL, -- '笔画数'
  zheng_code varchar(32) DEFAULT NULL, -- '郑码'
  wubi varchar(32) DEFAULT NULL, -- '五笔'

  -- 重复信息
  dup_count tinyint DEFAULT NULL, -- '重复次数'
  inter_dict_dup_hanzi varchar(64) DEFAULT NULL, -- '异体字字典间重复编码'
  korean_dup_hanzi varchar(32) DEFAULT NULL, -- '高丽异体字字典内部重复编码'
  is_inter_dict_redundant tinyint DEFAULT NULL, -- '字典间去重是否多余'
  is_korean_redundant tinyint DEFAULT NULL, -- '高丽去重是否多余'

  -- 拆字信息
  structure varchar(16) DEFAULT NULL, -- '结构'
  min_split varchar(255) DEFAULT NULL, -- '初步拆分'
  max_split varchar(512) DEFAULT NULL, -- '最大拆分'
  mix_split varchar(512) DEFAULT NULL, -- '混合拆分'
  deform_split varchar(255) DEFAULT NULL, -- '调笔拆分'
  similar_parts varchar(128) DEFAULT NULL, -- '相似部件'
  stroke_serial varchar(128) DEFAULT NULL, -- '部件序列'

  remark varchar(128) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL,
  u_t datetime NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='龙泉字库表';


/* 异体字拆字业务表 */
CREATE TABLE IF NOT EXISTS variants_split (
  id INT  NOT NULL AUTO_INCREMENT,

  -- 字典信息
  source tinyint DEFAULT NULL, -- '来源'
  hanzi_type tinyint DEFAULT NULL, -- '字形类型：文字、图片、文字且图片'
  hanzi_char varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi varchar(64) DEFAULT NULL, -- '所属正字'
  as_std_hanzi varchar(32) DEFAULT NULL, -- '兼正字号'
  seq_id varchar(32) DEFAULT NULL, -- '字的位置统一编码

  -- 重复信息
  is_redundant tinyint DEFAULT NULL, -- '是否多余'

  -- 初次
  skip_num_draft tinyint DEFAULT NULL, -- '太难跳过次数'
  init_split_draft varchar(128) DEFAULT NULL, -- '初步拆分'
  other_init_split_draft varchar(128) DEFAULT NULL, -- '其它初步拆分'
  deform_split_draft varchar(128) DEFAULT NULL, -- '调笔拆分'
  similar_parts_draft varchar(64) DEFAULT NULL, -- '相似部件'
  dup_id_draft varchar(32) DEFAULT NULL, -- '重复ID'

  -- 回查
  skip_num_review tinyint DEFAULT NULL, -- '太难跳过次数'
  init_split_review varchar(128) DEFAULT NULL, -- '初步拆分'
  other_init_split_review varchar(128) DEFAULT NULL, -- '其它初步拆分'
  deform_split_review varchar(128) DEFAULT NULL, -- '调笔拆分'
  similar_parts_review varchar(64) DEFAULT NULL, -- '相似部件'
  dup_id_review varchar(32) DEFAULT NULL, -- '重复ID'

  -- 审查
  skip_num_final tinyint DEFAULT NULL, -- '太难跳过次数'
  init_split_final varchar(128) DEFAULT NULL, -- '初步拆分'
  other_init_split_final varchar(128) DEFAULT NULL, -- '其它初步拆分'
  deform_split_final varchar(128) DEFAULT NULL, -- '调笔拆分'
  similar_parts_final varchar(64) DEFAULT NULL, -- '相似部件'
  dup_id_final varchar(32) DEFAULT NULL, -- '重复ID'


  -- 辅助审查及提交入库
  is_draft_equals_review tinyint DEFAULT NULL,  -- '初次回查是否相等'
  
  is_review_equals_final tinyint DEFAULT NULL,  -- '回查审查是否相等'
  is_checked tinyint DEFAULT 0, -- '是否人工审核'

  
  is_submitted tinyint DEFAULT 0, -- '是否入hanzi库'


  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL,
  u_t datetime NOT NULL,
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='异体字拆字业务表';


/* 异体字录入业务表 */
CREATE TABLE IF NOT EXISTS variants_input (
  id INT  NOT NULL AUTO_INCREMENT,

  -- 基本信息
  volume_num tinyint DEFAULT NULL, -- '册' 
  page_num int DEFAULT NULL, -- '页码' 

  -- 初次
  seq_num_draft tinyint DEFAULT NULL, -- '序号'
  hanzi_char_draft varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id_draft varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type_draft tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi_draft varchar(64) DEFAULT NULL, -- '所属正字'
  notes_draft varchar(64) DEFAULT NULL, -- '注释信息'
  is_del_draft tinyint DEFAULT NULL, -- '是否删除'

  -- 回查
  seq_num_review tinyint DEFAULT NULL, -- '序号'
  hanzi_char_review varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id_review varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type_review tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi_review varchar(64) DEFAULT NULL, -- '所属正字'
  notes_review varchar(64) DEFAULT NULL, -- '注释信息'
  is_del_review tinyint DEFAULT NULL, -- '是否删除'

  -- 审查
  seq_num_final tinyint DEFAULT NULL, -- '序号'
  hanzi_char_final varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id_final varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type_final tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi_final varchar(64) DEFAULT NULL, -- '所属正字'
  notes_final varchar(64) DEFAULT NULL, -- '注释信息'
  is_del_final tinyint DEFAULT NULL, -- '是否删除'



  -- 辅助审查及提交入库
  
  is_draft_equals_review tinyint DEFAULT NULL, -- '初次回查是否相等'
  
  is_review_equals_final tinyint DEFAULT NULL, -- '回查审查是否相等'
  
  is_checked tinyint DEFAULT 0, -- '是否人工审核'

  
  is_submitted tinyint DEFAULT 0,  -- '是否入hanzi库'


  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL,
  u_t datetime NOT NULL,
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='异体字录入业务表';


/* 高丽异体字字典 */
CREATE TABLE IF NOT EXISTS korean_variants_dict (
  id INT  NOT NULL AUTO_INCREMENT,
  glyph varchar(16) DEFAULT NULL, -- '字形'
  code varchar(16) DEFAULT NULL, -- 'Unicode'
  busu_id INT DEFAULT NULL, -- '部首ID，对应于hanzi_radicals的id'
  totalstrokes tinyint DEFAULT NULL, -- '总笔画'
  reststrokes tinyint DEFAULT NULL, -- '剩余笔画'
  jungma varchar(64) DEFAULT NULL, -- '郑码'
  standard varchar(16) DEFAULT NULL, -- '正字Unicode码'
  ksound varchar(16) DEFAULT NULL, -- '韩文发音'
  kmean varchar(128) DEFAULT NULL, -- '韩文含义'
  banjul varchar(64) DEFAULT NULL, -- '反切'
  csound varchar(64) DEFAULT NULL, -- '中文发音'
  cmean varchar(128) DEFAULT NULL, -- '中文含义'
  jsound varchar(64) DEFAULT NULL, -- '日文发音'
  jmean varchar(128) DEFAULT NULL, -- '日文含义'
  emean varchar(128) DEFAULT NULL, -- '英文含义'
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='高丽异体字字典';


/* 汉字部首表 */
CREATE TABLE IF NOT EXISTS hanzi_radicals (
  id INT  NOT NULL AUTO_INCREMENT,
  radical varchar(16) DEFAULT NULL, -- '部首'
  strokes tinyint DEFAULT NULL,  -- '笔画数'
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='汉字部首表';

/* 高丽异体字内部去重-待去重郑码表 */
CREATE TABLE IF NOT EXISTS korean_dup_zheng_codes (
  id INT  NOT NULL AUTO_INCREMENT,
  zheng_code VARCHAR(32) NOT NULL,  -- '郑码'
  count tinyint NOT NULL, -- '郑码对应汉字的数量'
  page_num smallint DEFAULT NULL, -- '页码'
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='高丽异体字内部去重-待去重郑码表';


/* 高丽异体字去重-去重结果表 */
CREATE TABLE IF NOT EXISTS korean_dedup (

  id INT  NOT NULL AUTO_INCREMENT,

  -- 高丽异体字字典信息
  source tinyint DEFAULT NULL, -- '来源'
  hanzi_type tinyint DEFAULT NULL, -- '字形类型：文字、图片、文字且图片'
  hanzi_char varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi varchar(64) DEFAULT NULL, -- '所属正字'
  zheng_code varchar(32) DEFAULT NULL, -- '郑码'

  -- 重复信息
  korean_dup_hanzi varchar(32) DEFAULT NULL, -- '异体字字典内部重复编码'

  remark VARCHAR(64) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL,
  u_t datetime NOT NULL,
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='高丽异体字去重-去重结果表';



/* 高丽台湾异体字去重-高丽字头表 */
CREATE TABLE IF NOT EXISTS korean_dup_characters (
  id INT  NOT NULL AUTO_INCREMENT,
  korean_variant VARCHAR(32) NOT NULL,  -- '高丽字头'
  unicode VARCHAR(32) NOT NULL,  -- '与字头字形相同/相近的Unicode'
  relation SMALLINT DEFAULT NULL,  -- '二者关系：形码均相同，形似码相同，形同码不同，无相同字形'
  remark VARCHAR(128) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL,
  u_t datetime NOT NULL,
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='高丽台湾异体字去重-高丽字头表';



/* 高丽台湾异体字去重结果表 */
CREATE TABLE IF NOT EXISTS inter_dict_dedup (
  id INT  NOT NULL AUTO_INCREMENT,

  -- 字典信息
  source tinyint DEFAULT NULL, -- '来源'
  hanzi_type tinyint DEFAULT NULL, -- '字形类型：文字、图片、文字且图片'
  hanzi_char varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi varchar(64) DEFAULT NULL, -- '所属正字'
  as_std_hanzi varchar(32) DEFAULT NULL, -- '兼正字号'

  -- 重复信息
  inter_dict_dup_hanzi_draft varchar(64) DEFAULT NULL, -- '异体字字典间重复编码'
  inter_dict_dup_hanzi_review varchar(64) DEFAULT NULL, -- '异体字字典间重复编码'
  inter_dict_dup_hanzi_final varchar(64) DEFAULT NULL, -- '异体字字典间重复编码'

  -- 辅助审查及提交入库
  is_draft_equals_review tinyint DEFAULT NULL,  -- '初次回查是否相等'
  is_review_equals_final tinyint DEFAULT NULL,  -- '回查审查是否相等'
  is_checked tinyint DEFAULT 0, -- '是否人工审核'
  is_submitted tinyint DEFAULT 0, -- '是否入hanzi库'

  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL,
  u_t datetime NOT NULL,
  PRIMARY KEY(`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='高丽台湾异体字去重结果表';


/* 任务池 */
CREATE TABLE IF NOT EXISTS tasks (
  id INT  NOT NULL AUTO_INCREMENT,
  user_id INT DEFAULT NULL, -- '拆字员'
  task_package_id INT(11) DEFAULT NULL, -- '任务包ID'
  business_id INT(11) NOT NULL, -- '业务ID，指的是对应于拆字、去重、录入业务表的ID'
  
  business_type tinyint DEFAULT NULL, -- '任务类型'
  business_stage tinyint DEFAULT NULL, -- '任务阶段'
  task_status tinyint DEFAULT NULL, -- '任务状态'
  credits SMALLINT DEFAULT NULL, -- '积分'
  remark VARCHAR(128) DEFAULT NULL, -- '备注'
  assigned_at INT NOT NULL, -- '分配时间'
  completed_at INT NOT NULL,  -- '完成时间' 
  c_t datetime NOT NULL, -- '创建时间'
  u_t datetime NOT NULL, -- '修改时间'
  PRIMARY KEY(`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='任务池';

/* 任务包 */
CREATE TABLE IF NOT EXISTS task_packages (
  id INT  NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL, -- '用户id'
  business_type tinyint DEFAULT NULL, -- '任务类型'
  business_stage tinyint DEFAULT NULL, -- '任务阶段'
  size smallint DEFAULT NULL, -- '工作包大小'
  status tinyint DEFAULT NULL, -- '工作包状态'
  daily_plan smallint DEFAULT NULL, -- '日计划工作量'
  due_date INT DEFAULT NULL, -- '预计完成时间'
  completed_num smallint DEFAULT NULL, -- '已完成数量'
  completed_at INT NOT NULL,  -- '完成时间'
  c_t datetime NOT NULL, -- '领取时间'
  u_t datetime NOT NULL, -- '修改时间'
  PRIMARY KEY(`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='任务包';


/* 积分兑换表 */
CREATE TABLE IF NOT EXISTS credits_redeem (
  id INT NOT NULL AUTO_INCREMENT,
  applied_by int DEFAULT NULL, -- '申请人的用户id'
  accepted_by int DEFAULT NULL, -- '受理人的用户id' 
  completed_by int DEFAULT NULL, -- '完成人的用户id'
  accepted_at INT DEFAULT NULL, -- '受理时间'
  completed_at INT DEFAULT NULL,  -- '完成时间'
  reward_name varchar(64) DEFAULT NULL, -- '奖品名称'
  cost_credits int DEFAULT NULL, -- '所用积分'  
  status tinyint DEFAULT NULL, -- '状态：申请中，已受理，已完成'
  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL, -- '申请时间'
  u_t datetime NOT NULL, -- '修改时间'
  PRIMARY KEY(`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='积分兑换表';

/* 日记 */
CREATE TABLE IF NOT EXISTS diaries (
  id INT  NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL, -- '用户id'
  
  tag tinyint DEFAULT NULL, -- '标签'
  work_types varchar(64) DEFAULT NULL, -- '工作类型'
  work_brief varchar(512) DEFAULT NULL, -- '工作摘要，如：【拆字x个，去重y页，录入z个。】'
  content text DEFAULT NULL, -- '打卡日记'
  c_t datetime NOT NULL, -- '创建时间'
  u_t datetime NOT NULL, -- '修改时间'
  PRIMARY KEY(`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci  COMMENT='日记';

/* 部件集 */
/* 部件来源：中华字库；GB13000.1规范；旧版龙泉字库（拆字网）；费锦昌；胡敬禹；龙泉字库 */
CREATE TABLE IF NOT EXISTS hanzi_parts (
  id INT  NOT NULL AUTO_INCREMENT,
  part_type tinyint DEFAULT NULL, -- '部件类型：文字、图片、文字且图片'
  part_char varchar(8) DEFAULT NULL, -- '文字'
  part_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  value varchar(32) DEFAULT NULL, -- '图片字IDS值'
  src tinyint DEFAULT NULL, -- '部件来源'
  src_chs_lib tinyint DEFAULT NULL, -- '中华字库'
  src_gb13000 tinyint DEFAULT NULL, -- 'GB13000.1规范'
  src_old_lqhanzi tinyint DEFAULT NULL, -- '旧版龙泉字库'
  src_feijinchang tinyint DEFAULT NULL, -- '费锦昌'
  src_hujingyu tinyint DEFAULT NULL, -- '胡敬禹'
  src_lqhanzi tinyint DEFAULT NULL, -- '龙泉字库'
  lqhanzi_sn tinyint DEFAULT NULL, -- '龙泉字库序号'
  is_redundant tinyint DEFAULT NULL, -- '是否多余'
  hard_level tinyint DEFAULT NULL, -- '难易等级'
  frequency int DEFAULT NULL, -- '部件频率'
  is_split_part tinyint DEFAULT NULL, -- '是否拆分部件'
  is_search_part tinyint DEFAULT NULL, -- '是否检索部件'
  replace_parts varchar(64) DEFAULT NULL, -- '代替部件'
  strokes tinyint DEFAULT NULL, -- '笔画数'
  stroke_order varchar(64) DEFAULT NULL, -- '笔顺'
  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t datetime NOT NULL, -- '创建时间'
  u_t datetime NOT NULL, -- '修改时间'
  PRIMARY KEY(`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='部件集';

--select * from hanzi_set as set where set.radical = hanzi_radicals.radical
alter table hanzi_set add index i_radical(radical);
alter table hanzi_radicals add index i_radical(radical);

--select * from hanzi_set where min_split = '';
alter table hanzi_set add index i_min_split(min_split(190));

--select input.*_final from variants_input as input into hanzi_set as set 
--where ( input.hanzi_char_final = set.hanzi_char or input.hanzi_pic_id_final = set.hanzi_pic_id) and set.source=汉字大字典
--select a.* from variants_input a, hanzi_set b                                             
--where ( a.hanzi_char_final = b.hanzi_char or a.hanzi_pic_id_final = b.hanzi_pic_id) and b.source='汉字大字典';

--select split.*_final from variants_split as split into hanzi_set as set 
--where ( split.hanzi_char = set.hanzi_char or split.hanzi_pic_id = set.hanzi_pic_id) and split.source = set.source and set.min_split = '';
--select a.* from variants_split a,hanzi_set b 
--where ( a.hanzi_char = b.hanzi_char or a.hanzi_pic_id = b.hanzi_pic_id) and a.source = b.source and b.min_split = '';
alter table hanzi_set add index i_hanzi_char_pic_id_source(hanzi_char,hanzi_pic_id,source);
alter table variants_input add index i_hanzi_char_pic_id_final(hanzi_char_final,hanzi_pic_id_final);
alter table variants_split add index i_hanzi_char_pic_id(hanzi_char,hanzi_pic_id);

--select * from hanzi_set as set where set.source=高丽
--and set.zheng_code = korean_dup_zheng_codes.zheng_code
--select * from hanzi_set a,korean_dup_zheng_codes b where a.source='高丽' 
--and a.zheng_code = b.zheng_code;
alter table hanzi_set add index i_source_zheng_code(source,zheng_code);
alter table korean_dup_zheng_codes add index i_zheng_code(zheng_code);

--其中 inter_dict_dedup.source = hanzi_set.source 
--and (inter_dict_dedup.hanzi_char = hanzi_set.hanzi_char 
--or inter_dict_dedup.hanzi_pic_id = hanzi_set.hanzi_pic_id)
alter table inter_dict_dedup add index i_hanzi_char_pic_id_source(hanzi_char,hanzi_pic_id,source);