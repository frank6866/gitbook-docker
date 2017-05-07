import inspect


def fun(key1, key2):
    print key1
    print key2


if __name__ == "__main__":
    args_dict = {"key1": "value1", "key2": "value2"}
    print dir(fun)
    print inspect.getargspec(fun)
    args = inspect.getargspec(fun)[0]
    eval("fun(1, 2)")
    print args




