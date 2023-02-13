# 中间件可以理解为装饰器
# 目标：在不改变试图代码的前提下，为视图添加额外的功能
"迭代器"

# 试图函数的中间件
def outer(fuc):
    print('初始化1')

    def inner(*args, **kwargs):
        print('试图处理之前执行内容1')
        fuck = fuc(*args, **kwargs)
        print('试图处理之后执行内容１')
        return fuck

    return inner

# 试图函数的中间件
def outer2(fuc):
    print('初始化2')

    def inner2(*args, **kwargs):
        print('试图处理之前执行内容2')
        fuck = fuc(*args, **kwargs)
        print('试图处理之后执行内容2')
        return fuck

    return inner2

# 试图函数的中间件
def outer3(fuc):
    print('初始化3')

    def inner3(*args, **kwargs):
        print('试图处理之前执行内容3')
        fuck = fuc(*args, **kwargs)
        print('试图处理之后执行内容3')
        return fuck

    return inner3