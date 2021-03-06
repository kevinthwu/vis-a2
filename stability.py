# COMP8503 Assignment 2
# Authors: Wu Tien Hsuan, Wu Zhiyong
# TCSVT 2017 Clustervision Visual Supervision of Unsupervised Clustering
# Stability Score

import sys
import pandas as pd
from scipy import linalg
from sklearn.cluster import KMeans
from rtree import index
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from itertools import combinations

def main(argv):

    paint_data = False

    if(len(argv) < 2):
        print("Usage: python stability.py <input-file> [<threshold> <search> <lowest-k> <highest-k>]")
        print("<input-file>: input file name.  Use t4.8k.dat or paint.csv as an example.")
        print("<threshold>:  the threshold for stable cluster. Default: 17")
        print("<search>:     whether to show the statistics for different thresholds (on|off). Default: off")
        print("<lowest-k>:   parameters k as in k-means. Default: 2")
        print("<highest-k>:  parameters k as in k-means. Default: 20")
        print("              The program will run all k from <lowest-k> to <highest-k>")
        return

    filename = argv[1]
    if filename == "paint.csv":
        paint_data = True
    
    threshold = 17
    k_means_low = 2
    k_means_high = 20
    search = False
    
    if(len(argv)>2):
        threshold = int(argv[2])
        
    if(len(argv)>3):
        if argv[3] == "on":
            search = True
    
    if(len(argv)>4):
        k_means_low = int(argv[4])
    
    if(len(argv)>5):
        k_means_high = int(argv[5])

    # Load data here
    print("=== Loading data ===")

    if paint_data:
        df = pd.read_table(filename,
                       sep=',',
                       index_col=None)

        X = df.iloc[:,2:].as_matrix()

        Xtsne = TSNE(n_components=2).fit_transform(X)

    else:                           
        df = pd.read_table(filename,
                        delim_whitespace=True,
                        index_col=None,
                        header=None)

        X = df.as_matrix()

    print("=== Data loaded ===")


    # Show the input data
    if paint_data:
        plt.scatter(Xtsne[:, 0], Xtsne[:, 1], 
                    c='blue', marker='o', 
                    s=5)        
    else:
        plt.scatter(df[0], df[1], 
                    c='blue', marker='o', 
                    s=5)
    plt.grid()
    plt.tight_layout()
    plt.savefig('./original.png', dpi=300)
    #plt.show()

    print("=== Initializing data ===")

    frequency = dict()
    for i in range(len(X)):
        frequency[i] = dict()
        for j in range(i+1, len(X)):
            frequency[i][j] = 0
    print("=== Initializing data ===")


    # do clustering
    print("=== Start Clustering ===")
    for k in range(k_means_low, k_means_high+1):
        
        print("Starting clustering: k-means -- k={}"
              .format(str(k)))
        
        km = KMeans(n_clusters=k, 
                    init='k-means++', 
                    random_state=0).fit(X)
        
        Y = km.labels_
        
        print("Storing the result...")
        
        # update the frequency list
        for i in range(k):
            loc = np.where(Y == i)[0]
            
            for j, s in combinations(loc, 2):
                frequency[j][s] += 1
                
        print("k-means -- k={} complete"
              .format(str(k)))
        
    print("=== Complete Clustering ===")

    # Print statistics
    print("***************************************")
    print("****** Pair Frequency Statistics ******")
    print("***************************************")

    for th in range(k_means_high-k_means_low+1, threshold-1, -1):
        print("Pairs with frequency equals {}: ".format(th),
               sum((v2 >= th)
                    for v1 in frequency.values() 
                        for v2 in v1.values()))

    
    # Connect the pairs of points that are above threshold
    number_of_clusters = 0
    print("===Finding stable clusters with threshold = {}===".format(threshold))
    print("This may take one to two minutes...")
    labels = [0 for x in range(len(X))]
    for i in range(len(X)):
        # Check if a point is labeled
        if labels[i] == 0:
            # If not labeled, check if the point is clustered with other points
            # above a specified number of times
            neighborhood = list()
            for j in range(i+1, len(X)):
                if frequency[i][j] >= threshold:
                    neighborhood.append(j)
            
            # If there is more than one point found, that means a "stable cluster"
            # is found. Label such point.
            if len(neighborhood) > 0:
                number_of_clusters += 1
                labels[i] = number_of_clusters
                
                Q = set(neighborhood)
                
                # Expand the cluster, find transitive closure
                while(len(Q)>0):
                    current = Q.pop()
                    labels[current] = number_of_clusters
                    
                    # Find if point [0, ..., current-1] appears in the current cluster for more than
                    # `threshold` number of times
                    for j in range(current):
                        if labels[j] == 0 and frequency[j][current] >= threshold:
                            Q.add(j)
                    
                    # Find if point [current+1, ..., end] appears in the current cluster for more than
                    # `threshold` number of times
                    for j in range(current+1, len(X)):
                        if labels[j] == 0 and frequency[current][j] >= threshold:
                            Q.add(j)


    colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "olive", "cyan"]
    markers = ["o", "s", "p", "*", "^", "8", "D"]
    labels = np.asarray(labels)

    if paint_data:

        plt.scatter(Xtsne[:, 0][labels==0], Xtsne[:, 1][labels==0], c='gray', marker='o', s=5)

        for i in range(1, number_of_clusters+1):
            plt.scatter(Xtsne[:, 0][labels==i], Xtsne[:, 1][labels==i], c=colors[i%9], marker=markers[int(i/9)%7], s=5)

    else:

        plt.scatter(df[0][labels==0], df[1][labels==0], c='gray', marker='o', s=5)

        for i in range(1, number_of_clusters+1):
            plt.scatter(df[0][labels==i], df[1][labels==i], c=colors[i%9], marker=markers[int(i/9)%7], s=5)

    plt.grid()
    plt.tight_layout()
    plt.savefig('./result_with_given_threshold.png', dpi=300)
    plt.show() #### This is the result so it is worth showing!! ###
    print("Outliers (does not meet threshold with any other data point) are shown in gray")

    if(number_of_clusters > len(colors)*len(markers)):
        print("Warning: some clusters are represented by the same color and marker, please reduce number of clusters or modify the plotting code")


    # Determine the threshold

    # The following code explores the threshold decremently from 
    # the number of possible clusters down to 1. It will stop at
    # the point where the scatter plot can be done using one 
    # marker with various colors. In this example, the number of
    # possible colors is 9.
    if search:
        for th in range(k_means_high-k_means_low+1, 0, -1):
        
            number_of_clusters = 0
            print("Finding stable clusters with threshold = {}".format(th))
            print("This may take one to two minutes...")
            
            labels = [0 for x in range(len(X))]
            
            for i in range(len(X)):
                # Check if a point is labeled
                if labels[i] == 0:
                    # If not labeled, check if the point is clustered with other points
                    # above a specified number of times
                    neighborhood = list()
                    for j in range(i+1, len(X)):
                        if frequency[i][j] >= th:
                            neighborhood.append(j)

                    # If there is more than one point found, that means a "stable cluster"
                    # is found. Label such point.
                    if len(neighborhood) > 0:
                        number_of_clusters += 1
                        labels[i] = number_of_clusters

                        Q = set(neighborhood)

                        # Expand the cluster, find transitive closure
                        while(len(Q)>0):
                            current = Q.pop()
                            labels[current] = number_of_clusters

                            # Find if point [0, ..., current-1] appears in the current cluster for more than
                            # `threshold` number of times
                            for j in range(current):
                                if labels[j] == 0 and frequency[j][current] >= th:
                                    Q.add(j)

                            # Find if point [current+1, ..., end] appears in the current cluster for more than
                            # `threshold` number of times
                            for j in range(current+1, len(X)):
                                if labels[j] == 0 and frequency[current][j] >= th:
                                    Q.add(j)
                                    
            print("*** Summary for threshold - {} ***".format(th))
            print("Number of clusters: ", number_of_clusters)
            print("Data size: ", len(labels))
            print("Data points covered: ", len(labels)-list(labels).count(0))
            print("Number of outliers: ", list(labels).count(0))
            
            labels = np.asarray(labels)
            for i in range(1, number_of_clusters+1):
                if paint_data:
                    plt.scatter(Xtsne[labels==i][:, 0], Xtsne[labels==i][:, 1], c=colors[i%9], marker=markers[int(i/9)%7], s=5)

                else:
                    plt.scatter(df[0][labels==i], df[1][labels==i], c=colors[i%9], marker=markers[int(i/9)%7], s=5)
                
                plt.grid()
                plt.tight_layout()
                #plt.show()
                plt.savefig('./result_' + str(th), dpi=300)
                
            if number_of_clusters > len(colors)*len(markers):
                print(">> This cannot be properly plotted due to the number of colors and markers.")
            if number_of_clusters <= len(colors):
                print(">> This can be plotted by using one marker with different colors.")
                print(">> The finding process will stop now.")
                break

if __name__ == "__main__":
    main(sys.argv)