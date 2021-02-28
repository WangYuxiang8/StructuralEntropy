
class TestDemo(object):

    def __init__(self, my_dict):
        self.my_dict = my_dict

    def get_dict(self):
        return self.my_dict

    def set_dict(self, my_dict):
        self.my_dict = my_dict


def test_1():
    t = TestDemo({1:'a', 2:'b'})
    print("t is: ", str(t.get_dict()))
    d = t.get_dict()
    d.pop(1)
    print("t is: ", str(t.get_dict()))


if __name__ == '__main__':
    test_1()