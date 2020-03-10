import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time as tm
import math


R = 6371000 # Radius of Earth, meters

def getSpeed(time0, time1, coord0, coord1):
    dTime = math.fabs(time1-time0) # Time change
    if dTime == 0:
        return 0
    
    # haversine formula 
    dlon = coord1[1] - coord0[1]
    dlat = coord1[0] - coord0[0]
    a = math.sin(dlat/2)**2 + math.cos(coord0[0]) * math.cos(coord1[0]) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    d = math.fabs(c * R) # Distance change in meters
    print("Distance", d)

    return d/dTime # Speed in meters/second



def find_nearest(locs, value):
    locs = np.asarray(locs)
    idx = (np.abs(locs - value)).argmin()
    return idx

# #############################################################################
# Read data
participant = 4


doc = "locs/location_" + str(participant) +".csv"
smdoc = "sm_reports/smoking_reports_" + str(participant) +".csv"


A_MEANSHIFT = 1
A_KMEANS = 2
A_HDBSCAN = 3


alg = A_MEANSHIFT # Algorithm

df = pd.read_csv(doc, header=0, index_col=0)
sm = pd.read_csv(smdoc, header=0, index_col=0)


# Dataset descriptions:
# 1 - sparse paths with large dense blobs
# 2 - high variance with high density regions
# 3 - sparse paths with small dense blobs
# 4 - dense paths with small dense blobs
# 5 - small variance, medium-sized high density blobs
# 6 - long sparse path, Seattle


lat = np.array(df["latitude"])
lon = np.array(df["longitude"])
time = np.array(df["datetime"])
time_datetime = [datetime.datetime.strptime(str(time_string), "%Y-%m-%d %H:%M:%S") for time_string in time]
time_posix = np.array([ tm.mktime(dt.timetuple())  for dt in time_datetime])


sm_time = np.array(sm["datetime"])
sm_time_datetime = [datetime.datetime.strptime(str(time_string), "%Y-%m-%d %H:%M:%S") for time_string in sm_time]
sm_time_posix = [ tm.mktime(dt.timetuple())  for dt in sm_time_datetime]
smoking_locs = np.empty((2,len(sm_time_posix)))

for i in range(0, len(sm_time_posix)):
    ind = find_nearest(time_posix, sm_time_posix[i])
    smoking_locs[0, i] = lat[int(ind)]
    smoking_locs[1, i] = lon[int(ind)]

# Sort data using timestamps
srt = time_posix.argsort()
time_posix = time_posix[srt]
print(time_posix)
lat = lat[srt]
lon = lon[srt]

# for i in range(1, len(lat)):
#     print(getSpeed(time_posix[i-1], time_posix[i], (lat[i-1], lon[i-1]), (lat[i], lon[i])))


print(sm_time_posix)

# Do sin cos transformation
# x = np.array([])
# y = np.array([])
# z = np.array([])
# tX = np.array([])
# tY = np.array([])
# tZ = np.array([])
# for i in range(0, lat.size):
    # x = np.append(x, np.array(math.cos(lat[i]) * math.cos(lon[i])))
    # y = np.append(y, np.array(math.cos(lat[i]) * math.sin(lon[i])))
    # z = np.append(z, np.array(math.sin(lat[i])))
    # tX = np.append(x, np.array(math.cos(time_posix[i]) * math.cos(time_posix[i])))
    # tY = np.append(y, np.array(math.cos(time_posix[i]) * math.sin(time_posix[i])))
    # tZ = np.append(z, np.array(math.sin(time_posix[i])))


# Normalize!
# minX = np.amin(x)
# maxX = np.amax(x)
# minY = np.amin(y)
# maxY = np.amax(y)
# minZ = np.amin(z)
# maxZ = np.amax(z)
# minTX = np.amin(tX)
# maxTX = np.amax(tX)
# minTY = np.amin(tY)
# maxTY = np.amax(tY)
# minTZ = np.amin(tZ)
# maxTZ = np.amax(tZ)

# xNorm = np.array([])
# yNorm = np.array([])
# zNorm = np.array([])
# tNorm = np.array([])
# tXNorm = np.array([])
# tYNorm = np.array([])
# tZNorm = np.array([])

# for i in range(0, x.size):
#     xNorm = np.append(xNorm, np.array((x[i]-minX)/(maxX-minX)))
#     yNorm = np.append(yNorm, np.array((y[i]-minY)/(maxY-minY)))
#     zNorm = np.append(zNorm, np.array((z[i]-minZ)/(maxZ-minZ)))
    # tXNorm = np.append(tXNorm, np.array((tX[i]-minTX)/(maxTX-minTX)))
    # tYNorm = np.append(tYNorm, np.array((tY[i]-minTY)/(maxTY-minTY)))
    # tZNorm = np.append(tZNorm, np.array((tZ[i]-minTZ)/(maxTZ-minTZ)))
# print(time_posix)
# X = np.vstack((xNorm, yNorm, zNorm)).T
# X = np.vstack((xNorm, yNorm, zNorm, tXNorm, tYNorm, tZNorm)).T
X = np.vstack((lat, lon)).T



if(alg == A_KMEANS):
    #############################################################################
    # Compute clustering with k-means

    from sklearn.cluster import KMeans
    from sklearn import cluster, datasets


    n = 10  # k

    # The following bandwidth can be automatically detected using

    km = KMeans(n_clusters=n, random_state=0)
    km.fit(X)
    labels = km.labels_
    cluster_centers = km.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)

    ############################################################################
    # Plot k-means result

    from itertools import cycle
    plt.figure(1)
    plt.clf()
    max_sm_events = 0
    for k in range(n_clusters_):
        smoking = 0
        my_members = labels == k
        for j in range (0, len(sm_time_posix)):
            if smoking_locs[0, i] in X[my_members, 0] and smoking_locs[1, i] in X[my_members, 1]:
                smoking = smoking + 1
        if smoking > max_sm_events:
            max_sm_events = smoking
            print(max_sm_events)

    colors = 'kbgrcmybgrcmybgrcmybgrcmy'
    for k in range(n_clusters_):
        # if k has smoking event:
        #     col = 'r'
        # else:
        #     col = 'k'
        smoking = 0
        my_members = labels == k
        for j in range (0, len(sm_time_posix)):
            if smoking_locs[0, i] in X[my_members, 0] and smoking_locs[1, i] in X[my_members, 1]:
                smoking = smoking + 1
        

        red = str(hex(255 * int(smoking / max_sm_events)))[2:]
        while len(red) < 2:
            red = "0" + red
        col = "#" + red + "0000"
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], color=col, marker='.', linestyle = 'None')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=4)
    plt.title('Number of clusters: %d' % n_clusters_)
    plt.savefig('graph.png')

elif(alg == A_MEANSHIFT):

    #############################################################################
    # Compute clustering with MeanShift

    from sklearn.cluster import MeanShift, estimate_bandwidth
    from sklearn import cluster, datasets

    # The following bandwidth can be automatically detected using
    # quantile 0.1 is good
    bandwidth = estimate_bandwidth(X, quantile=0.1, n_jobs=-1)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)

    ############################################################################
    # Plot MeanShift result

    
    # from itertools import cycle

    # plt.figure(1)
    # plt.clf()

    # colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # for k, col in zip(range(n_clusters_), colors):
    #     my_members = labels == k
    #     cluster_center = cluster_centers[k]
    #     plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #             markeredgecolor='k', markersize=14)
    # plt.title('K clusters: %d' % n_clusters_)
    # plt.show()

    plt.figure(1)
    plt.clf()
    max_sm_events = 0
    for k in range(n_clusters_):
        smoking = 0
        my_members = labels == k
        for j in range (0, len(sm_time_posix)-1):
            if smoking_locs[0, j] in X[my_members, 0] and smoking_locs[1, j] in X[my_members, 1]:
                smoking = smoking + 1
        if smoking > max_sm_events:
            max_sm_events = smoking
            print("Max smoking events per cluster", max_sm_events)

    colors = 'kbgrcmybgrcmybgrcmybgrcmy'
    for k in range(n_clusters_):
        # if k has smoking event:
        #     col = 'r'
        # else:
        #     col = 'k'
        smoking = 0
        my_members = labels == k
        for j in range (0, len(sm_time_posix)):
            if smoking_locs[0, j] in X[my_members, 0] and smoking_locs[1, j] in X[my_members, 1]:
                smoking = smoking + 1
        

        red = str(hex(255 * int(smoking / max_sm_events)))[2:]
        while len(red) < 2:
            red = "0" + red
        col = "#" + red + "0000"
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], color=col, marker='.', linestyle = 'None')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=4)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.savefig('graph.png')
