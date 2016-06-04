classdef Individual
%%个体的类里面只存储基因和适应度
properties
        gene
        %%gene 是个一维数组，里面放的是走过的城市 如2,4,3,1,5 表示从2开始最后回到2的一个过程
        fitness
    end

    methods
        function  obj=Individual(varargin)
           %%构造函数
           nargin=length(varargin);
           if(nargin==0)
               obj.gene=0;%脚本语言不存在数据类型的问题看着随便初始化一下就可以
               obj.fitness=0;
           elseif(nargin==2)
                obj.gene=nargin{1};
                obj.fitness=nargin{2};
           else error('input error')
           end
        end   
        
        
    end

end
