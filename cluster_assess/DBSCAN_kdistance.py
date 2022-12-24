from math import radians

import matplotlib.pyplot as plt
import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score, silhouette_score
from sklearn.metrics.pairwise import haversine_distances


def DBSCAN_kdistance_assess(info: str) -> pd.DataFrame:
    sites = pd.read_csv('data/siteInfo/'+info+'.csv')
    prepro = list(map(lambda point: list(map(radians, point)),
                      zip(sites['sLatitude'], sites['sLongitude'])))
    # multiply by Earth radius to get meters
    distances = haversine_distances(prepro, prepro) * 6371000
    SCscore = []
    CHscore = []
    range_object = range(3, 11)
    for k in range_object:
        try:
            # https://blog.csdn.net/Cyrus_May/article/details/113504879
            k_distances = list(map(lambda x: sorted(
                x)[k], distances))  # 第k邻近点的距离列表
            knee = KneeLocator(  # 非升序状态下的曲线拐点
                x=range(len(k_distances)),
                y=sorted(k_distances, reverse=True),
                curve='convex',
                direction='decreasing',
            )
            dbscan_ = DBSCAN(
                eps=knee.elbow_y,
                min_samples=k+1,
                metric='precomputed',
            ).fit_predict(distances)
            SCscore.append(silhouette_score(distances, dbscan_))
            CHscore.append(calinski_harabasz_score(distances, dbscan_))
        except ValueError:
            print(k+1, knee.elbow_y)
            SCscore.append(-1)
            CHscore.append(-1)
    return pd.DataFrame(data={
        'k': range_object,
        'SC': SCscore,
        'CH': CHscore,
    })


# 2019: 3,5,6,7,8 ->3,3,3,2,3
# 2020: 4,5,6,8 -> 3,3,3,3
if __name__ == '__main__':
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    data201903 = DBSCAN_kdistance_assess('201903')
    data202003 = DBSCAN_kdistance_assess('202003')
    ax1.plot('k', 'SC', 'r-x', data=data201903, label='201903')
    ax1.plot('k', 'SC', 'b-x', data=data202003, label='202003')
    ax2.plot('k', 'CH', 'r-x', data=data201903, label='201903')
    ax2.plot('k', 'CH', 'b-x', data=data202003, label='202003')
    ax1.set(ylabel='silhouette_score',
            title='eps: the knee of k-distance list, min: k+1')
    ax2.set(ylabel='calinski_harabasz_score', xlabel='k')
    ax1.legend()
    ax2.legend()
    fig.tight_layout()
    plt.show()
    plt.close()
