from math import radians

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import haversine_distances


def DBSCAN_assess(info: str) -> tuple[np.array, np.array, np.array]:
    sites = pd.read_csv('data/siteInfo/'+info+'.csv')
    prepro = list(map(lambda point: list(map(radians, point)),
                      zip(sites['sLatitude'], sites['sLongitude'])))
    # multiply by Earth radius to get meters
    distances = haversine_distances(prepro, prepro) * 6371000
    minPts_array = np.arange(2, 7)
    eps_array = np.arange(360, 400)
    zz = []
    for eps in eps_array:
        z = []
        for minPts in minPts_array:
            try:
                dbscan = DBSCAN(
                    eps=eps,
                    min_samples=minPts,
                    metric='precomputed',
                ).fit_predict(distances)
                # z.append(len(set(dbscan)) - (1 if -1 in dbscan else 0))
                z.append(silhouette_score(prepro, dbscan))
                # z.append(calinski_harabasz_score(prepro, dbscan))
            except ValueError:
                print(eps, minPts)
                z.append(-1)
        zz.append(z)
    return minPts_array, eps_array, np.array(zz)

# SC(min): 2019->3,2020->2,4,5
# CH(min): 2019->3,2020->4
if __name__ == '__main__':
    minPts, eps, Z = DBSCAN_assess('201903')
    X, Y = np.meshgrid(minPts, eps)
    fig = plt.figure()
    ax3d = plt.axes(projection='3d')
    sur = ax3d.plot_surface(X, Y, Z, cmap='rainbow')
    ax3d.set(xlim=[np.min(minPts), np.max(minPts)], ylim=[np.min(eps), np.max(eps)],
             zlim=[np.min(Z), np.max(Z)])
    ax3d.set_xlabel('minPts (number)')
    ax3d.set_ylabel('ε (m)')
    cb = fig.colorbar(mappable=sur, fraction=0.03, pad=0.06)
    cb.locator = ticker.MaxNLocator(nbins=5)
    cb.update_ticks()
    # cb.set_label('Number of clusters', rotation=-90, labelpad=10)
    cb.set_label('SC', rotation=-90, labelpad=10)
    # cb.set_label('CH', rotation=-90, labelpad=10)
    plt.show()
    plt.close()
    