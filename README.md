Lqhanzi project
===============

环境安装要求
-------------
> 需要安装以下软件，建议使用`pip`进行安装，`Django`以及下面的所有`app`都有详细的开发文档，请查看官网．

* [Django](https://www.djangoproject.com/)
* [django-guardian](http://django-guardian.readthedocs.io/en/stable/)
* [restframework](http://www.django-rest-framework.org)
* [djangorestframework-jwt](https://github.com/GetBlimp/django-rest-framework-jwt)

```bash
> pip install django==1.10.4
> pip install django-guardian
> pip install djangorestframework
> pip install markdown       # Markdown support for the browsable API.
> pip install django-filter  # Filtering support
> pip install djangorestframework-jwt
> ... # 其他软件包，建议用下面的命令安装
```
*可以直接使用下面的命令安装*

```bash
# 安装Python虚拟环境
>pip install virtualenv
>pip install virtualenvwrapper

# 下载代码
>git clone http://gitlab.lqdzj.cn/lqdzj/lqhanzi.git

# 基于同目录，建立项目环境
>virtualenv lqhanzi
>cd lqhanzi

# 进入项目环境，安装依赖包
>. bin/activate
(lqhanzi)>pip install -r requirements.txt

# 退出环境
(lqhanzi)> deactivate

# 启动mysql
> mysql.server start

# 创建数据库lqhanzi
> mysqladmin create lqhanzi -u root -p

# 创建表
> . bin/activate
(lqhanzi)> cd lqhanzi/project
(lqhanzi)> ./manage.py makemigration
(lqhanzi)> ./manage.py migrate
(lqhanzi)> ./manage.py test

# 初始化数据
(lqhanzi)> ./manage.py runscript init_db
(lqhanzi)> ./manage.py runscript init_rbac

# 启动服务器
(lqhanzi)> ./manage.py runserver
```

pubdocs 
-------
> 请把一些说明性的文档，如PEP8等，或者其他介绍的文档放在此路径，建议用`Markdown`写文档
> 如果内容含有中文，请务必使用`UTF8`编码。


mysite
------
> 项目的代码路径

此项目的目前代码树
------------------------

```text
mysite/ # 项目代码路径
├── db.sqlite3 # 先可以使用sqlite数据库
├── hanzilib # 字库
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
├── mysite
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
