Django Guardian
================

> 对数据模型的基本权限，可以在定义数据模型的时候加上，可以参考下面网址学习，文档内容简单易懂:
> [django-guardian readthedocs](http://django-guardian.readthedocs.io/en/stable/)

```text
add__
delete__
view__
modify__
```

1. `hanzi_set`

```text
add__hanzi_set
delete__hanzi_set
view__hanzi_set
modify__hanzi_set
```

*The rest models can make like examples above*

2. `variants_split`

3. `variants_input`

4. `korean_variants_dict`

5. `hanzi_radicals`

6. `korean_dup_zheng_codes`

7. `korean_dedup`

8. `korean_dup_characters`

9. `inter_dict_dedup`

10. `tasks`

11. `task_packages`

12. `credits_redeem`

13. `diaries`


# 使用说明

> 参考项目README.md中的说明，做完初始化后，
> 基本权限就配置完了。
> 
> 权限信息请参考 workbench.models.RbacAction
> 
> 默认管理员参考 scripts.init_rbac
> 
> 使用方式如下：

```
from workbench.models import RbacAction
action = RbacAction.objects.get(code="op")

# 查找某个用户的记录, 这里user是sys_admin
from sysadmin.models import User
user = User.objects.get(id=5) 

user.has_perm('op_task', action)
> False

user.has_perm('op_system', action)
> True
```