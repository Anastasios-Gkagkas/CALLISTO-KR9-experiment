import numpy as np


def calcHammingDist(queryCode, databaseCodes):
    return 0.5 * (databaseCodes.shape[1] - queryCode @ np.transpose(databaseCodes))


def getResultsNum(shotsId, queryCode, databaseCodes, resultsNum):
    # Compute Hamming distances
    hammingDist = calcHammingDist(queryCode, databaseCodes)
    print('Here')
    print(hammingDist.shape)

    # Arrange position according to hamming distance
    args = np.argsort(hammingDist)

    #print(np.array(shotsId)[args][:resultsNum])
    shotsId = np.array(shotsId)[args][:, :resultsNum]
    #print(resultsNum)
    #print(shotsId.shape)
    #print(shotsId)

    return shotsId

