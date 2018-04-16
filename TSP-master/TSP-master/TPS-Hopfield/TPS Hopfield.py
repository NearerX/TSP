# -*- coding: utf-8 -*-
import random
import copy
#import time
#import sys
import math

# 城市坐标
city_num = 8
distance_x = [
    178, 272, 176, 171, 650, 499, 267, 703, 408, 437, 491, 74, 532, 416, 626,
    42, 271, 359, 163, 508, 229, 576, 147, 560, 35, 714, 757, 517, 64, 314,
    675, 690, 391, 628, 87, 240, 705, 699, 258, 428, 614, 36, 360, 482, 666,
    597, 209, 201, 492, 294
]
distance_y = [
    170, 395, 198, 151, 242, 556, 57, 401, 305, 421, 267, 105, 525, 381, 244,
    330, 395, 169, 141, 380, 153, 442, 528, 329, 232, 48, 498, 265, 343, 120,
    165, 50, 433, 63, 491, 275, 348, 222, 288, 490, 213, 524, 244, 114, 104,
    552, 70, 425, 227, 331
]
# 城市距离
distance_graph = [ [0.0 for col in range(city_num)] for raw in range(city_num)]

#----------- TSP问题 -----------
        
class TSP(object):

    def __init__(self,n = city_num):

     
        # 城市数目初始化为city_num
        self.n = n
        self.new()
        # 计算城市之间的距离
        for i in range(city_num):
            for j in range(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))


    # 初始化
    def new(self, evt = None):

        self.A=1.5     # 变化率A
        self.D=1.0     # 变化率D
        self.u0=0.02   # 初始u值
        self.step=0.01 # 步长
        self.iter = 1  # 迭代次数
        self.path = range(city_num)

        # 计算总长度
        self.DistanceCity = self.__cal_total_distance()
        # 初始化状态
        self.U=[ [0.5*self.u0*math.log(city_num-1) for col in range(city_num)] for raw in range(city_num)]
        # 加上随机值[-1:1]
        for raw in range(city_num):
            for col in range(city_num):
                self.U[raw][col] += 2*random.random()-1
        # 阈值函数
        self.V=[ [0.0 for col in range(city_num)] for raw in range(city_num)]
        for raw in range(city_num):
            for col in range(city_num):
                self.V[raw][col] = (1+math.tanh(self.U[raw][col]/self.u0))/2
                
    # 计算路径总距离
    def __cal_total_distance(self):
        
        temp_distance = 0.0
        
        for i in range(1, city_num):
            start, end = self.path[i], self.path[i-1]
            temp_distance += distance_graph[start][end]

        # 回路
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        return temp_distance
        
    # 停止搜索
    def DeltaU(self):

        # 计算每一行的和
        rawsum = []
        for raw in range(city_num):
            raw_sum = 0
            for col in range(city_num):
                raw_sum += self.V[raw][col]
            rawsum.append(raw_sum-1)
            
        # 计算每一列的和
        colsum = []
        for col in range(city_num):
            col_sum = 0
            for raw in range(city_num):
                col_sum += self.V[raw][col]
            colsum.append(col_sum-1)
            
        # 将第一列移向最后
        deltau = copy.deepcopy(self.V)
        for raw in deltau:
            temp = raw[0]
            del raw[0]
            raw.append(temp)
            
        # 计算deltau
        for raw in range(city_num):
            for col in range(city_num):
                deltau[raw][col] = -1*(self.A*rawsum[raw]+self.A*colsum[col]+self.D*self.DistanceCity*deltau[raw][col])
                
        return deltau

    # 计算能量
    def Energy(self):

        # 计算每一行的和的平方和
        rawsum = []
        for raw in range(city_num):
            raw_sum = 0
            for col in range(city_num):
                raw_sum += self.V[raw][col]
            rawsum.append(raw_sum-1)
        rawsumsqr = 0
        for raw in rawsum:
            rawsumsqr += raw*raw
        # 计算每一列的和的平方和
        colsum = []
        for col in range(city_num):
            col_sum = 0
            for raw in range(city_num):
                col_sum += self.V[raw][col]
            colsum.append(col_sum-1)
        colsumsqr = 0
        for col in colsum:
            colsumsqr += col*col

        # 将第一列移向最后
        PermitV = copy.deepcopy(self.V)
        for raw in PermitV:
            temp = raw[0]
            del raw[0]
            raw.append(temp)
            for item in raw:
                item *= self.DistanceCity
        # 矩阵点乘和
        sumV = 0
        for raw in range(city_num):
            for col in range(city_num):
                sumV += PermitV[raw][col] * self.V[raw][col]
        # 计算能量
        E = 0.5*(self.A*rawsumsqr+self.A*colsumsqr+self.D*sumV)
        return E

    # 生成路径
    def Pathcheck(self):
        V1 = [ [0 for col in range(city_num)] for raw in range(city_num)]
        # 寻找每一列的最大值
        for col in range(city_num):
            MAX = -1.0
            MAX_raw = -1
            for raw in range(city_num):
                if self.V[raw][col] > MAX:
                    MAX = self.V[raw][col]
                    MAX_raw = raw
            # 相应位置赋值为1
            V1[MAX_raw][col] = 1
            
        # 计算每一行的和
        rawsum = []
        for raw in range(city_num):
            raw_sum = 0
            for col in range(city_num):
                raw_sum += V1[raw][col]
            rawsum.append(raw_sum)
            
        # 计算每一列的和
        colsum = []
        for col in range(city_num):
            col_sum = 0
            for raw in range(city_num):
                col_sum += V1[raw][col]
            colsum.append(col_sum)
        # 计算差的平方和
        sumV1 = 0
        for item in range(city_num):
            sumV1 += (rawsum[item] - colsum[item])**2
        # 形成路径
        path = []
        if sumV1 != 0:
            path.append(-1)
        else:
            for col in range(city_num):
                for raw in range(city_num):
                    if V1[raw][col] == 1:
                        path.append(raw)
        return path
        
    # 开始搜索
    def search_path(self):      
        
        for i in range(500):  
            delta_u = self.DeltaU()
            # 计算deltau
            for raw in range(city_num):
                for col in range(city_num):
                    self.U[raw][col] += delta_u[raw][col] * self.step
            # 计算阈值
            for raw in range(city_num):
                for col in range(city_num):
                    self.V[raw][col] = (1+math.tanh(self.U[raw][col]/self.u0))/2

            # 计算能量
            E = self.Energy()
            # 生成路径
            path = self.Pathcheck()
            if path[0] != -1:
                self.path = path
                print ("迭代次数：",self.iter,"最佳路径总距离：",int(self.__cal_total_distance()))
            else:
                print ("迭代次数：",self.iter,"失败")
            self.iter += 1
#----------- 程序的入口处 -----------
                
if __name__ == '__main__':


    TSP().search_path()
    
