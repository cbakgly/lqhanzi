Config MySQL
===========

On Debian/Ubuntu based distributions
---------------------------------------

1. Install MySQL Server and Python MySQL client
```bash
sudo apt-get install mysql-server # Set root password
sudo apt-get install python-mysqldb
```
2. Edit mysql-server bind-address config to `0.0.0.0`
```bash
bind-address		= 0.0.0.0
```

3. Connect to MySQL Server and create database
```mysql
mysql> create database lqhanzi;
Query OK, 1 row affected (0.01 sec)

mysql> grant all privileges on lqhanzi.* to lq@'%' identified by '123456';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```
CentOS based distributions
--------------------------
1. 
