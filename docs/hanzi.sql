
/* 龙泉字库表 */
CREATE TABLE IF NOT EXISTS hanzi_set (
  id INT(11) PRIMARY KEY,

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
  is_redundant tinyint DEFAULT NULL, -- '是否多余'
  dup_count tinyint DEFAULT NULL, -- '重复次数'
  inter_dict_dup_hanzi varchar(64) DEFAULT NULL, -- '异体字字典间重复编码'
  korean_dup_hanzi varchar(32) DEFAULT NULL, -- '高丽异体字字典内部重复编码'

  -- 拆字信息
  structure varchar(16) DEFAULT NULL, -- '结构'
  skip_num tinyint DEFAULT NULL, -- ‘跳过次数，多的话算难字'
  min_split varchar(256) DEFAULT NULL, -- '初步拆分'
  max_split varchar(512) DEFAULT NULL, -- '最大拆分'
  mix_split varchar(512) DEFAULT NULL, -- '混合拆分'
  deform_split varchar(256) DEFAULT NULL, -- '调笔拆分'
  similar_parts varchar(128) DEFAULT NULL, -- '相似部件'
  stroke_serial varchar(128) DEFAULT NULL, -- '部件序列'

  remark varchar(128) DEFAULT NULL, -- '备注'
  c_t INT NOT NULL,
  u_t INT NOT NULL 
);


/* 异体字拆字业务表 */
CREATE TABLE IF NOT EXISTS variants_split (
  id INT(11) PRIMARY KEY,

  -- 字典信息
  source tinyint DEFAULT NULL, -- '来源'
  hanzi_type tinyint DEFAULT NULL, -- '字形类型：文字、图片、文字且图片'
  hanzi_char varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi varchar(64) DEFAULT NULL, -- '所属正字'
  as_std_hanzi varchar(32) DEFAULT NULL, -- '兼正字号'
  tw_seq_id varchar(32) DEFAULT NULL, -- '位置编号'

  -- 重复信息
  is_redundant tinyint DEFAULT NULL, -- '是否多余'

  -- 初次
  skip_num_draft tinyint DEFAULT NULL, -- '是否难字'
  init_split_draft varchar(128) DEFAULT NULL, -- '初步拆分'
  other_init_split_draft varchar(128) DEFAULT NULL, -- '其它初步拆分'
  deform_split_draft varchar(128) DEFAULT NULL, -- '调笔拆分'
  similar_parts_draft varchar(64) DEFAULT NULL, -- '相似部件'
  dup_id_draft varchar(32) DEFAULT NULL, -- '重复ID'

  -- 回查
  skip_num_review tinyint DEFAULT NULL, -- '是否难字'
  init_split_review varchar(128) DEFAULT NULL, -- '初步拆分'
  other_init_split_review varchar(128) DEFAULT NULL, -- '其它初步拆分'
  deform_split_review varchar(128) DEFAULT NULL, -- '调笔拆分'
  similar_parts_review varchar(64) DEFAULT NULL, -- '相似部件'
  dup_id_review varchar(32) DEFAULT NULL, -- '重复ID'

  -- 审查
  skip_num_final tinyint DEFAULT NULL, -- '是否难字'
  init_split_final varchar(128) DEFAULT NULL, -- '初步拆分'
  other_init_split_final varchar(128) DEFAULT NULL, -- '其它初步拆分'
  deform_split_final varchar(128) DEFAULT NULL, -- '调笔拆分'
  similar_parts_final varchar(64) DEFAULT NULL, -- '相似部件'
  dup_id_final varchar(32) DEFAULT NULL, -- '重复ID'

  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t INT NOT NULL,
  u_t INT NOT NULL 
);

/* 异体字录入业务表 */
CREATE TABLE IF NOT EXISTS variants_input (
  id INT(11) PRIMARY KEY,

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

  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t INT NOT NULL,
  u_t INT NOT NULL 
);

/* 高丽异体字字典 */
CREATE TABLE IF NOT EXISTS korean_variants_dict (
  id INT(11) PRIMARY KEY,
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
  emean varchar(128) DEFAULT NULL -- '英文含义'
);

/* 汉字部首表 */
CREATE TABLE IF NOT EXISTS hanzi_radicals (
  id INT PRIMARY KEY,
  radical varchar(16) DEFAULT NULL, -- '部首'
  strokes tinyint DEFAULT NULL  -- '笔画数'
);

/* 高丽异体字内部去重-待去重郑码表 */
CREATE TABLE IF NOT EXISTS korean_dup_zheng_codes (
  id INT(11) PRIMARY KEY,
  zheng_code VARCHAR(32) NOT NULL,  -- '郑码'
  count tinyint NOT NULL, -- '郑码对应汉字的数量'
  page_num smallint DEFAULT NULL -- '页码'
);

/* 高丽异体字去重-去重结果表 */
CREATE TABLE IF NOT EXISTS korean_dedup (

  id INT(11) PRIMARY KEY,

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
  c_t INT NOT NULL,
  u_t INT NOT NULL
);


/* 高丽台湾异体字去重-高丽字头表 */
CREATE TABLE IF NOT EXISTS korean_dup_characters (
  id INT PRIMARY KEY,
  korean_variant VARCHAR(32) NOT NULL,  -- '高丽字头'
  unicode VARCHAR(32) NOT NULL,  -- '与字头字形相同/相近的Unicode'
  relation SMALLINT DEFAULT NULL,  -- '二者关系：形码均相同，形似码相同，形同码不同，无相同字形'
  remark VARCHAR(128) DEFAULT NULL, -- '备注'
  c_t INT NOT NULL,
  u_t INT NOT NULL
);


/* 高丽台湾异体字去重结果表 */
CREATE TABLE IF NOT EXISTS inter_dict_dedup (
  id INT(11) PRIMARY KEY,

  -- 字典信息
  source tinyint DEFAULT NULL, -- '来源'
  hanzi_type tinyint DEFAULT NULL, -- '字形类型：文字、图片、文字且图片'
  hanzi_char varchar(8) DEFAULT NULL, -- '文字'
  hanzi_pic_id varchar(32) DEFAULT NULL, -- '图片字编码'
  variant_type tinyint DEFAULT NULL, -- '正异类型'
  std_hanzi varchar(64) DEFAULT NULL, -- '所属正字'
  as_std_hanzi varchar(32) DEFAULT NULL, -- '兼正字号'

  -- 重复信息
  inter_dict_dup_hanzi varchar(64) DEFAULT NULL, -- '异体字字典间重复编码'

  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t INT NOT NULL,
  u_t INT NOT NULL 
);

/* 任务池 */
CREATE TABLE IF NOT EXISTS tasks (
  id INT PRIMARY KEY,
  user_id INT DEFAULT NULL, -- '拆字员'
  business_id INT(11) NOT NULL, -- '业务ID，指的是对应于拆字、去重、录入业务表的ID'
  task_package_id INT(11) DEFAULT NULL, -- ‘任务包ID’
  business_type tinyint DEFAULT NULL, -- '任务类型'
  business_stage tinyint DEFAULT NULL, -- '任务阶段'
  task_status tinyint DEFAULT NULL, -- '任务状态'
  credits SMALLINT DEFAULT NULL, -- '积分'
  remark VARCHAR(128) DEFAULT NULL, -- '备注'
  assigned_at INT NOT NULL, -- '分配时间'
  completed_at INT NOT NULL,  -- '完成时间' 
  c_t INT NOT NULL, -- '创建时间'
  u_t INT NOT NULL -- '修改时间'
);

/* 任务包 */
CREATE TABLE IF NOT EXISTS task_packages (
  id INT(11) PRIMARY KEY,
  user_id int NOT NULL, -- '用户id'
  business_type tinyint DEFAULT NULL, -- '任务类型'
  business_stage tinyint DEFAULT NULL, -- '任务阶段'
  size smallint DEFAULT NULL, -- '工作包大小'
  status tinyint DEFAULT NULL, -- '工作包状态'
  daily_plan smallint DEFAULT NULL, -- '日计划工作量'
  due_date INT DEFAULT NULL, -- '预计完成时间'
  completed_num smallint DEFAULT NULL, -- '已完成数量'
  completed_at INT NOT NULL,  -- '完成时间'
  c_t INT NOT NULL, -- '领取时间'
  u_t INT NOT NULL -- '修改时间'
);

/* 积分兑换表 */
CREATE TABLE IF NOT EXISTS credits_redeem (
  id INT PRIMARY KEY,
  applied_by int DEFAULT NULL, -- '申请人的用户id'
  accepted_by int DEFAULT NULL, -- '受理人的用户id' 
  completed_by int DEFAULT NULL, -- '完成人的用户id'
  accepted_at INT DEFAULT NULL, -- '受理时间'
  completed_at INT DEFAULT NULL,  -- '完成时间'
  reward_name varchar(64) DEFAULT NULL, -- '奖品名称'
  cost_credits int DEFAULT NULL, -- '所用积分'  
  status tinyint DEFAULT NULL, -- '状态：申请中，已受理，已完成'
  remark varchar(64) DEFAULT NULL, -- '备注'
  c_t INT NOT NULL, -- '申请时间'
  u_t INT NOT NULL -- '修改时间'
);

/* 日记 */
CREATE TABLE IF NOT EXISTS diaries (
  id INT PRIMARY KEY,
  user_id int NOT NULL, -- '用户id’，
  tag tinyint DEFAULT NULL, — ‘标签’,
  work_types varchar(64) DEFAULT NULL, -- '工作类型'
  work_brief varchar(512) DEFAULT NULL, -- '工作摘要，如：【拆字x个，去重y页，录入z个。】'
  content text DEFAULT NULL, -- '打卡日记'
  c_t INT NOT NULL, -- '创建时间'
  u_t INT NOT NULL -- '修改时间'
);