# def getContent():
#     while True:
#         url = yield 'I have content'
#         print('get content form url:%s'%url)
# def getUrl():
#     url_list = ['url1','url2','url3','url4','url5']
#     for i in url_list:
#         print("*"*20)
#         g.send(i)
#         print("*"*20)
# if __name__ == '__main__':
#     g = getContent()
#     print(next(g)) #到这步才会打印一句话'I have content'。不加这句话下面的语句执行会报错
#     getUrl()





# def getContext():
#     while True:
#         url = yield 'I have content'
#         print('get the url form:%s'%url)
#
# def getUrl(g):
#     url_list = ['u1','u2','u3','u4','u5']
#     for i in url_list:
#         g.send(i)
# if __name__ == '__main__':
#     g = getContext()
#     print(next(g))
#     getUrl(g)





# import gevent
# from gevent.lock import Semaphore
#
# sem = Semaphore(1)
#
# def fun1():
#     for i in range(3):
#         sem.acquire()
#         print('I am fun 1 this is %s'%i)
#         gevent.sleep(0)
#         sem.release()
#
# def fun2():
#     for i in range(5):
#         sem.acquire()
#         print('I am fun 2 this is %s'%i)
#         gevent.sleep(0)
#         sem.release()
#
# t1 = gevent.spawn(fun1)
# t2 = gevent.spawn(fun2)
#
# gevent.joinall([t1,t2])

# #Gevent框架实现协程，Gevent是一个python三方的协程框架，需要pip安装
import gevent
from gevent.lock import Semaphore  #引入信号量来设置锁

sem = Semaphore(1)

def fun1():
    for i in range(5):
        sem.acquire()     #加锁
        print('I am fun1 this is %s'%i)
        sem.release()     #释放锁

def fun2():
    for i in range(5):
        sem.acquire()
        print('I am fun2 this is %s'%i)
        sem.release()

t1 = gevent.spawn(fun1)   #设置函数
t2 = gevent.spawn(fun2)

gevent.joinall([t1,t2])   #开始运行协程中的数据




