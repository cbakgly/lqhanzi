-- SET foreign_key_checks = 0; 

rename table lq_tasks to lq_tasks_bk;

-- import data

insert into lq_tasks_bk(id, task_status, business_id, business_type, business_stage, credits, remark, assigned_at, completed_at, c_t, u_t, task_package_id, user_id) select id, task_status, business_id, business_type, business_stage, credits, remark, assigned_at, completed_at, c_t, u_t, task_package_id, user_id from lq_tasks;

create temporary table tmp (business_type smallint(11), content_id smallint(11));
truncate table tmp;
insert into tmp (business_type,content_id) select 1,id from django_content_type where app_label="backend" and model="variantssplit";
insert into tmp (business_type,content_id) select 2,id from django_content_type where app_label="backend" and model="variantsinput";
insert into tmp (business_type,content_id) select 8,id from django_content_type where app_label="backend" and model="interdictdedup";
insert into tmp (business_type,content_id) select 6,id from django_content_type where app_label="backend" and model="inputpage";
insert into tmp (business_type,content_id) select 5,id from django_content_type where app_label="backend" and model="koreandupcharacters";

UPDATE lq_tasks
SET
    content_type_id = (SELECT
            tmp.content_id
        FROM
            tmp
        WHERE
            tmp.business_type = lq_tasks.business_type);
            
            
update lq_tasks set object_id=`business_id`;
truncate table lq_input_page;
insert into lq_input_page (page_num) select distinct(page_num) from lq_variants_input;
create temporary table tmp_page_num (user_id smallint(11), task_package_id smallint(11), page_num smallint(11), completed_at datetime, c_t datetime, u_t datetime, content_type_id smallint(11));
truncate table tmp_page_num;
insert into tmp_page_num(user_id,task_package_id,page_num,completed_at,c_t,u_t, content_type_id) select tp.user_id,tp.id,vi.page_num,tp.completed_at,tp.c_t,tp.u_t,1 from lq_task_packages as tp, lq_tasks as ts, lq_variants_input as vi where
ts.object_id = vi.id and ts.task_package_id = tp.id group by page_num order by page_num;
UPDATE tmp_page_num
SET
    content_type_id = (SELECT
            tmp.content_id
        FROM
            tmp
        WHERE
            tmp.business_type = 6);
INSERT INTO `lqhanzi`.`lq_tasks`
(`user_id`,`task_package_id`,`object_id`,`assigned_at`,`completed_at`,`c_t`,`u_t`,`content_type_id`,`business_type`,`business_stage`,`task_status`,`credits`,`remark`)
select user_id, task_package_id, page_num, completed_at, completed_at, c_t, u_t, content_type_id, 6, 3, 3, 0, "" from tmp_page_num;

