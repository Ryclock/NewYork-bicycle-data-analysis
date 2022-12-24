from math import radians

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score, silhouette_score
from sklearn.metrics.pairwise import haversine_distances


def DBSCAN_assess(info: str) -> pd.DataFrame:
    sites = pd.read_csv('data/siteInfo/'+info+'.csv')
    prepro = list(map(lambda point: list(map(radians, point)),
                      zip(sites['sLatitude'], sites['sLongitude'])))
    # multiply by Earth radius to get meters
    distances = haversine_distances(prepro, prepro) * 6371000
    if info == '201903':
        minPts = 3
    else:
        minPts = 4
    eps_array = np.arange(397.524, 397.526, 0.0001)
    SCscore = []
    CHscore = []
    for eps in eps_array:
        try:
            labels = DBSCAN(
                eps=eps,
                min_samples=minPts,
                metric='precomputed',
            ).fit_predict(distances)
            SCscore.append(silhouette_score(prepro, labels))
            CHscore.append(calinski_harabasz_score(prepro, labels))
        except ValueError:
            print(eps, minPts)
            SCscore.append(-1)
            CHscore.append(-1)
    return pd.DataFrame(data={
        'eps': eps_array,
        'SC': SCscore,
        'CH': CHscore,
    })


# 2019: min=3, eps=388.886
# 2020: min=4, eps=397.5244
if __name__ == '__main__':
   #  data201903 = DBSCAN_assess('201903')
    data202003 = DBSCAN_assess('202003')
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
   #  ax1.plot('eps', 'SC', 'r-', data=data201903, label='201903')
    ax1.plot('eps', 'SC', 'b-x', data=data202003, label='202003')
   #  ax2.plot('eps', 'CH', 'r-', data=data201903, label='201903')
    ax2.plot('eps', 'CH', 'b-x', data=data202003, label='202003')
    ax1.set(ylabel='silhouette_score')
    ax1.legend()
    ax2.set(ylabel='calinski_harabasz_score', xlabel='eps')
    ax2.legend()
    fig.tight_layout()
    plt.show()
    plt.close()
