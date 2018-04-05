from surprise import KNNBasic,SVD
from surprise import Dataset
from surprise import evaluate,print_perf
from surprise import GridSearch
import pandas as pd
import io

#载入数据集，该数据集是一个电影评分数据集,数据结构：uid,iid,score,time
data=Dataset.load_builtin('ml-100k')

#将数据集采用交叉验证均分为3份
data.split(n_folds=3)

'''协调过滤'''
#使用协调过滤算法
algo=KNNBasic()

#评估算法的效果，这里采用RMSE和MAE
perf=evaluate(algo,data,measures=['rmse','mae'])
print_perf(perf)

'''SVD分解'''
#指定参数取值范围
param_grid={'n_epochs': [5, 10], 'lr_all': [0.002, 0.005],'reg_all': [0.4, 0.6]}
#利用surprise自带的GridSearch确定最优参数
grid_search=GridSearch(SVD,param_grid,measures=['rmse','fcp'])
grid_search.evaluate(data)

#确定最优参数和结果
print(grid_search.best_score['rmse'])
print(grid_search.best_params['rmse'])
print(grid_search.best_score['fcp'])
print(grid_search.best_params['fcp'])
result=pd.DataFrame.from_dict(grid_search.cv_results)
result

#进行推荐
def read_item_names():
    file_name=('C:\\Users\\T\\.surprise_data\\ml-100k\\ml-100k\\u.item')
    rid_to_name={}
    name_to_rid={}
    with io.open(file_name,'r',encoding='ISO-8859-1') as f:
        for line in f:
            line=line.split('|')
            rid_to_name[line[0]]=line[1]
            name_to_rid[line[1]]=line[0]
    return rid_to_name,name_to_rid
rid_to_name,name_to_rid=read_item_names()

#采用基于物品的协同过滤
transet=data.build_full_trainset()
algo=KNNBasic(sim_options={'name': 'pearson_baseline', 'user_based': False})
algo.train(transet)

#查看电影Now and Then (1995)最相似的10部电影
toy_story_raw_id = name_to_rid['Now and Then (1995)']
toy_story_raw_id
toy_story_inner_id=algo.trainset.to_inner_iid(toy_story_raw_id)
toy_story_inner_id
toy_story_neighbors=algo.get_neighbors(toy_story_inner_id,k=10)
toy_story_neighbors

#将10部电影转化为对应的名字
toy_story_neighbors = (algo.trainset.to_raw_iid(inner_id)
                       for inner_id in toy_story_neighbors)
toy_story_neighbors = (rid_to_name[rid]
                       for rid in toy_story_neighbors)
for movie in toy_story_neighbors:
    print(movie)