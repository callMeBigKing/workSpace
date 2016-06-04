clear;
clc;
maxIter=100;%最大迭代次数
cityNum=20;%城市个数
distance=rand(cityNum)*100;
distance=tril(distance,-1)+triu(distance',0);  %生成随机距离矩阵
GA=Engine(distance);%生成对象
GA=GA.InitPop();%初始化
for iter=1:maxIter %迭代
   GA= GA.Breed();%繁殖包括交叉繁殖和变异
   plot(iter,GA.totalDistance-GA.bestFitness,'--',iter,GA.totalDistance-GA.aveFitness,'*')
   hold on;
end

