Lqhanzi project
===============

环境搭建与安装说明
-------------
> 需要安装以下软件，建议使用`pip`进行安装，`Django`以及下面的所有`app`都有详细的开发文档，请查看官网．

```bash
# 启动mysql
> mysql.server start

# 创建数据库lqhanzi
> mysqladmin create lqhanzi -u root -p

# 为lqhanzi 创建用户lq，密码123456
> mysql -u root -p
> CREATE USER lq@'localhost' IDENTIFIED BY '123456';
> GRANT ALL PRIVILEGES ON lqhanzi.* TO lq;

# 下载代码
>git clone http://gitlab.lqdzj.cn/lqdzj/lqhanzi.git
OR
>git clone ssh://git@gitlab.lqdzj.cn:9022/lqdzj/lqhanzi.git

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
##同步主库信息
`
    git remote -v
`

origin	ssh://git@gitlab.lqdzj.cn:9022/yuwangjun/lqhanzi.git (fetch)
origin	ssh://git@gitlab.lqdzj.cn:9022/yuwangjun/lqhanzi.git (push)

如没有upstream，执行下面命令

git remote add upstream ssh://git@gitlab.lqdzj.cn:9022/lqdzj/lqhanzi.git