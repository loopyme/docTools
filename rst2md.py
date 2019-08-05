# python3
# -*- coding: utf-8 -*-
# @File    : rst2md.py
# @Desc    : rst & md converter
# @Project : docTools
# @Time    : 19-6-3 上午10:42
# @Author  : Loopy
# @Contact : peter@mail.loopy.tech
# @License : CC BY-NC-SA 4.0 (subject to project license)

import requests


def help_md_rst(from_file, to_file, data):
    """ rst & md 转化辅助函数 """
    response = requests.post(
        url="http://c.docverter.com/convert",
        data=data,
        files={"input_files[]": open(from_file, "rb")},
    )

    if response.ok:
        if to_file is None:

            # auto backup
            to_file = from_file
            with open(to_file, "w") as f:
                with open("bak_" + to_file, "w") as f_bac:
                    f_bac.write(f.read())
        else:
            with open(to_file, "w") as f:
                f.write(response.content)
    else:
        print("response is not ok")


def md_to_rst(from_file, to_file=None):
    data = {"to": "rst", "from": "markdown"}
    help_md_rst(from_file, to_file, data)


def rst_to_md(from_file, to_file=None):
    data = {"to": "markdown", "from": "rst"}
    help_md_rst(from_file, to_file, data)


if __name__ == "__main__":
    md_to_rst("README.md", "README.rst")
