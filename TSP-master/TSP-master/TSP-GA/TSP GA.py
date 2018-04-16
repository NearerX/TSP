# -*- coding: utf-8 -*-00000000000000000000
import random
import math
import time
import matplotlib.pyplot as plt

# 城市坐标
distance_x = [
    178,272,176,171,650,499,267,703,408,437,491,74,532,
    416,626,42,271,359,163,508,229,576,147,560,35,714,
    757,517,64,314,675,690,391,628,87,240,705,699,258,
    428,614,36,360,482,666,597,209,201,492,294]
distance_y = [
    170,395,198,151,242,556,57,401,305,421,267,105,525,
    381,244,330,395,169,141,380,153,442,528,329,232,48,
    498,265,343,120,165,50,433,63,491,275,348,222,288,
    490,213,524,244,114,104,552,70,425,227,331]

# 遗传算法类
from GA import GA

#----------- TSP问题 -----------
class TSP(object):

    # 初始化
    def __init__(self,n=50):
        # 城市数目初始化为50
        self.n = n
        self.new()
            
    # 随机初始
    def new(self):
        # 初始化城市节点
        self.nodes = []  # 节点坐标

        for i in range(len(distance_x)):
            # 在画布上随机初始坐标
            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x, y))
        
        # 遗传算法
        self.ga = GA(
                lifeCount = 50,
                xRate = 0.7,
                mutationRate = 0.1,
                judge = self.judge(),
                mkLife = self.mkLife(),
                xFunc = self.xFunc(),
                mFunc = self.mFunc(),
                save = self.save()
            )

    # 得到当前顺序下连线总长度
    def distance(self, order):
        
        distance = 0
        for i in range(-1, self.n - 1):
            i1, i2 = order[i], order[i + 1]
            p1, p2 = self.nodes[i1], self.nodes[i2]
            distance += math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        return distance

    # 创造新生命
    def mkLife(self):
        def f():
            lst = list(range(self.n))
            # 随机顺序
            random.shuffle(lst)
            return lst
        return f

    # 评价函数
    def judge(self):
            
        return lambda lf,av=100: 1.0 / self.distance(lf.gene)

    # 交叉函数：选择lf2序列前子序列交叉到lf1前段，删除重复元素
    def xFunc(self):
            
        def f(lf1, lf2):
            p2 = random.randint(1, self.n - 1)
            # 截取if2
            g1 = lf2.gene[0:p2] + lf1.gene
            g11 = []
            for i in g1:
                if i not in g11:
                    g11.append(i)
            return g11
        return f
        
    # 变异函数:选择两个不同位置基因交换，第一个选择的基因重新加入到序列尾端
    def mFunc(self):
            
        def f(gene):
            p1 = random.randint(0, self.n - 1)
            p2 = random.randint(0, self.n - 1)
            while p2 == p1:
                p2 = random.randint(0, self.n - 1)
            gene[p1], gene[p2] = gene[p2], gene[p1]
            gene.append(gene[p2])
            del gene[p2]
            return gene
            
        return f

    # 保存
    def save(self):
        def f(lf, gen):
            pass
        return f

    # 进化计算  
    ii=[]
    dd=[]
    def evolve(self):
      
        for i in range(10000):
            # 下一步进化
            self.ga.next()
            print("迭代次数：%d, 变异次数%d, 最佳路径总距离：%d" % (self.ga.generation, self.ga.mutationCount, self.distance(self.ga.best.gene))) 
            self.ii.append(i)
            self.dd.append(self.distance(self.ga.best.gene))
        
    def imgshow(self):
        plt.figure(1)
        plt.plot(self.ii,self.dd)
        plt.show()
        plt.figure(2)
        plt.scatter(distance_x,distance_y)
        disx=[distance_x[i] for i in self.ga.best.gene]
        disy=[distance_y[i] for i in self.ga.best.gene]
        disx.append(distance_x[self.ga.best.gene[0]])
        disy.append(distance_y[self.ga.best.gene[0]])
        plt.plot(disx,disy)
        plt.show()
        
            
#----------- 程序的入口处 -----------
        
if __name__ == "__main__":
    start = time.clock()
    a=TSP()
    a.evolve()
    a.imgshow()
    end = time.clock()
    print("Time:",round(end-start,2))
