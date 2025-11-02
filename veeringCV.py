import numpy as np
import h5py
import matplotlib.pyplot as plt
from contourpy.array import split_points_at_nan
#import faiss
from sklearn.cluster import KMeans
#from sklearnex import patch_sklearn
#patch_sklearn()
from scipy.spatial import distance
from scipy.signal import find_peaks
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from scipy.interpolate import UnivariateSpline
import logging

class VeeringNormalisation:
    def __init__(self, filePath):
        self.filePath = filePath
        self.pixcels = "empty"
        self.origShape = "empty"
        self.normalisation = []
        self.pixcelLength = 'empty'
        self.targetImages_ind = []
        self.normedStats = []
        self.timestamps = 'empty'
        self.params = 'empty'

    def Calc_Pixcel_Length(self):
        self.pixcelLength = np.power(np.power(self.pixcels[:,0,:],2)+
                                np.power(self.pixcels[:,1,:],2)+
                                np.power(self.pixcels[:,2,:],2)
                                ,1/2)


    def Get_Pixcels(self):
        dataIn = h5py.File(self.filePath, 'r')
        pixcels = np.array(dataIn['IMG_ARRAY'], dtype='float32')
        origShape = np.shape(pixcels)
        pixcels = np.reshape(pixcels, (-1,origShape[2],origShape[3]), order='F')
        pixcels = pixcels + .00000001
        self.pixcels = pixcels
        self.origShape = origShape
        self.timestamps = np.array(dataIn['TIME_STAMPS'])
        #self.params = np.array(dataIn['VSP_PARAMS'])

    def Get_Target_Images(self):
        self.targetImages_ind.append(np.argmin(np.mean(self.pixcelLength, axis=0)))
        self.targetImages_ind.append(np.argmax(np.mean(self.pixcelLength, axis=0)))
        self.targetImages_ind.append(np.argmin(np.std(self.pixcelLength, axis=0)))
        self.targetImages_ind.append(np.argmax(np.std(self.pixcelLength, axis=0)))
        self.targetImages_ind.append(np.argmin(np.mean(self.pixcels[:,0,:], axis=0)))
        self.targetImages_ind.append(np.argmax(np.mean(self.pixcels[:,0,:], axis=0)))
        self.targetImages_ind.append(np.argmin(np.mean(self.pixcels[:,1,:], axis=0)))
        self.targetImages_ind.append(np.argmax(np.mean(self.pixcels[:,1,:], axis=0)))
        self.targetImages_ind.append(np.argmin(np.mean(self.pixcels[:,2,:], axis=0)))
        self.targetImages_ind.append(np.argmax(np.mean(self.pixcels[:,2,:], axis=0)))

    def Normalise(self, dataSet, mean_actual, mean_target, std_actual, std_target):
        std_multiplier = std_target/std_actual
        mean_offset = dataSet - mean_actual
        mean_offset = mean_offset * std_multiplier
        dataSet_normed = mean_target + mean_offset
        dataSet_normed_multiplier = dataSet_normed / dataSet
        return dataSet_normed_multiplier
##1

    def Length_normalise(self):
        self.Calc_Pixcel_Length()
        imgMean_length = np.mean(self.pixcelLength, axis=0)
        imgStd_length = np.std(self.pixcelLength, axis=0)
        setMean_length = np.mean(self.pixcelLength)
        setStd_length = np.std(self.pixcelLength)
        std_multiplier = setStd_length/imgStd_length
        mean_offset = self.pixcelLength-imgMean_length
        mean_offset = mean_offset * std_multiplier
        pixcelLength_normed = setMean_length + mean_offset
        pixcelLength_normed_multiplier = pixcelLength_normed/self.pixcelLength
        for i in [0,1,2]:
            self.pixcels [:,i,:] = self.pixcels [:,i,:] * pixcelLength_normed_multiplier

##2
    def Colour_Normed(self):
        imgMean_red = np.mean(self.pixcels[:,0,:], axis=0)
        setMean_red = np.mean(self.pixcels[:,0,:])
        imgMean_green = np.mean(self.pixcels[:,1,:], axis=0)
        setMean_green = np.mean(self.pixcels[:,1,:])
        imgMean_blue = np.mean(self.pixcels[:,2,:], axis=0)
        setMean_blue = np.mean(self.pixcels[:,2,:])

        imgStd_red = np.std(self.pixcels[:,0,:], axis=0)
        setStd_red = np.std(self.pixcels[:,0,:])
        imgStd_green = np.std(self.pixcels[:,1,:], axis=0)
        setStd_green = np.std(self.pixcels[:,1,:])
        imgStd_blue = np.std(self.pixcels[:,2,:], axis=0)
        setStd_blue = np.std(self.pixcels[:,2,:])
        red_norm_multiplier = self.Normalise(self.pixcels[:,0,:], imgMean_red, setMean_red, imgStd_red, setStd_red)
        green_norm_multiplier = self.Normalise(self.pixcels[:,1,:], imgMean_green, setMean_green, imgStd_green, setStd_green)
        blue_norm_multiplier = self.Normalise(self.pixcels[:,0,:], imgMean_blue, setMean_blue, imgStd_blue, setStd_blue)
        self.pixcels[:,0,:] = self.pixcels[:,0,:] * red_norm_multiplier
        self.pixcels[:,1,:] = self.pixcels[:,1,:] * green_norm_multiplier
        self.pixcels[:,2,:] = self.pixcels[:,2,:] * blue_norm_multiplier


##3

    def RGB_Chrom_Normalise(self):
        pixcels_sum  = np.sum(self.pixcels ,axis=1)
        for i in [0,1,2]:
            self.pixcels [:,i,:] = (self.pixcels[:,i,:]/pixcels_sum)*255

    def Calc_Normed_Properties(self):
        self.Calc_Pixcel_Length()
        self.normedStats.append(np.mean(self.pixcelLength))
        self.normedStats.append(np.std(self.pixcelLength))
        self.normedStats.append(np.std(np.mean(self.pixcelLength, axis=0)))

    def RunNormalisation(self, normTypes):
        self.Get_Pixcels()
        self.Calc_Pixcel_Length()
        self.Get_Target_Images()

        for normType in normTypes:

            if normType == 0:
                self.normalisation.append('None')

            elif normType == 1:
                self.Length_normalise()
                self.normalisation.append('Length Normal')

            elif normType == 2:
                self.Colour_Normed()
                self.normalisation.append('Colour Normal')

            elif normType == 3:
                self.RGB_Chrom_Normalise()
                self.normalisation.append('RGB Chromacity')

        self.Calc_Normed_Properties()

class PlotArray:
    def __init__(self,pixcels, originalShape, indices, order='F'):
        self.pixcels = pixcels
        self.origShape = originalShape
        self.indicies = indices
        self.order = order

    def Convert_to_Image(self):
        self.pixcels = np.array(np.reshape(self.pixcels, self.origShape, self.order), dtype='int')
        self.pixcels = self.pixcels[:,:,:,self.indicies]
        self.pixcels = np.clip(self.pixcels, 0, 255)

    def Save_Image(self, path, subIndicies, fileType='.jpg'):
        for n in subIndicies:
            plt.imshow(self.pixcels[:,:,:,n])
            plt.savefig(str(path)+str(n)+str(fileType))

    def Save_Array(self, path):
        np.save(path, self.pixcels)

class VeeringClustering_vSp:
    def __init__(self, filePath, initialClusters, iterations):
        self.importPath = filePath
        self.features = 'Empty'
        self.vSpParams = 'Empty'
        self.clusteringMethod = 'faiss'
        self.clusteringScope = 'set'
        self.cluster_labels = 'Empty'
        self.cluster_Centroids = 'Empty'
        self.cluster_vSpID = ['Empty,Empty']
        self.cluster_stats = []
        self.initialClusters = initialClusters
        self.iterations = iterations
        self.clusterCount_FAISS = 'Empty'

    def Import_Features(self):
        dataIn = h5py.File(self.importPath, 'r')
        self.features = np.array(dataIn['PIXCELS_NORM'], dtype='float32')
        self.vSpParams = np.array(dataIn['VSP_PARAMS'])

    def Get_Clusters_FAISS(self):
        smallestCluster_size = self.features.shape[0]
        markerSize_count = self.vSpParams[1]*self.features.shape[0]
        self.clusterCount_FAISS = self.initialClusters-1

        while markerSize_count < smallestCluster_size:
            self.clusterCount_FAISS += 1
            kmeans = faiss.Kmeans(self.features.shape[1], self.clusterCount_FAISS, niter=self.iterations, verbose=True, gpu=True)
            kmeans.train(self.features)

            pixcelCount_perCluster = np.unique(I, return_counts=True)
            markerCluster = np.where(pixcelCount_perCluster[1]== pixcelCount_perCluster[1].min())
            smallestCluster_size = pixcelCount_perCluster[markerCluster]
            self.cluster_vSpID[0] = markerCluster

            if smallestCluster_size < 0.5*markerSize_count:
                markerSize_count = markerSize_count*1.15
                self.clusterCount_FAISS = self.initialClusters
                smallestCluster_size = self.features.shape[0]

        D,I = kmeans.index.search(self.features,1)
        self.cluster_labels = I
        self.cluster_Centroids = kmeans.centroids

        def Get_Clusters_SCI(self):
            kmeans = KMeans(init = self.cluster_Centroids, n_clusters=self.clusterCount_FAISS, max_iter=self.iterations, verbose=1, n_init=10).fit(self.features)
            self.cluster_labels= kmeans.labels_
            self.cluster_Centroids = kmeans.cluster_centers_

        def Clustering(self):
            self.features = np.reshape(self.features, (-1,self.features.shape[1]))
            self.Get_Clusters_FAISS()

            if self.clusteringMethod == 'SKlearn':
                self.Get_Clusters_SCI()

        def Run_Clustering(Self, method, scope):
            self.clusteringMethod = method
            self.clusteringScope = scope

            if self.clusteringScope == 'set':
                self.Clustering()

class Thresholding:
    def __init__(self, pixcels, targetColour, searchRange):
        self.threshPix = pixcels
        self.targetColour = np.array(targetColour, dtype='float32')
        self.originalShape = np.shape(pixcels)
        self.searchRange = searchRange

    def Reshape_Flat(self):
        self.threshPix = np.reshape(np.moveaxis(self.threshPix,[2],[1]),(-1,3))

    def Calc_Distances(self):
        self.eucledianDistances = np.linalg.norm(self.targetColour - self.threshPix, axis=1)


    def Calc_Threshold(self):
        try:
            x_mean = []
            y_mean = []
            search = range(self.searchRange[0], self.searchRange[1], self.searchRange[2])
            for x1 in search:
                x_mean.append(x1)
                y_mean.append(np.mean(self.eucledianDistances[np.where(self.eucledianDistances < x1)]))

            peaks = find_peaks(np.gradient(np.gradient(y_mean))*-1)
            if peaks[0].size == 0:
                peaks = find_peaks(np.gradient(y_mean)*-1)
            if peaks[0].size == 0:
                peaks = find_peaks(y_mean)

            opt_mean = x_mean[peaks[0][0]]

        except Exception as e:
            logging.error(e)
            logging.error('Failed to calculate opt_mean do to ')
            print(e)
            opt_mean = (self.searchRange[0]+self.searchRange[1])/2
        try:
            x_std = []
            y_std = []
            for x1 in search:
                x_std.append(x1)
                y_std.append(np.std(self.eucledianDistances[np.where(self.eucledianDistances < x1)]))

            peaks = find_peaks(np.gradient(np.gradient(y_std)))
            if peaks[0].size == 0:
                peaks = find_peaks(np.gradient(np.gradient(y_std))*-1)
                if peaks[0].size == 0:
                    peaks = find_peaks(np.gradient(y_std))
            if peaks[0].size == 0:
                peaks = find_peaks(y_std)

            opt_std = x_std[peaks[0][0]]

        except Exception as e:
            logging.error(e)
            logging.error('Failed to calculate opt_std do to ')
            print(e)
            opt_std = (self.searchRange[0]+self.searchRange[1])/2

        try:
            x_count = []
            y_count = []
            eucledianDistances = np.reshape(self.eucledianDistances, (-1,self.originalShape[2]))
            for x1 in search:
                x_count.append(x1)
                y_count.append((np.std(np.unique(np.where(eucledianDistances< x1)[1], return_counts=True)[1])))

            peaks = find_peaks(np.gradient(np.gradient(y_count))*-1)
            if peaks[0].size == 0:
                peaks = find_peaks(np.gradient(y_count)*-1)
            if peaks[0].size == 0:
                peaks = find_peaks(y_count)
            opt_count = x_count[peaks[0][0]]
        except Exception as e:
            logging.error(e)
            logging.error('Failed to calculate opt_count do to ')
            print(e)
            opt_count = (self.searchRange[0]+self.searchRange[1])/2

        self.threshold = int(np.mean([opt_mean,opt_std,opt_count]))
        self.graphStats = [x_mean,y_mean, opt_mean, x_std,y_std, opt_std, x_count,y_count, opt_count]

    def Threshold_Graphs(self):
        x_mean = self.graphStats[0]
        y_mean = self.graphStats[1]
        opt_mean = self.graphStats[2]
        x_std = self.graphStats[3]
        y_std = self.graphStats[4]
        opt_std = self.graphStats[5]
        x_count = self.graphStats[6]
        y_count = self.graphStats[7]
        opt_count = self.graphStats[8]

        self.thesholdFigure, self.axes = plt.subplots(3,3,figsize=(10,6))
        self.thesholdFigure.suptitle('Pixcel Threshold Selection' +'\n' + 'Threshold: ' + str(self.threshold))
        self.axes[0,0].plot(x_mean,y_mean)
        self.axes[0,0].vlines(opt_mean,min(y_mean),max(y_mean),colors='red')
        self.axes[1,0].plot(x_mean,np.gradient(y_mean))
        self.axes[1,0].vlines(opt_mean,min(np.gradient(y_mean)),max(np.gradient(y_mean)),colors='red')
        self.axes[2,0].plot(x_mean,np.gradient(np.gradient(y_mean)), color='orange')
        self.axes[2,0].vlines(opt_mean,min(np.gradient(np.gradient(y_mean))),max(np.gradient(np.gradient(y_mean))),colors='red')
        self.axes[0,0].set_title('Mean of Distance of Eucledian Points')

        self.axes[0,1].plot(x_std,y_std)
        self.axes[0,1].vlines(opt_std,min(y_std),max(y_std),colors='red')
        self.axes[1,1].plot(x_std,np.gradient(y_std))
        self.axes[1,1].vlines(opt_std,min(np.gradient(y_std)),max(np.gradient(y_std)),colors='red')
        self.axes[2,1].plot(x_std,np.gradient(np.gradient(y_std)), color='orange')
        self.axes[2,1].vlines(opt_std,min(np.gradient(np.gradient(y_std))),max(np.gradient(np.gradient(y_std))),colors='red')
        self.axes[0,1].set_title('SD of Distance of Eucledian Points')

        self.axes[0,2].plot(x_count,y_count)
        self.axes[0,2].vlines(opt_count,min(y_count),max(y_count), colors='red')
        self.axes[1,2].plot(x_count,np.gradient(y_count))
        self.axes[1,2].vlines(opt_count,min(np.gradient(y_count)),max(np.gradient(y_count)), colors='red')
        self.axes[2,2].plot(x_count,np.gradient(np.gradient(y_count)),color='orange')
        self.axes[2,2].vlines(opt_count,min(np.gradient(np.gradient(y_count))),max(np.gradient(np.gradient(y_count))), colors='red')
        self.axes[0,2].set_title('SD of Pixcel Count per Image')

    def Run_Thresholding(self):
        self.Reshape_Flat()
        self.Calc_Distances()
        self.Calc_Threshold()

    def Threshold_Sweep_Graphs(self, offsets, origShape, pixels):
        self.pixels = pixels
        thresh_offset = offsets
        self.thresh_offsetPlot, self.axes = plt.subplots(1, len(thresh_offset), figsize=(30, 5))
        for i in range(len(thresh_offset)):
            threshPix = np.copy(self.pixels)
            thresh_shape = threshPix.shape
            threshPix = np.moveaxis(threshPix, [2], [1])
            threshPix = np.reshape(threshPix, (-1, 3), order='F')
            eucledianDistances = np.linalg.norm(self.targetColour - threshPix, axis=1)
            eucledianDistances = np.reshape(eucledianDistances, (thresh_shape[0], thresh_shape[2]), order='F')
            eucledianDistances = np.reshape(eucledianDistances,
                                            (origShape[0], origShape[1], origShape[3]),
                                            order='F')
            stripes = np.transpose(np.asarray(np.where(eucledianDistances[:, :, :] < (self.threshold + thresh_offset[i]))))
            self.axes[i].plot(stripes[:, 1], stripes[:, 0], 'o', markersize=.1, color='blue')
            self.axes[i].set_title('Threshhold = ' + str(self.threshold + thresh_offset[i]) + '\n' + 'Threshold Offset = ' + str(
                thresh_offset[i]))

    def Generate_Stripe_Pixcels(self,thresholdOffset,pixcels, origShape):
        self.threshold_offset = thresholdOffset
        self.threshold = self.threshold + self.threshold_offset
        self.threshPix = pixcels
        thresh_shape = self.threshPix.shape
        self.threshPix = np.moveaxis(self.threshPix, [2], [1])
        self.threshPix = np.reshape(self.threshPix, (-1, 3), order='F')
        eucledianDistances = np.linalg.norm(self.targetColour - self.threshPix, axis=1)
        eucledianDistances = np.reshape(eucledianDistances, (thresh_shape[0], thresh_shape[2]), order='F')
        eucledianDistances = np.reshape(eucledianDistances,
                                        (origShape[0], origShape[1], origShape[3]),
                                        order='F')
        self.stripes = np.transpose(np.asarray(np.where(eucledianDistances[:, :, :] < self.threshold)))

    def Count_Filter(self, lowerBound, upperBound):
        self.lowerBound_quantile = lowerBound
        self.upperBound_quantile = upperBound
        self.lowerBound = np.quantile(np.unique(self.stripes[:, 2], return_counts=True)[1], self.lowerBound_quantile)
        self.upperBound = np.quantile(np.unique(self.stripes[:, 2], return_counts=True)[1], self.upperBound_quantile)
        self.countFilter_ind = np.where(np.all([[np.unique(self.stripes[:, 2], return_counts=True)[1] < self.upperBound],
                                           [np.unique(self.stripes[:, 2], return_counts=True)[1] > self.lowerBound]], axis=0))[1]
        stripesInd = np.empty([1], dtype='uint8')
        for i in self.countFilter_ind:
            stripesInd = np.concatenate((stripesInd, np.where(self.stripes[:, 2] == i)[0]), axis=0)
        self.stripesInd = stripesInd[1:]
        self.stripes = self.stripes[stripesInd,:]

    def Cnt_Filter_Plot(self):
        self.cnt_filterFig, self.axes = plt.subplots(2, 1, figsize=(5, 10))
        self.axes[0].hist(np.unique(self.stripes[:, 2], return_counts=True)[1])
        self.axes[0].set_title("Count of pixcels per image" + "\n" +
                          "Lower Bound Quantile = " + str(self.lowerBound_quantile) + "\n"
                                                                                 "Upper Bound Quantile = " + str(
            self.upperBound_quantile))
        self.axes[0].vlines(self.lowerBound, 0, int(np.unique(self.stripes[:, 2], return_counts=True)[0].max() * 0.25), color='red')
        self.axes[0].vlines(self.upperBound, 0, int(np.unique(self.stripes[:, 2], return_counts=True)[0].max() * 0.25), color='red')
        self.axes[1].boxplot(np.unique(self.stripes[:, 2], return_counts=True)[1], vert=False)
        self.axes[1].vlines(self.lowerBound, 0.5, 1.5, color='red')
        self.axes[1].vlines(self.upperBound, 0.5, 1.5, color='red')

    def Stripes_Plot_Clean(self):
        self.CNT_cleanPlot, self.axes = plt.subplots(1, 1, figsize=(3,3))
        self.axes.plot(self.stripes[:, 1], self.stripes[:, 0], 'o', markersize=.1, color='blue')


class Set_DB:
    def __init__(self, stripes, multipliers, countFilter_ind, clusterOffset):
        self.stripes = stripes
        self.set_eps_multiplier = multipliers[0]
        self.set_min_multiplier = multipliers[1]
        self.countFilter_ind = countFilter_ind
        self.clusterOffset = clusterOffset

    def Set_PCA_DB(self):
        pca = PCA(n_components=2)

        pca.fit(self.stripes[:, 0:2])
        self.stripes_rot = pca.transform(self.stripes[:, 0:2])
        self.setRotation_matrix = pca.components_
        self.setRotation_degrees = np.degrees(np.arccos(self.setRotation_matrix[0, 0]))
        self.setCluster_eps = int((self.stripes_rot[:, 0].max() - self.stripes_rot[:, 0].min()) * self.set_eps_multiplier)

        if self.setCluster_eps < 2:
            self.setCluster_eps = 2
        self.setCluster_min = int((self.stripes_rot.shape[0] / self.countFilter_ind.shape[0]) * self.set_min_multiplier)
        if self.setCluster_min < 2:
            self.setCluster_min = 2

        self.stripes_rot_clus, self.inv = np.unique(self.stripes_rot, axis=0, return_inverse=True)
        self.stripe_clusters_set = DBSCAN(eps=self.setCluster_eps, min_samples=self.setCluster_min).fit(self.stripes_rot_clus)
        self.cluster_counts = np.unique(self.stripe_clusters_set.labels_[self.inv], return_counts=True)
        self.cluster_counts = np.array([self.cluster_counts[1], self.cluster_counts[0]])
        self.cluster_counts_sorted = np.sort(self.cluster_counts)

        if (self.cluster_counts_sorted[0].max() / self.cluster_counts_sorted.sum()) > 0.98:
            self.cluster_count_cutoff = np.where(self.cluster_counts_sorted[0] == self.cluster_counts_sorted[0].max())[0]
            self.cluster_count_cutoff = int(self.cluster_count_cutoff)
            self.cluster_cutoff_by = 'Percentage'

        else:
            self.cluster_count_cutoff = np.where(np.gradient(self.cluster_counts_sorted[0][:-1]) == np.gradient(self.cluster_counts_sorted[0][:-1]).max())[0][-1]
            self.cluster_count_cutoff = int(self.cluster_count_cutoff)
            self.cluster_cutoff_by = 'Gradient'

        if self.cluster_count_cutoff < 0:
            self.cluster_count_cutoff = 0

        self.cluster_count_cutoff = self.cluster_count_cutoff + int(self.clusterOffset)
        self.cluster_filter = self.cluster_counts[0] >= self.cluster_counts_sorted[0, self.cluster_count_cutoff]
        self.cluster_filter = self.cluster_counts[1, self.cluster_filter]

        self.pca = pca

    def Cluster_Filter_FIG(self):
        self.cluster_filterFig, axes = plt.subplots(4, 1, figsize=(5, 15))
        axes[0].plot(self.cluster_counts_sorted[1], self.cluster_counts_sorted[0])
        axes[0].vlines(self.cluster_count_cutoff - 1, min(self.cluster_counts_sorted[0]), max(self.cluster_counts_sorted[0]),
                       colors='red')
        axes[0].set_title("Count of pixcels per cluster" + "\n" +
                          "cluster offset = " + str(self.clusterOffset) + "\n" +
                          "cluster Cutt off = " + str(self.cluster_count_cutoff - 1) + "\n" +
                          "Cut of set by - " + self.cluster_cutoff_by)
        axes[1].plot(self.cluster_counts_sorted[1], np.gradient(self.cluster_counts_sorted[0]), color='orange')
        axes[1].vlines(self.cluster_count_cutoff - 1, min(np.gradient(self.cluster_counts_sorted[0])),
                       max(np.gradient(self.cluster_counts_sorted[0])), colors='red')
        axes[2].plot(self.cluster_counts_sorted[1], np.gradient(np.gradient(self.cluster_counts_sorted[0])))
        axes[2].vlines(self.cluster_count_cutoff - 1, min(np.gradient(np.gradient(self.cluster_counts_sorted[0]))),
                       max(np.gradient(np.gradient(self.cluster_counts_sorted[0]))), colors='red')
        axes[3].plot(self.cluster_counts_sorted[1], np.gradient(np.gradient(np.gradient(self.cluster_counts_sorted[0]))))
        axes[3].vlines(self.cluster_count_cutoff - 1, min(np.gradient(np.gradient(np.gradient(self.cluster_counts_sorted[0])))),
                       max(np.gradient(np.gradient(np.gradient(self.cluster_counts_sorted[0])))), colors='red')

    def Cluster_Plot_FIG(self):
        self.cluster_Plot, axes = plt.subplots(1, 2, figsize=(15, 5))
        colours = ['tab:blue', 'tab:green', 'tab:red', 'tab:orange', 'tab:pink', 'tab:purple', 'tab:yellow', 'tab:cyan',
                   'tab:magenta', ]
        bar_colours = []
        n = 0
        for i in np.unique(self.stripe_clusters_set.labels_):
            if i in self.cluster_filter:
                axes[0].plot(self.stripes_rot[np.where(self.stripe_clusters_set.labels_ == i)][:, 1],
                             self.stripes_rot[np.where(self.stripe_clusters_set.labels_ == i)][:, 0], 'o', markersize=.1,
                             color=colours[n])
                bar_colours.append(colours[n])
                n += 1
            else:
                axes[0].plot(self.stripes_rot[np.where(self.stripe_clusters_set.labels_ == i)][:, 1],
                             self.stripes_rot[np.where(self.stripe_clusters_set.labels_ == i)][:, 0], '*', color='black')
                bar_colours.append('black')
        axes[0].set_title('Stripes by Cluster')
        axes[1].bar(np.unique(self.stripe_clusters_set.labels_, return_counts=True)[0],
                    np.unique(self.stripe_clusters_set.labels_, return_counts=True)[1], color=bar_colours)
        axes[1].set_xticks(np.unique(self.stripe_clusters_set.labels_, return_counts=True)[0])
        axes[1].set_yscale('log')
        axes[1].grid(color='grey', which='major', linestyle=':', axis='y')
        axes[1].set_title('Pixcel count by cluster')

    def Make_DB_Scan_Set(self):
        toKeep = []
        print(len(self.cluster_filter))
        for i in range(len(self.cluster_filter)):
            print(i)
            toKeep.append(list(np.where(self.stripe_clusters_set.labels_[self.inv] == self.cluster_filter[i])[0]))

        toKeep = [item for sublist in toKeep for item in sublist]
        self.toKeep = toKeep
        filter = np.sort(toKeep)

        self.filter = filter

        return self.stripes[filter, :], self.pca

class Pic_DB:
    def __init__(self, stripes, setRotation_degrees, set_pca):
        self.stripes = stripes
        self.setRotation_degrees = setRotation_degrees
        self.set_pca = set_pca

    def Pic_DB_Scan(self, sample, plotSamples, pic_eps_multiplier, pic_min_multiplier):

        clusterPoints_dict = {}
        if sample:
            step = int(np.unique(self.stripes[:, 2]).size / plotSamples)
            plotIndex = []
            i = 0
            for i in range(plotSamples):
                plotIndex.append(int(i * step))

            sample_plot_images = np.unique(self.stripes[:, 2])[plotIndex]
        else:
            sample_plot_images = np.unique(self.stripes[:, 2])

        if sample:
            sample_images_cluster_fig, axes = plt.subplots(sample_plot_images.size, 1,
                                                           figsize=(5, sample_plot_images.size * 5))

        for n in range(sample_plot_images.size):
            i = sample_plot_images[n]
            stripes_pic = np.where(self.stripes[:, 2] == i)[0]
            stripes_pic = self.stripes[stripes_pic, 0:2]
            stripes_rot = self.set_pca.transform(stripes_pic)

            pca_pic = PCA(n_components=2).fit(stripes_pic)
            picRotation = np.degrees(np.arccos(pca_pic.components_[0, 0]))

            pic_eps = int((stripes_pic[:, 0].max() - stripes_pic[:, 0].min()) * pic_eps_multiplier)
            if pic_eps < 2:
                pic_eps = 2
            pic_min = int(stripes_pic.size * pic_min_multiplier)
            if pic_min < 2:
                pic_min = 2

            stripe_clusters = DBSCAN(eps=pic_eps, min_samples=pic_min).fit(stripes_rot)

            cluster_points = []
            for cluster in np.unique(stripe_clusters.labels_):
                if cluster > -1:
                    points = stripes_rot[np.where(stripe_clusters.labels_ == cluster)[0], :]
                    cluster_points.append(points)
                clusterPoints_dict[i] = cluster_points

            if sample:
                for i in np.unique(stripe_clusters.labels_):
                    if i > -1:
                        axes[n].scatter(stripes_rot[np.where(stripe_clusters.labels_ == i)][:, 1],
                                        stripes_rot[np.where(stripe_clusters.labels_ == i)][:, 0])
                    else:
                        axes[n].scatter(stripes_rot[np.where(stripe_clusters.labels_ == i)][:, 1],
                                        stripes_rot[np.where(stripe_clusters.labels_ == i)][:, 0], marker='*',
                                        color='black')

                axes[n].set_title('Image No. ' + str(sample_plot_images[n]) + '\n' +
                                  'Image Rotation = ' + str(np.abs(picRotation - self.setRotation_degrees)) + '\n' +
                                  'Pic Eps = ' + str(pic_eps) + ' -- Pic Min = ' + str(pic_min))
                axes[n].set_xticks([])
                axes[n].set_yticks([])

        self.clusterPoints_dict = clusterPoints_dict


class Fit_Spline_Calc:
    def __init__(self, clusterPoints_dict, origShape, setPCA):
        self.clusterPoints_dict = clusterPoints_dict
        self.origShape = origShape
        self.setPCA = setPCA

    def Fit_Splines(self, plotSpline,  linearInterp_threshold_multiplier, minPoint_filter, weightsFilter_quantile,):
        self.linearInterp_threshold_multiplier = linearInterp_threshold_multiplier
        self.minPoint_filter = minPoint_filter
        self.weightsFilter_quantile = weightsFilter_quantile

        splines_set = {}
        points_to_fit_weights = {}

        for pic in self.clusterPoints_dict.keys():
            splines_set[pic] = []
            points_to_fit_weights[pic] = []

            for i in range(len(self.clusterPoints_dict[pic])):
                points_to_fit = self.clusterPoints_dict[pic][i]
                x = points_to_fit[:, 0]
                y = points_to_fit[:, 1]
                x_unique = np.arange(int(np.min(x)), int(np.max(x)), 1)
                y_unique = []
                y_min_plot = []
                y_max_plot = []
                weights = []
                for val in x_unique:

                    ind = np.where(np.all([[x > val - 0.49], [x < val + 0.51]], axis=0))[1]
                    y_sample = y[ind]
                    if y_sample.size == 0:
                        y_median = 0
                        weight = 0
                        y_min = 0
                        y_max = 0

                    else:
                        y_min = np.min(y_sample)
                        y_max = np.max(y_sample)
                        y_range = (y_max - y_min) + 1
                        weight = y_sample.size / y_range
                        y_median = np.median(y_sample)

                    if weight > 1:
                        weight = 1
                    y_unique.append(y_median)
                    weights.append(weight)
                    y_min_plot.append(y_min)
                    y_max_plot.append(y_max)
                weights = np.asarray(weights)

                weightsFilter_limit = np.quantile(weights[np.where(weights > 0)[0]], weightsFilter_quantile)

                if weightsFilter_limit == 1:
                    weightsFilter_limit = 0.99

                weightsFiltered = np.where(weights >= weightsFilter_limit, weights, np.zeros_like(weights))
                if x_unique.shape[0] > minPoint_filter:
                    if x_unique.shape[0] > self.origShape[0] * linearInterp_threshold_multiplier:
                        spline = UnivariateSpline(x_unique, y_unique, w=weights, s=len(weights))

                    else:
                        spline = UnivariateSpline(x_unique, y_unique, w=weights, s=len(weights), k=1)

                    spline = [spline, int(np.min(x)), int(np.max(x))]
                    splines_set[pic].append(spline)
                    points_to_fit_weights[pic].append([x_unique, y_unique, weights])

                if plotSpline:
                    plot_x = np.arange(np.min(x_unique), np.max(x_unique), 1)
                    plot_y = spline[0](plot_x)

                    weights_filterPlot, axes = plt.subplots(3, len(self.clusterPoints_dict[pic]),
                                                            figsize=(5 * len(self.clusterPoints_dict[pic]), 15))
                    axes[0, i].hist(weights)
                    axes[0, i].set_yscale('log')
                    axes[0, i].vlines(weightsFilter_limit, 0, 10, colors='r')
                    axes[0, i].set_title("Cluster # " + str(i) + '\n'
                                                                 'weightFilter_limit = ' + str(weightsFilter_limit))
                    axes[1, i].hist(weightsFiltered[np.where(weightsFiltered > 0)[0]])
                    axes[1, i].set_yscale('log')
                    axes[1, i].vlines(weightsFilter_limit, 0, 10, colors='r')
                    axes[2, i].plot(plot_x, plot_y, color='b')
                    axes[2, i].plot(x_unique, y_min_plot, 'o', markersize=0.2, color='red')
                    axes[2, i].plot(x_unique, y_max_plot, 'o', markersize=0.2, color='green')

                self.splines_set = splines_set
                self.points_to_fit_weights = points_to_fit_weights

    def Link_Splines(self,plotSpline, splineWalkDist, gradTollerance, posTolerance):
        self.splineWalkDist = splineWalkDist
        self.gradTollerance = gradTollerance
        self.posTolerance = posTolerance

        clustersToJoin_set = {}
        splines_set = self.splines_set
        points_to_fit_weights = self.points_to_fit_weights

        if plotSpline:
            splinesWalk_plot, axes = plt.subplots(len(splines_set.keys()), 3,
                                                  figsize=(15, 5 * len(splines_set.keys())))

        for i in range(len(splines_set.keys())):
            pic = list(splines_set.keys())[i]
            clustersToJoin = []
            splines = splines_set[pic]

            if plotSpline:
                for spline in splines:
                    plot_x = np.arange(spline[1], spline[2], 1)
                    plot_y = spline[0](plot_x)
                    axes[i, 0].plot(plot_y, plot_x)
                    axes[i, 0].set_title("i = " + str(i) + "\n" + "key = " + str(pic))

                for spline in splines:
                    plot_x_walk = np.arange(spline[1] - splineWalkDist, spline[2] + splineWalkDist, 1)
                    plot_y_walk = spline[0](plot_x_walk)
                    axes[i, 1].plot(plot_y_walk, plot_x_walk)
                    axes[i, 1].set_title("i = " + str(i) + "\n" + "key = " + str(pic))

            for n in range((len(splines_set[pic]))):
                for m in range(n, (len(splines_set[pic]))):
                    if n != m:

                        x_min = np.min(
                            [splines_set[pic][n][1] - splineWalkDist, splines_set[pic][n][2] + splineWalkDist,
                             splines_set[pic][n][1] - splineWalkDist, splines_set[pic][n][2] + splineWalkDist])
                        x_max = np.max(
                            [splines_set[pic][n][1] - splineWalkDist, splines_set[pic][n][2] + splineWalkDist,
                             splines_set[pic][n][1] - splineWalkDist, splines_set[pic][n][2] + splineWalkDist])
                        x1_min = np.min(
                            [splines_set[pic][n][1] - splineWalkDist, splines_set[pic][n][2] + splineWalkDist])
                        x1_max = np.max(
                            [splines_set[pic][n][1] - splineWalkDist, splines_set[pic][n][2] + splineWalkDist])
                        x2_min = np.min(
                            [splines_set[pic][m][1] - splineWalkDist, splines_set[pic][m][2] + splineWalkDist])
                        x2_max = np.max(
                            [splines_set[pic][m][1] - splineWalkDist, splines_set[pic][m][2] + splineWalkDist])
                        # x1 = np.arange(x1_min,x1_max,posTolerance)
                        # x2 = np.arange(x2_min,x2_max,posTolerance)
                        x = np.arange(x_min, x_max, posTolerance)
                        y1 = splines_set[pic][n][0](x)
                        y2 = splines_set[pic][m][0](x)

                        intersects = np.where(np.abs(y1 - y2) < posTolerance)[0]
                        x_intersects = x[intersects]
                        derivative_1 = splines_set[pic][n][0].derivative()(x_intersects)
                        derivative_2 = splines_set[pic][m][0].derivative()(x_intersects)

                        derivate_dif = derivative_1 / derivative_2

                        if np.any(
                                np.all([[derivate_dif < gradTollerance], [derivate_dif > (1 / gradTollerance)]],
                                       axis=0)):
                            clustersToJoin.append([n, m])

                        print('n = ' + str(n) + ' m = ' + str(m) + ' length = ' + str(intersects.shape))

            clustersToJoin_set[pic] = clustersToJoin

            pairs = clustersToJoin_set[pic]

            toPop = []

            for pair in pairs:
                print(pair)
                newMin = np.min([splines_set[pic][pair[0]][1], splines_set[pic][pair[1]][1]])
                newMax = np.max([splines_set[pic][pair[0]][2], splines_set[pic][pair[1]][2]])

                if points_to_fit_weights[pic][pair[0]][0][0] < points_to_fit_weights[pic][pair[1]][0][0]:
                    newX = np.concatenate(
                        (points_to_fit_weights[pic][pair[0]][0], points_to_fit_weights[pic][pair[1]][0]))
                    newY = np.concatenate(
                        (points_to_fit_weights[pic][pair[0]][1], points_to_fit_weights[pic][pair[1]][1]))
                    newWeights = np.concatenate(
                        (points_to_fit_weights[pic][pair[0]][2], points_to_fit_weights[pic][pair[1]][2]))
                elif points_to_fit_weights[pic][pair[0]][0][0] > points_to_fit_weights[pic][pair[1]][0][0]:
                    newX = np.concatenate(
                        (points_to_fit_weights[pic][pair[1]][0], points_to_fit_weights[pic][pair[0]][0]))
                    newY = np.concatenate(
                        (points_to_fit_weights[pic][pair[1]][1], points_to_fit_weights[pic][pair[0]][1]))
                    newWeights = np.concatenate(
                        (points_to_fit_weights[pic][pair[1]][2], points_to_fit_weights[pic][pair[0]][2]))
                newX = newX[np.unique(newX, return_index=True)[1]]
                newY = newY[np.unique(newX, return_index=True)[1]]
                newWeights = newWeights[np.unique(newX, return_index=True)[1]]

                newSpline = UnivariateSpline(newX, newY, w=newWeights, s=len(newWeights))
                splines_set[pic].append([newSpline, newMin, newMax])
                toPop.append(int(pair[0]))
                toPop.append(int(pair[1]))

            toPop = sorted(toPop, reverse=True)
            for pop in toPop:
                splines_set[pic].pop(pop)

            splines = splines_set[pic]
            if plotSpline:
                for spline in splines:
                    plot_x = np.arange(spline[1], spline[2], 1)
                    plot_y = spline[0](plot_x)
                    axes[i, 2].plot(plot_y, plot_x)
                    axes[i, 2].set_title("i = " + str(i) + "\n" + "key = " + str(pic))

        self.splines_set_link = splines_set

    def Filter_Splines(self, numberStripes):

        self.numberStripes = numberStripes

        splines_set = self.splines_set_link


        for n in range(len(splines_set.keys())):
            print('\n')
            pic = list(splines_set.keys())[n]
            print(pic)

            zeroValue = []
            splineRanges = []
            orderByZero = []

            for i in range(len(splines_set[pic])):
                if (abs(splines_set[pic][i][1]) / splines_set[pic][i][1]) == (
                        abs(splines_set[pic][i][1]) / splines_set[pic][i][1]):
                    orderByZero_loop = False
                    if splines_set[pic][i][1] > 0:
                        zeroInput = np.min([splines_set[pic][i][1], splines_set[pic][i][2]])
                    elif splines_set[pic][i][1] < 0:
                        zeroInput = np.max([splines_set[pic][i][1], splines_set[pic][i][2]])

                else:
                    zeroInput = 0
                    orderByZero_loop = True

                if (splines_set[pic][i][2] - splines_set[pic][i][1]) > 3:
                    if not np.isnan(splines_set[pic][i][0](zeroInput)):
                        orderByZero.append(orderByZero_loop)
                        zeroValue.append(int(splines_set[pic][i][0](zeroInput)))
                        splineRanges.append(int(splines_set[pic][i][2] - splines_set[pic][i][1]))
            print(orderByZero)
            print(np.all(orderByZero))
            orderByZero = np.all(orderByZero)
            zeroValue = np.asarray([zeroValue])
            splineRanges = np.asarray([splineRanges])
            print(zeroValue)
            print(splineRanges)
            splineRanges_raw = splineRanges
            zerosDecending = (np.shape(zeroValue)[1] * 0.5) < np.shape(np.where(np.diff(zeroValue) < 0)[0])[0]

            rangeDecending = (np.shape(splineRanges)[1] * 0.5) < np.shape(np.where(np.diff(splineRanges) < 0)[0])[0]
            zeroValue_ind = np.argsort(zeroValue)[0]
            splineRanges_ind = np.argsort(splineRanges)[0]
            finalSplines = []
            if zerosDecending != rangeDecending:
                zeroValue_ind = np.flip(zeroValue_ind)
            if np.where(zeroValue_ind == splineRanges_ind)[0].shape[0] >= numberStripes:
                splineRanges = np.flip(splineRanges[0, np.where(zeroValue_ind == splineRanges_ind)[0]])[
                    0:numberStripes]
                print("reducing stripes by matching")

            elif orderByZero:
                splineRanges = np.flip(splineRanges[0, zeroValue_ind])
                print('keeping all stripes, sort by zero values')
                print(splineRanges)

            else:
                splineRanges = np.flip(splineRanges[0, splineRanges_ind])
                print('keeping all stripes, sort by spline Ranges')
                print(splineRanges)

            print(splineRanges.shape[0])
            if splineRanges.shape[0] > numberStripes:
                print("blunt stripe by range")
                splineRanges = splineRanges[0:numberStripes]
                print(splineRanges)

            for splineRange in splineRanges:
                finalSplines.append(splines_set[pic][np.where(splineRanges_raw == splineRange)[1][0]])

            splines_set[pic] = finalSplines

        self.splines_set_final = splines_set

    def Calc_Properties(self):
        splines_set = self.splines_set_final
        pca = self.setPCA

        stripe_properties = {}

        for pic in splines_set.keys():
            stripeStats = []
            plot_points_ant = []
            plot_points_stripe = []

            if len(splines_set[pic]) > 0:
                try:
                    for stripeNo in range(len(splines_set[pic])):
                        x = np.arange(splines_set[pic][stripeNo][1], splines_set[pic][stripeNo][2], 1)
                        y = splines_set[pic][stripeNo][0](x)

                        points = np.transpose(np.array([x, y]))
                        points_orig = pca.inverse_transform(points)

                        plot_points_stripe.append(points_orig)

                        twistVector = np.asarray(
                            [points_orig[-1, 1] - points_orig[0, 1], points_orig[-1, 0] - points_orig[0, 0]])
                        twistOrigin = np.asarray([points_orig[0, 1], points_orig[0, 0]])
                        twist = np.arctan(twistVector[1] / twistVector[0])
                        points_orig_matrix = np.matrix(np.transpose(points_orig))
                        rot_matrix = np.matrix([[np.cos(twist), -1 * np.sin(twist)], [np.sin(twist), np.cos(twist)]])
                        point_rot_matrix = np.matmul(rot_matrix, points_orig_matrix)
                        mirror = False
                        if np.max(point_rot_matrix[0] < 0):
                            mirror = True
                            point_rot_matrix[0] = point_rot_matrix[0] * -1

                        draft_vector_rot = np.where(point_rot_matrix[0] > np.max(point_rot_matrix[0]) * 0.95)
                        draft_vector_rot = point_rot_matrix[:, int(np.mean(draft_vector_rot[1]))]
                        chord_rot = point_rot_matrix[1, -1] - point_rot_matrix[1, 0]
                        draft_vector_rot_origin = np.matrix(point_rot_matrix[0, 0], draft_vector_rot[1, 0])
                        draft = (draft_vector_rot[1, 0] - point_rot_matrix[1, 0]) / chord_rot
                        camber = (draft_vector_rot[0, 0] - draft_vector_rot_origin) / chord_rot
                        frontCamber_pos = (((draft_vector_rot[1, 0] - point_rot_matrix[1, 0]) / 2) + point_rot_matrix[1, 0])
                        frontCamber_pos = np.where(np.all([point_rot_matrix[1, :] < (frontCamber_pos + 1), point_rot_matrix[1, :] > (frontCamber_pos - 1)], axis=0))[1]
                        frontCamber = np.mean(point_rot_matrix[0, frontCamber_pos])
                        frontCamber = (frontCamber - draft_vector_rot_origin[0]) / (draft_vector_rot[0] - draft_vector_rot_origin[0])
                        backCamber_pos = (((point_rot_matrix[1, -1] - draft_vector_rot[1, 0]) / 2) + draft_vector_rot[1, 0])
                        backCamber_pos = np.where(np.all([point_rot_matrix[1, :] < (backCamber_pos + 1),point_rot_matrix[1, :] > (backCamber_pos - 1)], axis=0))[1]
                        backCamber = np.mean(point_rot_matrix[0, backCamber_pos])
                        backCamber = (backCamber - draft_vector_rot_origin[0]) / (draft_vector_rot[0] - draft_vector_rot_origin[0])

                        stripeStats.append([draft, camber[0, 0], frontCamber[0, 0], backCamber[0, 0]])

                        rot_matrix_inv = np.transpose(rot_matrix)
                        plotAnnotations_rot = np.asmatrix(
                            [[draft_vector_rot_origin[0, 0], draft_vector_rot[0, 0], point_rot_matrix[0, 0],
                              point_rot_matrix[0, -1]],
                             [draft_vector_rot[1, 0], draft_vector_rot[1, 0], point_rot_matrix[1, 0],
                              point_rot_matrix[1, -1]]])
                        plotAnnotations = np.matmul(rot_matrix_inv, plotAnnotations_rot)
                        plotAnnotations = np.asarray(np.transpose(plotAnnotations))

                        plot_points_ant.append(plotAnnotations)

                except:
                    print("failed on " + str(stripeNo) + " on " + str(pic))

            stripe_properties[pic] = [plot_points_stripe, plot_points_ant, stripeStats]

        self.stripe_properties = stripe_properties




