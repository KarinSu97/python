#多进程，进程的内存资源是独立的
from multiprocessing import Process
import time

def f(n):
    time.sleep(1)
    print(n**2)

if __name__=='__main__':
    for i in range(10):
        p=Process(target=f,args=[i,])
        p.start()


#进程池，用于批量创建子进程
from multiprocessing import Pool
import time

def f(n):
    print(n**2)
    time.sleep(2)
    return x**2

if __name__=='__main__':
    #定义启动的进程数量
    pool=Pool(processes=5)
    res_list=[]
    for i in range(10):
        #以异步并行的方式启动进程
        res=pool.apply_async(f,[i,])
        res_list.append(res)
    pool.close()
    pool.join()

#多线程，线程是公用内存资源的
import threading

lock=threading.Lock()
def run(info_list,n):
    lock.acquire()
    info_list.append(n)
    lock.release()
    print('%s\n' % info_list)

if __name__=='__main__':
    info=[]
    for i in range(10):
        p=threading.Thread(target=run,args=[info,i])
        p.start()
        p.join()