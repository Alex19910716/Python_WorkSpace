import codecs
import jieba
import os
from jieba import posseg

'''
流浪地球人物关系
'''


class Earth(object):

    # 初始化
    def __init__(self):
        # 姓名字典
        self.names = {}
        # 关系字典
        self.relationships = {}
        # 每段内人物关系
        self.lineNames = []

    # 分词方法
    def analyze_word(self):
        # 加载字典
        jieba.load_userdict(os.path.abspath(os.curdir) + "/resources/person.txt")
        with codecs.open(os.path.abspath(os.curdir) + "/resources/The Wandering Earth.txt", "r", "utf-8") as f:
            for line in f.readlines():
                # 分词返回词性
                poss = posseg.cut(line)
                # 为新读取的一段添加人物关系
                self.lineNames.append([])
                for w in poss:
                    # print("%s:%s" % (w.word, w.flag))
                    if w.flag != "nr" or len(w.word) < 2:
                        # 分词长度小于2 或词性不为nr时则与影片所需分析人物无关
                        continue
                    self.lineNames[-1].append(w.word)
                    if self.names.get(w.word) is None:
                        self.names[w.word] = 0
                        self.relationships[w.word] = {}
                    # 人物出现次数+1
                    self.names[w.word] += 1

    # 查看人物出现次数
    def names_info(self):
        for name, times in self.names.items():
            print(name, times)
        print(self.lineNames)
        print(self.relationships)

    # 分析人物关系
    def analyze_relationship(self):
        for line in self.lineNames:
            for name1 in line:
                for name2 in line:
                    if name1 == name2:
                        continue
                    if self.relationships[name1].get(name2) is None:
                        # 两个人物第一次共同出现 初始化次数
                        self.relationships[name1][name2] = 1
                    else:
                        # 两个人物共同出现 关系+1
                        self.relationships[name1][name2] += 1

    # 写txt文件 用于网络图使用
    def generate_gephi(self):
        # 人物权重(节点)
        with codecs.open(os.path.abspath(os.curdir) + "/resources/earth_node.csv", "w", "gbk") as f:
            f.write("Id Label Weight\r\n")
            for name, times in self.names.items():
                f.write(name + " " + name + " " + str(times) + "\r\n")

        # 人物关系边(边)
        with codecs.open(os.path.abspath(os.curdir) + "/resources/earth_edge.csv", "w", "gbk") as f:
            f.write("Source Target Weight\r\n")
            for name, edge in self.relationships.items():
                for v, w in edge.items():
                    if w > 3:
                        f.write(name + " " + v + " " + str(w) + "\r\n")


if __name__ == "__main__":
    earth = Earth()
    earth.analyze_word()
    earth.analyze_relationship()
    # earth.names_info()
    earth.generate_gephi()
