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

PossibleUrls = [
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html",
    "https://pandas.pydata.org/pandas-docs/stable/reference/frame.html",
    "https://pandas.pydata.org/pandas-docs/stable/reference/io.html",
    "https://pandas.pydata.org/pandas-docs/stable/reference/general_functions.html",

]

Pattern = '<td><a class="reference internal" href="(.+?)" title="(.+?)"><code class="xref py py-obj docutils literal notranslate">'

ModinPath = "/home/x/Documents/git/modin/docs/UsingPandasonRay/io_supported.rst"

ProcessedFunction = "pandas"


def get_panda_apis():
    global PossibleUrls, Pattern
    apis = {}

    for url in PossibleUrls:
        r = requests.get(url)
        print("get " + url)
        api_contents = re.findall(Pattern, r.content.decode("utf-8"))
        for i in api_contents:
            if i[0][0:4] == "api/":
                apis[i[1]] = (
                        "https://pandas.pydata.org/pandas-docs/stable/reference/" + i[0]
                )
            else:
                apis[i[1]] = (
                        "https://pandas.pydata.org/pandas-docs/stable/reference/api/" + i[0]
                )

            # check if link is valid
            # r = requests.get(apis[i[1]])
            # if r.status_code != 200:
            #    print(
            #        "WARNING: Link {} is in status {}".format(apis[i[1]], r.status_code)
            #    )
    return apis


def get_modin_apis():
    global modin_apis, ModinPath
    modin_apis = ""
    pattern = "\| ``(.+?)``"
    with open(ModinPath, "r+") as f:
        text = f.read()
        f.seek(0)
        f.truncate()
        f.write(re.sub(pattern, add_url, text) + modin_apis)

    # auto backup
    with open(ModinPath + "bak", "w") as f:
        f.write(text)


def add_url(matched):
    global pandas_apis, modin_apis, ProcessedFunction
    modin_api = matched.group()[4:-2]
    if ProcessedFunction + "." + modin_api in pandas_apis.keys():
        modin_apis += ".. _`{}`: {}\n".format(
            modin_api, pandas_apis[ProcessedFunction + "." + modin_api]
        )
        return "| `{}`_ ".format(modin_api)
    else:
        print("WARNING: {}.{} is not found".format(ProcessedFunction, modin_api))
        return matched.group()


if __name__ == "__main__":
    pandas_apis = get_panda_apis()
    get_modin_apis()
    print("DONE")
