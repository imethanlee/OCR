from sql import *
from ps import *
from tkinter import *

# 实用工具函数在此定义
myfont = "宋体 12"


def ps(entry: Entry):
    myps = PS(entry.get()[1:-1])
    myps.run()


