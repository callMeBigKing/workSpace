classdef Individual
%%�����������ֻ�洢�������Ӧ��
properties
        gene
        %%gene �Ǹ�һά���飬����ŵ����߹��ĳ��� ��2,4,3,1,5 ��ʾ��2��ʼ���ص�2��һ������
        fitness
    end

    methods
        function  obj=Individual(varargin)
           %%���캯��
           nargin=length(varargin);
           if(nargin==0)
               obj.gene=0;%�ű����Բ������������͵����⿴������ʼ��һ�¾Ϳ���
               obj.fitness=0;
           elseif(nargin==2)
                obj.gene=nargin{1};
                obj.fitness=nargin{2};
           else error('input error')
           end
        end   
        
        
    end

end
