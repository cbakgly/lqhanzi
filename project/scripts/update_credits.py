from django.db import connection

sql = '''
set foreign_key_checks=0;
truncate table lq_credits;
INSERT INTO `lqhanzi`.`lq_credits` (`credit`, `sort`, `user_id`, `u_t`) select sum(credits),business_type,user_id, now() from lq_tasks where task_status=3 group by business_type, user_id;
INSERT INTO `lqhanzi`.`lq_credits` (`credit`, `sort`, `user_id`, `u_t`) select sum(credit),0,user_id, now() from lq_credits group by user_id;
set foreign_key_checks=1;
'''


def run():
    cursor = connection.cursor()
    cursor.execute(sql)
