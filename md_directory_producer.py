# python3
# -*- coding: utf-8 -*-
# @File    : md_directory_producer.py
# @Desc    : Directory producer for markdown
# @Project : docTools
# @Time    : 19-6-14 下午7:25
# @Author  : Loopy
# @Contact : peter@mail.loopy.tech
# @License : CC BY-NC-SA 4.0 (subject to project license)

import re
import os


class DirectoryProducer:

    manual_check = True
    default_max_title_level = 3
    default_root_path = "./"
    default_result_path = "./"

    @classmethod
    def config(
        cls,
        default_max_title_level=None,
        manual_check=None,
        default_result_path=None,
        default_root_path=None,
    ):
        cls.default_max_title_level = (
            default_max_title_level
            if default_max_title_level is not None
            else cls.default_max_title_level
        )
        cls.manual_check = (
            manual_check if manual_check is not None else cls.manual_check
        )
        cls.default_root_path = (
            default_root_path
            if default_root_path is not None
            else cls.default_root_path
        )
        cls.default_result_path = (
            default_result_path
            if default_result_path is not None
            else cls.default_result_path
        )

    def __init__(
        self,
        result_filename,
        is_target_file,
        max_title_level=None,
        result_title=None,
        root_path=None,
        result_path=None,
        is_sorted = False,
    ):
        self.max_title_level = (
            max_title_level
            if max_title_level is not None
            else self.default_max_title_level
        )
        self.root_path = root_path if root_path is not None else self.default_root_path
        self.result_path = (
            result_path if result_path is not None else self.default_result_path
        )
        self.result_title = (
            result_title if result_title is not None else result_filename
        )
        self.result_filename = result_filename
        self.is_sorted = is_sorted
        if hasattr(is_target_file, "__call__"):
            self.is_target_file = is_target_file
        else:
            self.is_target_file = lambda filename: self.is_target_file_auto(
                filename, *is_target_file
            )

    @staticmethod
    def is_target_file_auto(file_name, limit_low, limit_high):
        if file_name.__contains__("."):  # is not a directory
            file_name, file_type = file_name.split(".")[0:2]
            if (
                file_type == "md"
                and file_name.isdigit()
                and limit_low <= int(file_name) < limit_high
            ):
                return True
        return False

    @staticmethod
    def title_format(title):
        """transfer the *title* to readable format"""
        title = re.sub("#+? |\n", "", title)
        title = re.sub("\\\\. ", " ", title)
        return title

    def title_to_link(self, file_name, title):
        """transfer the *title* in the *file_name* to relative link"""
        title_dic = {
            r"\n|\.|\\\\|": r"",
            r"#+ ": r"#",
            r" |:": r"-",
            r"\(.+?\)": r"",
        }
        for pattern in title_dic.keys():
            title = re.sub(pattern, title_dic[pattern], title)

        # get the relpath from result_path to the processing file
        path = os.path.relpath(
            os.path.abspath(os.path.join(self.root_path, file_name)), self.result_path
        )

        id = path + title
        return id.lower()

    def titles_sort(self, titles):
        """sort the *titles* list"""

        # title to index
        index_to_title_dic = {}
        for t in titles:
            t_split = t.split(" ")[0].split(".")
            index = ""
            for i in range(self.max_title_level):
                if len(t_split) > i and t_split[i].isdigit():
                    index += t_split[i].zfill(3)
                else:
                    index += "000"
            index_to_title_dic[int(index)] = t

        sorted_index = list(index_to_title_dic.keys())
        sorted_index.sort()
        res = []

        for i in sorted_index:
            res.append((index_to_title_dic[i]))
        return res

    def generate(self):
        # get all the titles, links and their levels
        links = {}
        levels = {}
        for file in os.listdir(self.root_path):
            if self.is_target_file(file):
                with open(self.root_path + file, "r") as f:
                    titles = re.findall("\n#+?.+\n|^#+?.+\n", f.read())
                    for t in titles:
                        t_level = t.count("#")
                        if t_level < self.max_title_level:
                            t_title = self.title_format(t)
                            t_link = self.title_to_link(file, t)

                            levels[t_title] = t_level
                            links[t_title] = t_link

        # sort the titles
        if self.is_sorted:
            titles_sorted = links.keys()
        else:
            titles_sorted = self.titles_sort(links.keys())

        # produce the directory
        directory = self.result_title + "\n"
        for t in titles_sorted:
            directory += (levels[t] - 1) * 4 * " "
            directory += "* [{}]({})\n".format(t, links[t])

        # check and write to file
        path = self.result_path + self.title_format(self.result_filename)
        if self.manual_check:
            print(
                directory[:500]
                + "\n"
                + "=" * 66
                + "\nPreview the first 500 chars of the directory here"
            )
            check = input(
                "Make sure the file will be written to: {}?\n(y/n)>>>".format(path)
            )
            if check not in ["y", "Y", "yes"]:
                return
        with open(path, "w") as f:
            f.write(directory)
            print("Write directory to:" + path)


if __name__ == "__main__":
    DirectoryProducer.config(
        manual_check=False,
        default_max_title_level=3,
        default_result_path="./0.21.3/",
        default_root_path="./0.21.3/",
    )

    job_list = [
        {
            "result_filename": "1.md",
            "result_title": "# 1. 监督学习",
            "is_target_file": (2, 19),
        },
        {
            "result_filename": "19.md",
            "result_title": "# 2. 无监督学习",
            "is_target_file": (20, 29),
        },
        {
            "result_filename": "29.md",
            "result_title": "# 3. 模型选择和评估",
            "is_target_file": (30, 35),
        },
        {
            "result_filename": "35.md",
            "result_title": "# 4. 检验",
            "is_target_file": (36, 37),
        },
        {
            "result_filename": "new_37.md",
            "result_title": "# 5. 数据集转换",
            "is_target_file": (38, 47),
        },
        # {
        #     "result_filename": "50.md",
        #     "result_title": "# scikit-learn 教程 0.21.x",
        #     "is_target_file": (51, 62),
        #     "is_sorted":True,
        # },
        # {
        #     "result_filename": "new_52.md",
        #     "result_title": "# 关于科学数据处理的统计学习教程",
        #     "is_target_file": (53, 59),
        #     "max_title_level":2,
        #     "is_sorted":True,
        # },
    ]

    for job in job_list:
        DirectoryProducer(**job).generate()
