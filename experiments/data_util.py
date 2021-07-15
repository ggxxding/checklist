# -*- coding:utf-8 -*-
import os
import codecs
import pandas
if __name__ == "__main__":
    rootdir = './ChnSentiCorp_htl_ba_4000/neg'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        with codecs.open(path, 'r',encoding='gb2312') as f:
            text=''
            while True:
                lines=f.readline()
                if not lines:
                    break
                    pass

                text+=lines
                pass
            print(text)