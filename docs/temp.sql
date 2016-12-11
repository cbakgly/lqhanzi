Temp SQL Defination
===================

1. User model Table Create SQL
```sql
CREATE TABLE `auth_user` (
--- default fields
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,

--- added fields

  `gender` varchar(2), -- F for Female M for Male
  `qq` varchar(32),
  `mb` varchar(32), -- Mobile phone
  `address` varchar(128), -- Address/or Location

  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

操作日志
--------

id default
1. user_id  foreign key
2. logtype == number
2. logtime
3. message


