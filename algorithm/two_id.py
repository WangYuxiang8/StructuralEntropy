"""
    author: wangyuxiang
    date: 2021-2-28

    为了保存已经求出来的两个社区合并之后熵的变化量
"""


class TwoID(object):

    def __init__(self, id1, id2):
        self.id1 = id1      # int
        self.id2 = id2      # int

    def __str__(self):
        return "TwoID [ID1=" + str(self.id1) + ", ID2=" + str(self.id2) + "]"

    def get_id1(self):
        return self.id1

    def get_id2(self):
        return self.id2
