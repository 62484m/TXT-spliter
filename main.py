#!/usr/bin/python3
"""
Txt Tool

Descriptions:
合并txt
分割txt

"""
import datetime
import os
import threading
import time
import tkinter as tk
import pygubu
from pygubu.builder import ttkstdwidgets
from pygubu.builder.widgets import pathchooserinput


RIGHT_COLOR = '#008000'
WRONG_COLOR = '#d70428'
BACKGROUND_COLOR = 'yellow'
RIGHT_TEXT = 'OK '
WRONG_TEXT = '[X]'
WARNING_TEXT = '[警告！]'
INFO_COLOR = '#0080ff'


class App(pygubu.TkApplication):
    """GUI 界面"""

    def __init__(self, master):
        # 线程

        super(App, self).__init__(master)

    def _create_ui(self):
        self.builder = builder = pygubu.Builder()

        ui_path = os.path.join(os.path.dirname(__file__), "Gui.ui")
        builder.add_from_file(ui_path)

        # builder.add_from_file('/Users/cynthia/Desktop/test.ui')

        self.mainwindow = builder.get_object('Frame_1', self.master)
        self.master.title('txt小工具')
        builder.connect_callbacks(self)

        # 文件选择
        self.pathchooserinput1 = self.builder.get_object('pathchooserinput_1')
        self.pathchooserinput2 = self.builder.get_object('pathchooserinput_2')

        # 按钮组件
        self.btn_combine = self.builder.get_object('Button_1')
        self.btn_split = self.builder.get_object('Button_2')

        # 输入组件
        self.Ent_split_num = self.builder.get_object('Entry_1')
        self.Tex_content = self.builder.get_object('Text_2')

        # 输出框、滚动条
        self.text_info = self.builder.get_object('Text_3')
        self.info_sc = self.builder.get_object('Scale_1')
        self.info_sc['command'] = self.text_info.yview

    def read_file(self, path):
        """
        Read data from XLS or TXT
        """
        filename, f_type = path.split('.')
        data = []

        if f_type == 'txt':
            with open(path) as f:
                qq_data = f.readlines()
                for qq in qq_data:
                    data.append(qq.strip('\n'))
            return data

        elif f_type == 'xls':
            from xlrd import open_workbook
            workbook = open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            # print(sheet.name, sheet.nrows, sheet.ncols)  # sheet的名称、行数、列数
            for row in range(1, sheet.nrows):
                content = sheet.row_values(row)
                try:
                    qq = str(int(content[0]))
                except ValueError:
                    qq = content[0]
                data.append(qq)
            return data

        else:
            self.wrong_output('错误文件类型：自动跳过。{}'.format(path))
            return

    def combine(self):
        """
        Combine Txt files into 1 txt
        """
        fpath = self.pathchooserinput1.cget('path')
        if not fpath:
            self.wrong_output('未选择文件夹')
            return

        dirs = os.listdir(fpath)
        absolute_dirs = []
        for file in dirs:
            absolute_dirs.append(os.path.join(fpath, file))

        with open(r'合并%s.txt' % str(int(time.time())), 'a') as f:
            for file in absolute_dirs:
                qq_list = self.read_file(file)
                self.right_output('读取成功{}条；{}'.format(len(qq_list), file))

                for qq in qq_list:
                    f.write(qq + '@qq.com' + '\n')

        self.right_output('读取完成，写入成功')

    def split(self):
        """
        Split 1 txt into many txts each 300 content.
        """
        fpath = self.pathchooserinput2.cget('path')
        if not fpath:
            self.wrong_output('未选择需要拆分的源文件')
            # return

        try:
            split_num = int(self.Ent_split_num.get())
            content = self.Tex_content.get('0.0', '100.0').split('\n')
        except Exception as e:
            self.wrong_output(repr(e))
            return

        with open(fpath, 'r') as f:
            qq_list = f.readlines()

        f_count = 1
        output_dir = '拆分{}/'.format(str(int(time.time())))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        for i in range(0, len(qq_list), (split_num - len(content) + 1)):
            qq_tem_list = qq_list[i: i + (split_num - len(content) + 1)]
            with open(r'{}{}.txt'.format(output_dir, f_count), 'a+') as f:
                for qq in qq_tem_list:
                    f.write(qq)
                for con in content:
                    f.write(con + '\n')
            f_count += 1
        self.right_output('拆分完成')

    def right_output(self, info=''):
        """输出样式 - 正确ok"""

        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self.text_info.tag_config('right-tag', background=BACKGROUND_COLOR, foreground=RIGHT_COLOR)
        self.text_info.insert(1.0, RIGHT_TEXT + now + info + '\n')
        self.text_info.tag_add('right-tag', '1.0', '1.4')

    def wrong_output(self, info=''):
        """输出样式 - 错误[x]"""

        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self.text_info.tag_config('wrong-tag', background=BACKGROUND_COLOR, foreground=WRONG_COLOR)
        self.text_info.insert(1.0, WRONG_TEXT + now + info + '\n')
        self.text_info.tag_add('wrong-tag', '1.0', '1.4')

    def warning_output(self, info=''):
        """输出样式 - 错误[x]"""

        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self.text_info.tag_config('wrong-tag', background=BACKGROUND_COLOR, foreground=WRONG_COLOR)
        self.text_info.insert(1.0, '\n')
        self.text_info.insert(1.0, WARNING_TEXT + now + info + '\n')
        self.text_info.tag_add('wrong-tag', '1.0', '1.6')
        self.text_info.insert(1.0, WARNING_TEXT + now + info + '\n')
        self.text_info.tag_add('wrong-tag', '1.0', '1.6')
        self.text_info.insert(1.0, WARNING_TEXT + now + info + '\n')
        self.text_info.tag_add('wrong-tag', '1.0', '1.6')


if __name__ == '__main__':
    xls_path = []
    root = tk.Tk()
    app = App(root)
    app.run()
