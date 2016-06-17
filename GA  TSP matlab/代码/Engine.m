classdef Engine
    %engine �˴���ʾ�йش����ժҪ
    %   �˴���ʾ��ϸ˵��
    %�����о�����һ���ṹ���һ��static������ô����ô�����
    % GA ���棬�����Ŵ��㷨����Ҫ�õ��ķ�����������������
    %%ע������matlab������һ��α����������ķ�����Ӧд�ɶ�������һ�鹦�ܵĲ���
    properties
        cityNum
        %����Ľ��������еĸ���
        distance
        % distance �Ƕ�ά��������
        totalDistance
        %distance���ܾ���
        popSize
        %��Ⱥ����
        crossoverRate
        %���򽻲����
        mutationRate
        %����ͻ�����
        population
        %��Ⱥ population��һΨ��������洢����Individual����
        bestFitness
        worstFitness
        totalFitness
        aveFitness
        best
    end
    
    methods
        function obj=Engine(varargin)
            %���matlab û������ֻ��ǿ���ֶ�����  ע�����˳�� distance,popSize,crossoverRate,mutationRate
            %����ֻ��
             nargin=length(varargin);
             switch nargin
                 case 1 % ���д����case �Ͳ�д̫��������
                     %ֻ��distance
                     obj.distance=varargin{1};
                     obj.popSize=100;
                     obj.crossoverRate=0.7;
                     obj.mutationRate=0.1;
                   
                 case 4
                     %ȫ������
                      obj.distance=varargin{1};
                      obj.popSize=varargin{2};
                      obj.crossoverRate=varargin{3};
                      obj.mutationRate=varargin{4};
                 otherwise
                     error('������Ϣ����')
                   
             end
            
             obj.totalDistance=sum(sum(tril(obj.distance,-1)));%%ȡ�����ǵĺ�
             obj.cityNum=size(varargin{1},2);% size��A��1/2��1����2����
        end
        
    end
    
    
     methods
              %  methods(Access='private')��������
        function obj=InitPop(obj)
           % %��ʼ����Ⱥ
            %matlab list ���趨��ֱ���þͿ�����
            for people=1:obj.popSize
                obj.population(people).gene=randperm(obj.cityNum);
                obj.population(people).fitness=obj.CalFitGene(obj.population(people).gene);
            end    
            obj=obj.CalFit();%���������Ӧ��
        end
        
        function fit=CalFitGene(obj,gene)
            fit=0;
            for city=1:obj.cityNum-1
                  %%  obj.population(people).gene(city)%% 
                    %%obj.population(people).gene(city+1)%%�������������֮��ľ���
                  %%����������һ���������һ������֮��ľ�����˼�����mod
                  fit=fit+obj.distance(gene(city),gene(city+1));
            end
            fit=fit+obj.distance(gene(1),gene(obj.cityNum));
            fit=obj.totalDistance-fit;
        end
        
         function obj=CalFit(obj)
            %������Ⱥ�������Ӧ��ƽ����Ӧ����̾���
            obj.bestFitness=obj.CalFitGene(obj.population(1).gene);
            obj.worstFitness=obj.CalFitGene(obj.population(1).gene);
            obj.totalFitness=0;
            obj.best=obj.population(1);
            for people=1:obj.popSize
                obj.totalFitness= obj.totalFitness+obj.population(people).fitness;%�����ܵ���Ӧ��
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
           %%��������Ҫ�Ǻͷ�ֳ��ص�һЩ����
         function obj=Breed(obj)
             %����������ڲ�����һ��������Ⱥ��
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
             obj=obj.Mutation();%����
             if obj.best.fitness>obj.population(1).fitness
                 obj.population(1)=obj.best;
             end
             obj=obj.CalFit();%���������Ӧ��
             
         end
         
         function father=Filter(obj)
             %���̶�ѡ��father mather
             randNum=obj.totalFitness*rand();
             addNum=0;%�ۼ���
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
             %�����babby�Ǹ����飬����������babby
             %father mather����Individual����
             %�������OX����
             babby(1)=father;
             babby(2)=mather;
             if(rand()<obj.crossoverRate)
                 %����Ҫ������н���
                 
                 point1=randi(obj.cityNum);%��ȡ����point1��point2�Ĳ���
                 point2=randi(obj.cityNum);
                 if point1>point2
                     temp=point2;
                     point2=point1;
                     point1=temp;
                 end
                 %%ʼ����point2�ں���
                
%                  for city=1:obj.cityNum
%                      babby(1).gene(city)=mather .gene(mod(city+point2,cityNum));%%babby2 ��father
%                      babby(2).gene(city)=father .gene(mod(city+point2,cityNum));%%babby1 ��mather
%                  end
                babby(1).gene=circshift(mather.gene,[0,-point2+1]);%���ƶ�point2
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
                 %���״����뾺��
                 if(father.fitness>babby(1).fitness)
                     babby(1)=father;
                 end
                 if(mather.fitness>babby(2).fitness)
                     babby(2)=mather;
                 end
             end
             
         end
         
         function obj=Mutation(obj)
             %%�任����λ�õõ�һ��6��ѡ��һ����Ӧ����ߵ�
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
             %%%�����е���������ٸ�
             mutationPoint=randperm(obj.cityNum,3);
             mutation(1)=people;
             for i=1:length(mutationPoint)
                 for j=i+1:length(mutationPoint)
                     %����
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

