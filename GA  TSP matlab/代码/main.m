clear;
clc;
maxIter=50;%����������
cityNum=20;%���и���
distance=rand(cityNum)*100;
distance=tril(distance,-1)+triu(distance',0);  %��������������
GA=Engine(distance);%���ɶ���
GA=GA.InitPop();%��ʼ��
bestFitness=zeros(1,maxIter);
aveFitness=zeros(1,maxIter);
for iter=1:maxIter %����
   GA= GA.Breed();%��ֳ�������深ֳ�ͱ���
   bestFitness(iter)=GA.totalDistance-GA.bestFitness;
   aveFitness(iter)=GA.totalDistance-GA.aveFitness;
   hold on;
end
iter=linspace(1,maxIter,maxIter);
plot(iter,bestFitness,'--',iter,aveFitness)



