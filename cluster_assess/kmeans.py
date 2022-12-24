import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, silhouette_score


# 坐标区域较小(单个城市内), 故采用欧氏距离近似于经纬度球面距离(但仍可能存在少许误差)
def kmeans_assess(info: str) -> pd.DataFrame:
    sites = pd.read_csv('data/siteInfo/'+info+'.csv')
    label = pd.DataFrame(data={
        'longitude': sites['sLongitude'],
        'latitude': sites['sLatitude'],
    })
    prepro = label
    k = [i for i in range(20, 51)]
    SCscore = []
    CHscore = []
    for i in k:
        labels = KMeans(
            n_clusters=i,
            tol=0,
        ).fit_predict(prepro)
        SCscore.append(silhouette_score(prepro, labels))
        CHscore.append(calinski_harabasz_score(prepro, labels))
    return pd.DataFrame(data={
        'K': k,
        'SC': SCscore,
        'CH': CHscore,
    })


# 2019: (20-0,20+0),[40,45]
# 2020: (20-0,20+0),(30-0,30+0)
if __name__ == '__main__':
    data201903 = kmeans_assess('201903')
    data202003 = kmeans_assess('202003')
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax1.set(ylabel='silhouette_score')
    ax1.plot('K', 'SC', 'r-', data=data201903, label='201903')
    ax1.plot('K', 'SC', 'b-', data=data202003, label='202003')
    ax1.legend()
    ax2.set(ylabel='calinski_harabasz_score', xlabel='K')
    ax2.plot('K', 'CH', 'r-', data=data201903, label='201903')
    ax2.plot('K', 'CH', 'b-', data=data202003, label='202003')
    ax2.legend()
    fig.tight_layout()
    plt.show()
    plt.close()
