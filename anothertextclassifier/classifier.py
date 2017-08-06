import scipy.stats
from math import sqrt
import math
import warnings
def classify(testStruct,cStructs):
    totalFiles=sum([len(x) for x in cStructs])
    classPriors=[float(len(x))/totalFiles for x in cStructs]
    classProbs=[1 for _ in cStructs]
    allWordTypes=[]
    allInfluenceVals=[[] for x in classPriors]
    allInfluencingTags=[]
    for fClass in cStructs:
        for textFile in fClass:
            for WordTypeIndex in range(0,len(testStruct)):
                allWordTypes.append([])
                for tag in textFile[WordTypeIndex]:
                    if tag not in allWordTypes[WordTypeIndex]:
                        allWordTypes[WordTypeIndex].append(tag)
    for WordTypeIndex in range(0,len(testStruct)):
        for tag in allWordTypes[WordTypeIndex]:
#            if isCatagorical(testStruct,cStructs,tag,WordTypeIndex) and False:
#                #print "cat"
#                isInTest=tag in testStruct[WordTypeIndex]
#                #calculate the total likelyhood for this tag in testStruct
#                totalTagsEqual=0
#                for fClass in cStructs:
#                    for textFile in fClass:
#                        if (isInTest) == (tag in textFile[WordTypeIndex]):
#                            totalTagsEqual+=1
#                totalLikelyhood=float(totalTagsEqual)/totalFiles
#                #calculate individual class likelyhoods for a given tag
#                classLikelyhoods=[]
#                for fClass in cStructs:
#                    classTagsEqual=1
#                    for textFile in fClass:
#                        if (isInTest) == (tag in textFile[WordTypeIndex]):
#                            classTagsEqual+=1
#                    classLikelyhoods.append(float(classTagsEqual)/len(fClass))
                #now calculate and update probabilities for each
#                if totalLikelyhood>0:
            #classProbs=[(((classLikelyhoods[classIndex]*classPriors[classIndex])/totalLikelyhood)*classProbs[classIndex]) for classIndex in range(0,len(cStructs))]
#            else:
            data=[]
            for fClass in cStructs:
                cData=[]
                for textFile in fClass:
                    if tag in textFile[WordTypeIndex]:
                        cData.append(textFile[WordTypeIndex][tag]+1)
                    else:
                        cData.append(1)
                data.append(cData)
            #if dataIsNormal(data) and dataIsAvailable(data):
            if dataIsNormal(data) and dataIsAvailable(data):
                classParams=[scipy.stats.norm.fit(classData) for classData in data]
                isNoVariance=False
                for classParam in classParams:
                    if classParam[1]==0:
                        isNoVariance=True
                if not isNoVariance:
                    val=1
                    #print "NORMAL VARIED DATA"
                    if tag in testStruct[WordTypeIndex]:
                        val=testStruct[WordTypeIndex][tag]+1
                    classLikelyhoods=[scipy.stats.norm(classParam[0],classParam[1]).pdf(val) for classParam in classParams]
                    totalList=[point for cData in data for point in cData]
                    tMean,tSd=scipy.stats.norm.fit(totalList)
                    totalLikelyhood=scipy.stats.norm(tMean,tSd).pdf(val)
                    if totalLikelyhood>0:
                        classProbs=[(((classLikelyhoods[classIndex]*classPriors[classIndex])/totalLikelyhood)*classProbs[classIndex]) for classIndex in range(0,len(cStructs))]
                        for probIndex in range(0,len(classProbs)):
			    influe=0
                            if classProbs[probIndex] != 0 and classPriors[probIndex] != 0:
				influe=(math.log(classProbs[probIndex],2)-math.log(classPriors[probIndex],2))
			    allInfluenceVals[probIndex].append(influe)
                            allInfluencingTags.append(tag)
    return [classProbs,allInfluenceVals,allInfluencingTags]
def isCatagorical(testStruct,cStruct,tag,WordTypeIndex):
    fValue=0
    #test if two states
    for fClass in cStruct:
        for textFile in fClass:
            if tag in textFile[WordTypeIndex]:
                if fValue==0:
                    fValue=textFile[WordTypeIndex][tag]
                else:
                    if fValue != textFile[WordTypeIndex][tag]:
                        return False
    #test enough data?
    for fClass in cStruct:
        state1=0
        state2=0
        for textFile in fClass:
            if tag in textFile[WordTypeIndex]:
                state2+=1
            else:
                state1+=1
        if state1!=0 and state2!=0:
            if (float(state1)/state2) < .33 or (float(state1)/state2) > .66:
                #return False;
                a=1
        else:
            return False

    return True
def dataIsAvailable(data):
    for cData in data:
        if len(cData)<3:
            return False
    return True
def dataIsNormal(data):
    #gZ,gP=scipy.stats.normaltest(gList);
    #.055 threshold
    tList=[point for cData in data for point in cData]
    z,p=scipy.stats.normaltest(tList)
    if p<.055:
        return False
    return True
