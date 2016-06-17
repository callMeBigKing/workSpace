clear;
clc;
maxIter=50;%最大迭代次数
cityNum=20;%城市个数
distance=rand(cityNum)*100;
distance=tril(distance,-1)+triu(distance',0);  %生成随机距离矩阵
GA=Engine(distance);%生成对象
GA=GA.InitPop();%初始化
bestFitness=zeros(1,maxIter);
aveFitness=zeros(1,maxIter);
for iter=1:maxIter %迭代
   GA= GA.Breed();%繁殖包括交叉繁殖和变异
   bestFitness(iter)=GA.totalDistance-GA.bestFitness;
   aveFitness(iter)=GA.totalDistance-GA.aveFitness;
   hold on;
end
iter=linspace(1,maxIter,maxIter);
plot(iter,bestFitness,'--',iter,aveFitness)



