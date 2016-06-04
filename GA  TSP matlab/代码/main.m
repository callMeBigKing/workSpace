clear;
clc;
maxIter=100;%����������
cityNum=20;%���и���
distance=rand(cityNum)*100;
distance=tril(distance,-1)+triu(distance',0);  %��������������
GA=Engine(distance);%���ɶ���
GA=GA.InitPop();%��ʼ��
for iter=1:maxIter %����
   GA= GA.Breed();%��ֳ�������深ֳ�ͱ���
   plot(iter,GA.totalDistance-GA.bestFitness,'--',iter,GA.totalDistance-GA.aveFitness,'*')
   hold on;
end

