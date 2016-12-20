# PEP8 Python编码规范
## 代码布局（Code lay-out）
### 缩进
* 每一级缩进使用4个空格
* 可以使用悬挂式缩进（hanging indent）。当采用悬挂式缩进方式时，应该符合下列条件：第一行不应该有参数，而且应该能够清楚无误地将后面采用缩进的行作为后续行从其他行中区分出来

**YES**:

```Python
# 使用分隔符来对齐
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

多行的代码结果结束时，结束符：
```Python
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

### 每行的最大长度
* 每一行的最大长度为119个字符。对于docstring或者注释，每行的长度应该限制为72个字符

```Python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

### 换行的位置
* 在二进制操作符的后面或者前面换行都可以。对于新写的代码在二进制操作符的前面进行换行       

```Python
# Yes: easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

### 空行
* 类和top-level函数定义之间空两行；
* 类中的方法定义之间空一行；
* 函数内逻辑无关段落之间空一行；
* **可以多使用一些空行（尽量少用这种方式）来将一些相关的方法进行分组。在一批相关的单行代码(比如一组dummy实现)之间的空行可以省略，在函数中有节制地使用空行来将代码分块，来表明它们是不同的逻辑代码块。**


### 源文件编码
### Imports
* 不要在一句import中多个库；   

```Python
  # Yes:
  import os
  import sys

  # No:  
  import sys, os
```

* Import语句每次都是放在文件的开头，它在模块的注释和docstring下面，以及模块的全局变量和常量的上面；
* import部分按标准、第三方和自己编写顺序依次排放，之间空一行。
* 在import语句后面可以放入任何相关的all声明；


### 模块级别dunder名字的位置
* dunders: 前后各带有两个下划线的名字如：\_\_all\_\_ , \_\_author\_\_ , \_\_version\_\_等；
* dunders放在模块docstring的下面，以及除了"from \_\_future\_\_ imports "以外的import语句的上面， "from \_\_future\_\_ imports" 语句必须放在除docstring的其他任何语句的上面；  

```Python
  """This is the example module.

  This module does stuff.
  """

  from __future__ import barry_as_FLUFL

  __all__ = ['a', 'b', 'c']
  __version__ = '0.1'
  __author__ = 'Cardinal Biggles'

  import os
  import sys
```

## 字符串引号
统一使用双引号

## 表达式和代码语句中的空格
### 在以下的情况中避免使用不必要的空格  
* 圆括号、方括号和花括号里；

```Python
# Yes:
spam(ham[1], {eggs: 2})
# No:  
spam( ham[ 1 ], { eggs: 2 } )
```
* 逗号，分号，冒号前；

```Python
  # Yes:
  if x == 4: print x, y; x, y = y, x

  # No:  
  if x == 4 : print x , y ; x , y = y , x
```

* 切片里的冒号两边不加空格，如果冒号有一边没有参数，那么那一边的空格就剩了；

```Python
  # Yes:
  ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
  ham[lower:upper], ham[lower:upper:], ham[lower::step]
  ham[lower+offset : upper+offset]
  ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
  ham[lower + offset : upper + offset]

  # No:
  ham[lower + offset:upper + offset]
  ham[1: 9], ham[1 :9], ham[1:9 :3]
  ham[lower : : upper]
  ham[ : upper]
```

* 函数调用时函数名与左边的括号之间不要有空格；

```Python
  # Yes:
  spam(1)

  # No:  
  spam (1)
```

* 切片或者引用时函数名与左边的括号之间不要有空格；

```Python
  # Yes:
  dct['key'] = lst[index]

  # No:  
  dct ['key'] = lst [index]
```

* 赋值时赋值符左右各有一个空格；

```Python
  # Yes:
  x = 1
  y = 2
  long_variable = 3

  # No:
  x             = 1
  y             = 2
  long_variable = 3
```

### 其他的建议
* 在行的结尾不要使用空格；
* 在二进制操作符的两边各使用一个空格：赋值( += , -= etc.), 对比 ( == , < , > , != , <> , <= , >= , in , not in , is , is not ), 布尔操作 ( and , or , not )；       

```Python
  # Yes:
  i = i + 1
  submitted += 1
  x = x*2 - 1
  hypot2 = x*x + y*y
  c = (a+b) * (a-b)

  # No:
  i=i+1
  submitted +=1
  x = x * 2 - 1
  hypot2 = x * x + y * y
  c = (a + b) * (a - b)
```

* 当用于表示关键字参数或默认参数值时，不要在=符号周围使用空格；

```Python
  # Yes:
  def complex(real, imag=0.0):
      return magic(r=real, i=imag)

  # No:
  def complex(real, imag = 0.0):
      return magic(r = real, i = imag)
```

* 函数注释时，冒号左边无空格，右边有一个空格。在->箭头（如果存在）周围始终各有一个空格；

```Python
  # Yes:
  def munge(input: AnyStr): ...
  def munge() -> AnyStr: ...

  # No:
  def munge(input:AnyStr): ...
  def munge()->PosInt: ...
```

* 当将参数注释与默认值组合时，请在=符号周围使用空格（但仅适用于同时具有注释和默认值的参数）；

```Python
  # Yes:
  def munge(sep: AnyStr = None): ...
  def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...

  # No:
  def munge(input: AnyStr=None): ...
  def munge(input: AnyStr, limit = 1000): ...
```

* 一行不能多个statements

```Python
  # Yes:
  if foo == 'blah':
      do_blah_thing()
  do_one()
  do_two()
  do_three()

  # No:
  if foo == 'blah': do_blah_thing()
  do_one(); do_two(); do_three()

  # No:
  if foo == 'blah': do_blah_thing()
  for x in lst: total += x
  while t < 10: t = delay()

  # Definitely not:
  if foo == 'blah': do_blah_thing()
  else: do_non_blah_thing()

  try: something()
  finally: cleanup()

  do_one(); do_two(); do_three(long, argument,
                               list, like, this)

  if foo == 'blah': one(); two(); three()
```

## 注释
* 所有函数的参数和返回值必须要写注释
* 注释可以用自己熟悉的语言（中文或英文），但务必保持整洁和清晰

### 块注释
* 在一段代码前增加的注释，在‘#’后加一空格
* 快注释里面的段落用#号间隔成多行

```Python
# The is a line seperated by the sign
# which I don't know how to say it in English
```

### 行注释
* 不用行内注释

### 文档描述（docstrings）
* 详情见[PEP 257](https://www.python.org/dev/peps/pep-0257/)；
* 为所有的公共模块、函数、类、方法写docstrings；对于非公共的方法docstrings不是必须的，但是必须写注释（在def的下一行）；

## 命名习惯
总体原则，新编代码必须按下面命名风格进行，现有库的编码尽量保持风格。尽量单独使用小写字母‘l’，大写字母‘O’等容易混淆的字母。

| 对象       | 命名习惯       | 示例            | 备注 |
|:---------:|:-------------:| :-------------:| :-------:|
| 包    | 尽量短小，全部小写，不使用下划线  | lqhanzi | |
| 模块  | 尽量短小，全部小写，可以使用下划线    | longquan_hanzi | |
| 类    | 首字母大写  | ClassName | |
| 异常  | 首字母大写，最后加上Error | ClassNotExistError | 如果异常不是错误就不需要加上Error |
| 函数  | 全部小写，可以使用下划线   | longquan_hanzi | |
| 类的属性（方法和变量）| 全部小写，可以使用下划线   | longquan_hanzi | non-public的方法和变量命名时加一个下划线作为前缀|
| 实例  | 全部小写，可以使用下划线   | longquan_hanzi |non-public的方法命名时加一个下划线作为前缀 |
| 全局变量 | 全部小写，可以使用下划线 | \_global\_var | |
| 常量  | 全部大写，可以使用下划线   | MAX_OVERFLOW | |

继承里的命名规则：
* 类的属性若与关键字名字冲突，属性名加一个下划线作为后缀。不使用缩略或者错误的拼写；
* 如果类打算被子类化，并且有不想要子类使用的属性，请考虑以两个下划线作为命名的开头，结尾不用下划线；

## 编码建议
* String concatenation的时候使用`''.join()`的方式，不建议使用`a += b` 或者`a = a + b`；
* 使用`is`、`is not`取代`==`，比如`if x is not None`要优于`if x；`
* 定义函数时，不要多用`lambda表达式`，尽量使用`def`；

```Python
# Yes
def f(x): return 2*x

# No
f = lambda x: 2*x
```

* 使用`raise ValueError('message')`，代替`raise ValueError, 'message'`；
* 使用except时尽量说明具体的exceptions的名称，比如`except ImportError`，在以下两种情况下可以只用except:
    * If the exception handler will be printing out or logging the traceback; at least the user will be aware that an error has occurred.
    * If the code needs to do some cleanup work, but then lets the exception propagate upwards with raise . try...finally can be a better way to handle this case.
* 建议exception如此写：

```Python
try:
    process_data()
except Exception as exc:
    raise DataProcessingFailedError(str(exc))
```

* 尽量少的使用try语句；  

```Python
# Yes:
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)

# No:
try:
    # Too broad!
    return handle_value(collection[key])
except KeyError:
    # Will also catch KeyError raised by handle_value()
    return key_not_found(key)
```

* 函数中的所有return语句要么都返回一个表达式（如何没有表达式可返回则写`return None`)，要么都不返回；

```Python
# Yes:
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

def bar(x):
    if x < 0:
        return None
    return math.sqrt(x)

# No:
def foo(x):
    if x >= 0:
        return math.sqrt(x)

def bar(x):
    if x < 0:
        return
    return math.sqrt(x)
```

* 使用`startswith()`和`endswith()`代替切片进行序列前缀或后缀的检查；

```Python
# Yes:
if foo.startswith(‘bar’):

# No:
if foo[:3] == ‘bar’:
```

* 使用`isinstance()`比较对象的类型；

```Python
# Yes：
if isinstance(obj, int):

# No:
if type(obj) is type(1):

# 可以这样测试一个object是不是一个string
if isinstance(obj, basestring):
```

* 判断一个序列（strings, lists, tuples）是否为空，可以这样：

```Python
# Yes:
if not seq:
if seq:

# No:
if len(seq)
if not len(seq)
```

* 不要使用`==`来对比布尔值为True或者False；

```Python
# Yes:   
if greeting:

# No:    
if greeting == True:

# Worse:
if greeting is True:
```
