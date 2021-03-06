Lqhanzi project
===============

环境搭建与安装说明
-------------
> 需要安装以下软件，建议使用`pip`进行安装，`Django`以及下面的所有`app`都有详细的开发文档，请查看官网．

```bash
# OSX环境
> /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# 安装mysql
> brew install mysql

# my.cnf
default-storage-engine=INNODB
innodb_large_prefix=on

# 启动mysql
> mysql.server start

# 安装redis
> brew install redis

# 启动redis
> redis-server &
# OSX环境结束


# 创建数据库lqhanzi
> mysql -uroot -p
> CREATE DATABASE lqhanzi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;

# 为lqhanzi 创建用户lq，密码123456
> CREATE USER lq@'localhost' IDENTIFIED BY '123456';
> GRANT ALL PRIVILEGES ON lqhanzi.* TO lq;
> FLUSH PRIVILEGES;

# import data
> curl -LO https://s3.cn-north-1.amazonaws.com.cn/lqhanzi-misc/data/lqhanzi-sql.2017.03.14.tar.bz
# 导入略

# 下载代码
>git clone http://gitlab.lqdzj.cn/lqdzj/lqhanzi.git
OR
>git clone ssh://git@gitlab.lqdzj.cn:9022/lqdzj/lqhanzi.git

# 在gitlab.lqdzj.cn上fork代码到自己的库中，假设名字为abc，以下abc要替换成自己的username
# push, pull 参考https://segmentfault.com/a/1190000002783245
> cd lqhanzi
> git remote add mylib http://gitlab.lqdzj.cn/abc/lqhanzi.git

# 安装Python虚拟环境
>pip install virtualenv
>pip install virtualenvwrapper

# 基于同目录，建立项目环境
>virtualenv lqhanzi
>cd lqhanzi

# 进入项目环境，安装依赖包
>. bin/activate
(lqhanzi)>pip install -r requirements.txt

# 创建表 (凡是数据表更新过，都需要跑一下以下的migration命令)
> . bin/activate
(lqhanzi)> cd lqhanzi/project
(lqhanzi)> ./manage.py makemigrations
(lqhanzi)> ./manage.py migrate

# 初始化数据
(lqhanzi)> ./manage.py runscript init_db
(lqhanzi)> ./manage.py runscript init_rbac

# 启动服务器
(lqhanzi)> ./manage.py runserver

# 退出环境
(lqhanzi)> deactivate

```

每次启动电脑后，运行的步骤
--------

```
# 1 启动mysql
# 2 启动redis-server
# 3 进入python的虚拟环境：source ./bin/activate
# 4 ./manage.py runserver
```

遇到models变化后，runserver时给出各种错误信息，解决不了的步骤
--------

```
# 1 保存数据库数据
# 2 > mysql -uroot -p
# 3 > drop databases lqhanzi;
# 4 重复上面的创建过程
# 5 > ./manage.py makemigrations  
# 6 > ./manage.py migrate
# 7 > ./manage.py runserver

第5步对于django来说，每次models有变化都有运行以便环境有记录。
第6步是django把变化更新到mysql中。
一般这两步连在一起做。
```

相关文档
-------
> 请把一些说明性的文档，如PEP8等，或者其他介绍的文档放在docs下，建议用`Markdown`写文档
> 如果内容含有中文，请务必使用`UTF8`编码。

* [Django](https://www.djangoproject.com/)
* [django-guardian](http://django-guardian.readthedocs.io/en/stable/)
* [restframework](http://www.django-rest-framework.org)
* [djangorestframework-jwt](https://github.com/GetBlimp/django-rest-framework-jwt)
* [debug toolbar](https://django-debug-toolbar.readthedocs.io/en/stable/installation.html)

项目代码树
------------------------

```text
lqhanzi/ # 项目代码路径
├── db.sqlite3 # 先可以使用sqlite数据库
├── hanzi # 字库
│   ├── admin.py
│   ├── apps.py
│   ├── docs # 文档路径
│   │   └── api.hanzilib.README.md # API 文档
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── sysadmin # 运营管理后台
│   ├── admin.py
│   ├── apps.py
│   ├── docs # 文档路径
│   │   └── api.admin.README.md # API 文档
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── lqconfig
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── workbench # 用户工作台
    ├── admin.py
    ├── apps.py
    ├── docs # 用户工作台API文档
    │   └── api.workbench.README.md # API 文档
    ├── __init__.py
    ├── migrations
    │   ├── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```
