Lqhanzi project
===============

> Django 1.10.4

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
