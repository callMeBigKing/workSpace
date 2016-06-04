import numpy as np
import random as ran
from math import pow
import matplotlib.pyplot as plt

def initTao():
    # 计算初始化时信息素，从第一个点出发采用贪婪算法
    init=Ant()
    while init.allow:
        start=init.route[len(init.route)-1]
        chose=init.allow[0]
        for i in init.allow:
            if city[start,chose]>city[start,i]:
                chose=i
        init.route.append(chose)
        init.allow.remove(chose)
    init.CalLength()
    return antNum/init.length

class Ant:
    # 都采用ndarray类型,ndarray删除很麻烦不用了，后面的处理和操作都用list
    # 注意这里city需要设置成从零开始
    route=[]
    allow=[]
    length=0
    def __init__(self):
        self.route=[]
        initCity=ran.randint(0,cityNmu-1)
        # randint 是闭区间
        self.allow=list(range(cityNmu))
        # range 是左闭右开区间
        self.append(initCity)

    def append(self,city):
        self.route.append(city)
        self.allow.remove(city)
    def CalLength(self):
        self.length=0
        for i in range(len(self.route)-1):
            self.length+=city[self.route[i],self.route[i+1]];

def init():
#     初始化
    population=[]
    for i in range(antNum):
        population.append(Ant())
    return population
def search():
#     搜寻食物，就是寻找一条路径
    for ant in population:
        while ant.allow:
            ant.append(Next(ant))
        ant.CalLength()


def Next(ant):
    #给出ant的下一个城市
    start=ant.route[-1]
    rand=ran.random()
    flag=0
    for j in ant.allow:
        flag+=TransferP(ant,start,j)
        if flag>=rand:
            return j

def TransferP(ant,i,j):

    #计算（i,j）之间的转移概率
    fenzi=pow(tao[i,j],alfa)*pow(1/city[i,j],beta)
    fenmu=0
    for j in ant.allow:
        fenmu+=pow(tao[i,j],alfa)*pow(1/city[i,j],beta)
    return fenzi/fenmu

def updataTao(tao):
    # 更新tao矩阵
    detaTao=np.zeros((cityNmu,cityNmu))
    for ant in population:
        for i in range(len(ant.route)-1):
            detaTao[ant.route[i],ant.route[i+1]]+=antNum/cityNmu/ant.length

    tao=(1-rho)*tao+detaTao
    return tao
def CalBest():
    length=0
    best=population[0]
    for ant in population:
        length+=ant.length
        if best.length>ant.length:
            best=ant
    length/=antNum
    aveLength.append(length)
    bestAnt.append(best)
def plot():
    shortLength=[]
    for i in bestAnt:
        shortLength.append(i.length)
    plt.figure(figsize=(8,4))
    iterList=list(range(maxIter))
    plt.plot(iterList,aveLength)
    plt.plot(iterList,shortLength,color="red")
    plt.show()

if __name__ == '__main__':
    antNum=300
    cityNmu=10
    city=np.random.randint(1,high=cityNmu*2,size=[cityNmu,cityNmu])
    city=np.triu(city)
    city+=city.T
    # city和tao采取ndarray类型
    alfa=1
    beta=0.5
    rho=0.5
    maxIter=100
    tao=np.ones((cityNmu,cityNmu))
    tao=tao*initTao()
    population=init()
    aveLength=[]
    bestAnt=[]
    for i in range(maxIter):
        population=init()
        search()
        tao=updataTao(tao)
        CalBest()
    plot()
    print("finsh")



