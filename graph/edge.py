"""
    author: wangyuxiang
    date: 2021-2-26

    图边类，包含：
        - 源结点ID
        - 目的结点ID
        - 边权重
"""


class Edge(object):

    def __init__(self, src_id, dst_id, weight):
        self.src_id = src_id
        self.dst_id = dst_id
        self.weight = weight

    def get_src_id(self):
        return self.src_id

    def set_src_id(self, src_id):
        self.src_id = src_id

    def get_dst_id(self):
        return self.dst_id

    def set_dst_id(self, dst_id):
        self.dst_id = dst_id

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    # 返回边信息（字符串）
    def to_string(self):
        return "Edge [SrcId=]" + str(self.src_id) + ", DstId=" + str(self.dst_id) \
               + ", Weight=" + str(self.weight) + "]"
