
如何优雅的写一份`API`
=======================================

> 关于编写`api` 一直是个头疼的问题，关键字设计，`filter`设计，都很愁人，有时候会因为一个命名讨论半天。而且一个不好的设计逻辑会写很多无用的代码。那如何能写出一个漂亮的`API`呢，经过几次碰壁，终于找到一个个人认为是目前见过最好的模式。下面我们开始介绍如何使用


使用 `restful_framework`
----------------------------------------------------------

> `restful_framework` 是 `Django` 下使用推荐的一个框架，我们之所以使用框架就是为了不再重复别人已经走过的冤枉路。轮子已经造好，我们只需要会用就可以了。



先看瓜甜不甜
-------------------------
> 首先声明下，轮子不是我发明的，我只是个用轮子的

1. 点击下面的页面，我们先看看效果，查询所有用户
   http://127.0.0.1:8000/sysadmin/user/ 

2. 查询`id`为`1`的用户

   http://127.0.0.1:8000/sysadmin/user/1/

3. 按`username`查询

   http://127.0.0.1:8000/sysadmin/user/?username=xianer

4. 更复杂点的查询

   http://127.0.0.1:8000/sysadmin/user/?username=xianer&first_name=贤二

   > 老外的名字`first_name` 到底是姓还是名？
   > 更复杂的用法可以使用`startswith` `in` `exact` `range` 等参数

5. 删除一个用户

   http://127.0.0.1:8000/sysadmin/user/1/ 进去点击删除即可

6. 提交一个用户

   http://127.0.0.1:8000/sysadmin/user/ 下面填充好数据点击`POST`就👌了。

7. 更改一个用户

   http://127.0.0.1:8000/sysadmin/user/3/ 看到有个`PUT`么？改完点击下



看看代码怎么实现的
--------------------------------------
> 代码简单的都不好意思了，目前为了方便我都写到一个文件里了。回头可以分开的😄

1.先来看看`views` 怎么写

```python
# encoding: utf-8
from __future__ import unicode_literals
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework import viewsets
from rest_framework import serializers
import rest_framework_filters as filters
# 上面的这个filter真的挺好用的，它比官方的那个好用
# https://github.com/philipn/django-rest-framework-filters

# User management
# 下面是个序列化和反序列化的代码
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb', 'qq', 'address')

    def create(self, validated_data): # 这个和POST对应
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data): # 这个和PUT对应
        for key in ('username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb', 'qq'):
            setattr(instance, key, validated_data.get(key, getattr(instance, key)))
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserFilter(filters.FilterSet): # 过滤器就这么简单，复杂的，看其他代码
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb'}


class UserViewSet(viewsets.ModelViewSet): # 这个viewset多简单
    serializer_class = UserSerializer
    filter_class = UserFilter
    queryset = User.objects.all()
```
2.看看`URL` 怎么写

```python
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from sysadmin.views.api_sysadmin import OperationViewSet
from sysadmin.views.api_sysadmin import UserViewSet

router = DefaultRouter()
router.register(r'^operation', OperationViewSet)
router.register(r'^user', UserViewSet) # 只需要这么简单，增删改查全搞定
urlpatterns = router.urls
```

顺便看看 `DEBUG TOOLBAR`😁
> 这个东西也很好用，真的

https://django-debug-toolbar.readthedocs.io/en/stable/installation.html 详细的文档

配置里写好了，您要做的仅仅是下面

```bash
pip install -r requirements.txt
### 或者直接安装包 ###
pip install django-debug-toolbar
```


API 测试
-----------------
下面可以带大家看看`testcase` 怎么写，`sysadmin/tests.py` 就是例子

```bash
./manager.py test # 就可以执行测试了
./manager.py test sysadmin.tests # 只测试一个
```


Thanks everybody!
----------------------------------------