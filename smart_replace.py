# python3
# -*- coding: utf-8 -*-
# @File    : smart_replace.py
# @Desc    : 
# @Software: PyCharm
# @Time    : 19-6-1 下午3:12
# @Author  : Loopy
# @Doc     : http://api.loopy.tech/api/文档.html
# @Contact : 57658689098a@gmail.com 

import re
import os


def remove_mark(matched):
    global md_file, flag
    flag = False
    removed_letter = re.sub(r'```\n|```py\n|```|py', "", matched.group())
    removed_letter = re.sub(r'\n+', "\n", removed_letter)
    with open("./docs/log.txt", 'a') as log:
        log.write('=' * 36 + md_file + removed_letter)
    return removed_letter


if __name__ == '__main__':
    for md_file in os.listdir('./docs'):
        if md_file.split('.')[-1] == 'md':
            with open('./docs/'+md_file, 'r+') as f:
                flag = True
                ori_md = f.read()
                fix_md = re.sub('```py\n+!(.|\n)+?```', remove_mark, ori_md)
                if not flag:
                    f.seek(0)
                    f.truncate()
                    f.write(fix_md)
                    print('DONE at', md_file)
                else:
                    print('No jod to do at', md_file)
