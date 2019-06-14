# python3
# -*- coding: utf-8 -*-
# @File    : md_directory_producer.py
# @Desc    : md文档的目录生成器
# @Software: PyCharm
# @Time    : 19-6-14 下午7:25
# @Author  : Loopy
# @Contact : peter@mail.loopy.tech

import re
import os


def title_to_link(file_name, title):
    """transfer the *title* in the *file_name* to relative link"""
    global root_path, result_path
    dic = {'\n|\.|\\\\|\(|\)': '',
           '#+ ': '?id=_',
           ' ': '-'}
    for pattern in dic.keys():
        title = re.sub(pattern, dic[pattern], title)

    # get the relpath from result_path to the processing file
    path = os.path.relpath(os.path.abspath(os.path.join(root_path, file_name)), result_path)

    id = path + title
    return id.lower()


def title_format(title):
    """transfer the *title* to readable format"""
    title = re.sub('#+? |\n', '', title)
    title = re.sub('\\\\. ', ' ', title)
    return title


def titles_sort(titles):
    """sort the *titles* list"""
    global max_title_level

    # title to index
    index_to_title_dic = {}
    for t in titles:
        t_split = t.split(' ')[0].split('.')
        index = ''
        if len(t_split) > max_title_level and t_split[max_title_level].isdigit():
            # title level too low
            pass
        else:
            for i in range(max_title_level):
                if len(t_split) > i and t_split[i].isdigit():
                    index += t_split[i].zfill(3)
                else:
                    index += '000'
            index_to_title_dic[int(index)] = t

    sorted_index = list(index_to_title_dic.keys())
    sorted_index.sort()
    res = []

    for i in sorted_index:
        res.append((index_to_title_dic[i]))
    return res


###########################################################################################################
# parameters

# md文档所在位置
root_path = '../scikit-learn-doc-zh/docs/'

# 目录存放的目标位置（涉及相对位置的计算,生成后不可更改）
result_path = '../scikit-learn-doc-zh/'

# 目录标题（目录文件也将用此标题命名）
directory_title = "# 1.监督学习"

# 有效标题的最大层数（超过该层数的标题将不会出现在目录里）
max_title_level = 5


# 文件名有效判断函数（当不想这个文件出现在目录中时,应return False）
def is_target_file(file_name):
    """check *file_name* if it is target"""
    if file_name.__contains__('.'):  # is not a directory
        file_name, file_type = file_name.split('.')[0:2]
        if file_type == 'md' and file_name.isdigit() and 1 < int(file_name) < 19:
            return True
    return False


# 　主函数,无需修改
if __name__ == '__main__':
    # get all the titles and links
    links = {}
    for file in os.listdir(root_path):
        if is_target_file(file):
            with open(root_path + file, 'r') as f:
                titles = re.findall('\n#+?.+\n|^#+?.+\n', f.read())
                for t in titles:
                    links[title_format(t)] = title_to_link(file, t)

    # sort the titles
    titles_sorted = titles_sort(links.keys())

    # produce the directory
    directory = directory_title + '\n'
    for t in titles_sorted:
        directory += (t.count('.') - 1) * 4 * ' '
        directory += '* [{}]({})\n'.format(t, links[t])

    # check and write to file
    print(directory[:500] + '\n' + '=' * 66 + '\nPreview the first 500 chars of the directory here')
    path = result_path + title_format(directory_title) + '.md'
    check = input("Make sure the file will be written to: {}?\n(y/n)>>>".format(path))
    if check in ['y', 'Y', 'yes']:
        with open(path, 'w') as f:
            f.write(directory)
            print("Write directory to:" + path)
