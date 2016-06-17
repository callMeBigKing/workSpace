classdef Engine
    %engine 此处显示有关此类的摘要
    %   此处显示详细说明
    %这个类感觉像是一个结构体和一坨static方法怎么用怎么不舒服
    % GA 引擎，整个遗传算法所需要用到的方法都在这里面设置
    %%注意由于matlab的类是一种伪类所以里面的方法都应写成对整个类一块功能的操作
    properties
        cityNum
        %问题的阶数即城市的个数
        distance
        % distance 是二维距离数组
        totalDistance
        %distance的总距离
        popSize
        %种群数量
        crossoverRate
        %基因交叉概率
        mutationRate
        %基因突变概率
        population
        %种群 population是一唯数组里面存储的是Individual对象
        bestFitness
        worstFitness
        totalFitness
        aveFitness
        best
    end
    
    methods
        function obj=Engine(varargin)
            %叼逼matlab 没有重载只能强行手动重载  注意参数顺序 distance,popSize,crossoverRate,mutationRate
            %可以只给
             nargin=length(varargin);
             switch nargin
                 case 1 % 随便写几个case 就不写太多重载了
                     %只有distance
                     obj.distance=varargin{1};
                     obj.popSize=100;
                     obj.crossoverRate=0.7;
                     obj.mutationRate=0.1;
                   
                 case 4
                     %全部都给
                      obj.distance=varargin{1};
                      obj.popSize=varargin{2};
                      obj.crossoverRate=varargin{3};
                      obj.mutationRate=varargin{4};
                 otherwise
                     error('输入信息错误')
                   
             end
            
             obj.totalDistance=sum(sum(tril(obj.distance,-1)));%%取下三角的和
             obj.cityNum=size(varargin{1},2);% size（A，1/2）1行数2列数
        end
        
    end
    
    
     methods
              %  methods(Access='private')报错。。。
        function obj=InitPop(obj)
           % %初始化种群
            %matlab list 无需定义直接用就可以了
            for people=1:obj.popSize
                obj.population(people).gene=randperm(obj.cityNum);
                obj.population(people).fitness=obj.CalFitGene(obj.population(people).gene);
            end    
            obj=obj.CalFit();%计算最佳适应度
        end
        
        function fit=CalFitGene(obj,gene)
            fit=0;
            for city=1:obj.cityNum-1
                  %%  obj.population(people).gene(city)%% 
                    %%obj.population(people).gene(city+1)%%计算的是这两者之间的距离
                  %%还需计算最后一个城市与第一个城市之间的距离因此加上了mod
                  fit=fit+obj.distance(gene(city),gene(city+1));
            end
            fit=fit+obj.distance(gene(1),gene(obj.cityNum));
            fit=obj.totalDistance-fit;
        end
        
         function obj=CalFit(obj)
            %计算种群的最佳适应度平均适应度最短距离
            obj.bestFitness=obj.CalFitGene(obj.population(1).gene);
            obj.worstFitness=obj.CalFitGene(obj.population(1).gene);
            obj.totalFitness=0;
            obj.best=obj.population(1);
            for people=1:obj.popSize
                obj.totalFitness= obj.totalFitness+obj.population(people).fitness;%计算总的适应度
                if obj.bestFitness<obj.population(people).fitness
                   obj.bestFitness=obj.population(people).fitness;
                    obj.best=obj.population(people);
                end
                if obj.worstFitness>obj.population(people).fitness
                   obj.worstFitness=obj.population(people).fitness;
                end
            end  
            obj.aveFitness=obj.totalFitness/obj.popSize;
            
         end
         
         

         
     end
     
              
       methods  
           %%这里面主要是和繁殖相关的一些函数
         function obj=Breed(obj)
             %这个函数用于产生下一代跟换种群，
             for i=1:2:obj.popSize
                 father=obj.Filter();
                 mather=obj.Filter();
                 babby=obj.Crossover(father,mather);
                 if(i<obj.popSize)
                     obj.population(i)=babby(1);
                 end
                 if(i+1<obj.popSize)
                     obj.population(i+1)=babby(2);
                 end
             end
             obj=obj.Mutation();%变异
             if obj.best.fitness>obj.population(1).fitness
                 obj.population(1)=obj.best;
             end
             obj=obj.CalFit();%计算最佳适应度
             
         end
         
         function father=Filter(obj)
             %轮盘赌选出father mather
             randNum=obj.totalFitness*rand();
             addNum=0;%累加数
             father=obj.population(1);
             for people=1:obj.popSize
                 addNum=addNum+obj.population(people).fitness;
                 if addNum>=randNum
                     father=obj.population(people);
                     break;
                 end
             end
     
         end
         
         function babby=Crossover(obj,father,mather)
             %这里的babby是个数组，里面有两个babby
             %father mather都是Individual对象
             %这里采用OX交叉
             babby(1)=father;
             babby(2)=mather;
             if(rand()<obj.crossoverRate)
                 %满足要求则进行交叉
                 
                 point1=randi(obj.cityNum);%采取包括point1和point2的操作
                 point2=randi(obj.cityNum);
                 if point1>point2
                     temp=point2;
                     point2=point1;
                     point1=temp;
                 end
                 %%始终让point2在后面
                
%                  for city=1:obj.cityNum
%                      babby(1).gene(city)=mather .gene(mod(city+point2,cityNum));%%babby2 是father
%                      babby(2).gene(city)=father .gene(mod(city+point2,cityNum));%%babby1 是mather
%                  end
                babby(1).gene=circshift(mather.gene,[0,-point2+1]);%左移动point2
                babby(2).gene=circshift(father.gene,[0,-point2+1]);
                
                 for pitch=point1:point2
                     repeatPoint1=find(babby(1).gene==father.gene(pitch));
                     babby(1).gene(repeatPoint1)=[];
                     repeatPoint2=find(babby(2).gene==mather.gene(pitch));
                     babby(2).gene(repeatPoint2)=[];
                 end
                 
                 babby(1).gene=[father.gene(point1:point2),babby(1).gene];
                 babby(2).gene=[mather.gene(point1:point2),babby(2).gene];
                 
                 babby(1).gene=circshift(babby(1).gene,[0,point1-1]);
                 babby(1).fitness=obj.CalFitGene( babby(1).gene);
                 babby(2).gene=circshift( babby(2).gene,[0,point1-1]);
                 babby(2).fitness=obj.CalFitGene( babby(2).gene);
                 %父亲代参与竞争
                 if(father.fitness>babby(1).fitness)
                     babby(1)=father;
                 end
                 if(mather.fitness>babby(2).fitness)
                     babby(2)=mather;
                 end
             end
             
         end
         
         function obj=Mutation(obj)
             %%变换三个位置得到一共6个选出一个适应度最高的
             for people=1:obj.popSize
                 randNum=rand();
                 if randNum>obj.mutationRate
                     continue
                 else
                 end
                 obj.population(people)=obj.IndividualMutation(obj.population(people));
             end
         
         end
         
         function mutation=IndividualMutation(obj,people)
             %%%处理有点问题后期再改
             mutationPoint=randperm(obj.cityNum,3);
             mutation(1)=people;
             for i=1:length(mutationPoint)
                 for j=i+1:length(mutationPoint)
                     %交换
                     mutation(i+j-1)=people;
                     mutation(i+j-1).gene(mutationPoint(i))=people.gene(mutationPoint(j));
                     mutation(i+j-1).gene(mutationPoint(j))=people.gene(mutationPoint(i));
                 end
             end
             
             for i=2:length(mutation)
                 if mutation(1).fitness<mutation(i).fitness
                     mutation(1)=mutation(i);
                 end
             end
             mutation= mutation(1);
         end
         
       end
         
         
         
end

