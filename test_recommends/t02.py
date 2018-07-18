import pandas as pd
import numpy as np

# 被读取的文件
data = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5},
        'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 1.5, 'The Night Listener': 3.0},
        'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                             'Superman Returns': 3.5, 'The Night Listener': 4.0},
        'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                         'The Night Listener': 4.5, 'You, Me and Dupree': 2.5},
        'Mick LaSalle': {'Just My Luck': 2.0, 'Lady in the Water': 3.0, 'Superman Returns': 3.0,
                         'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
        'Jack Matthews': {'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0,
                          'You, Me and Dupree': 3.5},
        'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

# 数据清洗与转换
data = pd.DataFrame(data)
# 0个代表未被评定
data = data.fillna(0)
# 每列代表一部电影
mdata = data.T

# 计算不同电影的相似性，将数据归一化为[0,1]。
np.set_printoptions(3)
mcors = np.corrcoef(mdata, rowvar=0)
mcors = 0.5 + mcors * 0.5
mcors = pd.DataFrame(mcors, columns=mdata.columns, index=mdata.columns)


# 计算每个用户的每个项目的得分
# matrix：矩阵的电影用户
# mcors：电影电影相关矩阵
# item：这部电影的身份
# user:用户ID
# score:特定用户的电影评分
def cal_score(matrix, mcors, item, user):
    totscore = 0
    totsims = 0
    score = 0
    if pd.isnull(matrix[item][user]) or matrix[item][user] == 0:
        for mitem in matrix.columns:
            if matrix[mitem][user] == 0:
                continue
            else:
                totscore += matrix[mitem][user] * mcors[item][mitem]
                totsims += mcors[item][mitem]
        score = totscore / totsims
    else:
        score = matrix[item][user]
    return score


# 在成绩矩阵计算
# matrix:用户电影矩阵
# mcors:电影电影相关矩阵
# score_matrix:不同用户电影评分矩阵
def cal_matscore(matrix, mcors):
    score_matrix = np.zeros(matrix.shape)
    score_matrix = pd.DataFrame(score_matrix, columns=matrix.columns, index=matrix.index)
    for mitem in score_matrix.columns:
        for muser in score_matrix.index:
            score_matrix[mitem][muser] = cal_score(matrix, mcors, mitem, muser)
    return score_matrix


# give recommendations: 根据得分矩阵
# matrix:用户电影矩阵
# score_matrix:不同用户电影评分矩阵
# user:用户ID
# n:建议数量
def recommend(matrix, score_matrix, user, n):
    user_ratings = matrix.ix[user]
    not_rated_item = user_ratings[user_ratings == 0]
    recom_items = {}
    # recom_items={'a':1,'b':7,'c':3}
    for item in not_rated_item.index:
        recom_items[item] = score_matrix[item][user]
    recom_items = pd.Series(recom_items)
    recom_items = recom_items.sort_values(ascending=False)
    return recom_items[:n]


# 执行的方法
score_matrix = cal_matscore(mdata, mcors)
for i in range(10):
    user = input(str(i) + ' please input the name of user:')
    print
    recommend(mdata, score_matrix, user, 2)
