import numpy as np
def distance(x,y):
#     x,y的距离，x,y为array
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))



def KNNClassify(testData,trainData,listClasses,k):
    # testData 一维  trainData 多维 martix，
    dataSetSize=trainData.shape[0] #行数
    distances=np.zeros(dataSetSize)
    for index in range(dataSetSize):
        # 矩阵索引给一个参数索引到行
        distances[index]=distance(trainData[index],testData)
    sortedDistIndeicies=np.argsort(distances)
    # sort 返回的结果是从小到大
    classCount={}
    for i in  range(k):
        iVote=listClasses[sortedDistIndeicies[i]]
        classCount.iVote=classCount.get(iVote,0)+1

#         sorted(dic,value,reverse) 对字典进行排序
# •dic为比较函数，value 为排序的对象（这里指键或键值），
# •reverse：注明升序还是降序，True--降序，False--升序（默认）
    sortedCount=sorted(classCount.items(),key=lambda asd:asd[1],reverse=True)
    return sortedCount[0][0]
