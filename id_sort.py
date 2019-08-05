# python3
# -*- coding: utf-8 -*-
# @File    : id_sort.py.py
# @Desc    : Alphabetize the list of contributors
# @Project : docTools
# @Time    : 7/24/19 4:51 PM
# @Author  : Loopy
# @Contact : peter@mail.loopy.tech
# @License : CC BY-NC-SA 4.0 (subject to project license)

import re
import os

if __name__ == "__main__":
    with open("./contributors.md", "r+") as f:
        ori_md = f.read()
    ids = re.findall("(- \[.+?\]\(.+?\)|- \[.+?\]\(\))", ori_md)
    id_url = {}
    for i in ids:
        i_name, i_url = i.split("](")
        i_name = i_name[3:]
        i_url = i_url[:-1]

        if i_name in id_url.keys():
            print("WARNING: {} appears more than once".format(i_name))
        id_url[i_name] = i_url

    sorted_md = ""
    for i in sorted(id_url):
        sorted_md += "- [{}]({})\n".format(i, id_url[i])
    with open("./contributors.md", "w") as f:
        f.write(sorted_md)
    print("DONE,number of contributors: " + str(len(id_url)))
