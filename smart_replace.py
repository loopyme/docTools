# python3
# -*- coding: utf-8 -*-
# @File    : smart_replace.py
# @Desc    : 寻找目标(match_pattern)字符串,对其进行调整
# @Software: PyCharm
# @Time    : 19-6-1 下午3:12
# @Author  : Loopy
# @Contact : 57658689098a@gmail.com 

import re
import os

match_pattern = '```py\n+!(.|\n)+?```'
replace_from = '```\n|```py\n|```|py'
replace_to = ''

def remove_mark(matched):
    global md_file, flag
    flag = False
    
    # Operations on match string
    removed_letter = re.sub(replace_from, replace_to, matched.group())
    removed_letter = re.sub(r'\n+', "\n", removed_letter)
    
    # For possible manual reverification
    with open("./docs/log.txt", 'a') as log:
        log.write('=' * 36 + md_file + removed_letter)
    return removed_letter


if __name__ == '__main__':
    for md_file in os.listdir('./docs'):
        if md_file.split('.')[-1] == 'md':
            with open('./docs/'+md_file, 'r+') as f:
                flag = True # if no change required
                ori_md = f.read()
                fix_md = re.sub(match_pattern, remove_mark, ori_md)
                if not flag:
                    f.seek(0)
                    f.truncate()
                    f.write(fix_md)
                    print('DONE at', md_file)
                else:
                    print('No jod to do at', md_file)
