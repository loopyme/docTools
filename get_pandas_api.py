# python3
# -*- coding: utf-8 -*-
# @File    : get_pandas_api.py
# @Desc    : Link to Pandas_doc in modin_doc
# @Project : docTools
# @Time    : 8/5/19 10:16 AM
# @Author  : Loopy
# @Contact : peter@mail.loopy.tech
# @License : CC BY-NC-SA 4.0 (subject to project license)

import re
import requests


def get_panda_apis():
    pattern = '<td><a class="reference internal" href="(.+?)" title="(.+?)"><code class="xref py py-obj docutils literal notranslate">'
    apis = {}

    r = requests.get(
        "https://pandas.pydata.org/pandas-docs/stable/reference/frame.html"
    )
    api_contents = re.findall(pattern, r.content.decode("utf-8"))
    for i in api_contents:
        apis[i[1]] = "https://pandas.pydata.org/pandas-docs/stable/reference/" + i[0]

    r = requests.get(
        "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html"
    )
    api_contents = re.findall(pattern, r.content.decode("utf-8"))[0]
    for i in api_contents:
        apis[i[1]] = "https://pandas.pydata.org/pandas-docs/stable/reference/" + i[0]

    return apis


def get_modin_apis():
    global modin_apis
    modin_apis = ""
    pattern = "\| ``(.+?)``"
    with open(
        "/home/x/Documents/git/modin/docs/UsingPandasonRay/dataframe_supported.rst",
        "r+",
    ) as f:
        text = f.read()
        f.seek(0)
        f.truncate()
        f.write(re.sub(pattern, add_url, text) + modin_apis)


def add_url(matched):
    global pandas_apis, modin_apis
    modin_api = matched.group()[4:-2]
    if "pandas.DataFrame." + modin_api in pandas_apis.keys():
        modin_apis += ".. _`{}`: {}\n".format(
            modin_api, pandas_apis["pandas.DataFrame." + modin_api]
        )
        return "| `{}`_ ".format(modin_api)
    else:
        return matched.group()


if __name__ == "__main__":
    pandas_apis = get_panda_apis()
    get_modin_apis()
    print("DONE")
