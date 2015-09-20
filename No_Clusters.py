"""
Compute Number of Clusters in the Final Opinion Distribution
The algortihm is adopted from Deffuant (2006) and Huet et al (2008)
"""
def CompNoClusters():
    cluster_array = np.zeros((100,500))
    clusters = 0
    for i in range(no_of_agents):
        while True:
            a = cluster_array[np.where(cluster_array == i)]
            if a.size > 0:
                break
            else:
                clusters += 1
                current_cluster = []
                current_cluster.append(i)
                for j in range(no_of_agents):
                    delta1 = op1[i] - op1[j]
                    delta2 = op2[i] - op2[j]
                    if sqrt((delta1**2) + (delta2**2)) < epsilon:
                        current_cluster.append(j)
                for x in range (len(current_cluster)):   
                    cluster_array[clusters - 1][x] = current_cluster[x]
                
    cluster_size_list = list()
    for m in range(50):
        if cluster_array[m][0] == 0:
            break
        else:
            cluster_size = 0
            for n in range (300):
                if cluster_array[m][n] > 0:
                    cluster_size += 1
            cluster_size_list.append(cluster_size)
            if cluster_size < 0.01*no_of_agents:
                clusters -= 1
    print 'Number of Clusters = ', clusters
