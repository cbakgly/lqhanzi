'''
作者：Rui L
链接：https://www.zhihu.com/question/21572891/answer/26046582
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

使用时直接引用此文件
'''
from __future__ import unicode_literals
import sys


class ExceptionHook:
    instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            from IPython.core import ultratb
            self.instance = ultratb.FormattedTB(mode='Plain',
                 color_scheme='Linux', call_pdb=1)
        return self.instance(*args, **kwargs)

sys.excepthook = ExceptionHook()