
#import honeyClient
#import grabber
import argparse
import os
import glob
import random
import summarizeFile
import urllib2
from anothertextclassifier import classifier
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preform a Naive Baise on a given dataset of good and bad sits');
    parser.add_argument("DIRS", help="Directories for each class", nargs="+", type=str)
    parser.add_argument('-n', '--newfile', nargs='?', type=argparse.FileType('r'), help='file to classify')
    parser.add_argument('--num', type=int, required=True, help='number of files to use per class')
    parser.add_argument('--verbose', help='show verbose output that lists the most influencial tags',action='store_true')
    args=parser.parse_args()
    nFile=args.newfile
    numFilesUse=args.num
    print numFilesUse
    classFilenames=[]
    for directory in args.DIRS:
            dirFiles=[]
            for i in range(0, numFilesUse):
                filename=glob.glob(os.path.join(directory,'*.html'))[i]
                print filename
                dirFiles.append(os.path.join(filename))
            classFilenames.append(dirFiles)

    classTestFilenames=[]
    for fClass in classFilenames:
        numTestFiles=int(len(fClass)*.33)
        testFiles=[]
        for _ in range(0,numTestFiles):
            r=random.randint(0,len(fClass)-1)
            testFiles.append(fClass[r])
            del fClass[r]
        classTestFilenames.append(testFiles)

    classSums=[]
    classTestSums=[]

    parser=summarizeFile.sumParser()

    for fClass in classFilenames:
        for filename in fClass:
            fileA=open(filename,"r")
            dat=fileA.read()
            #print filename
            parser.feed(urllib2.unquote(dat).decode('utf8'))
        nDat=parser.files
        classSums.append(nDat)
        parser.resetParser()
    for fTClass in classTestFilenames:
        for filename in fTClass:
            fileA=open(filename,"r")
            dat=fileA.read()
            parser.feed(urllib2.unquote(dat).decode('utf8'))
        nDat=parser.files
        classTestSums.append(nDat)
        parser.resetParser()
    correct = 0
    wrong = 0
    for fClassIndex in range(0,len(classTestSums)):
        for testFile in classTestSums[fClassIndex]:
            returnObj = classifier.classify(testFile,classSums)
            probs=returnObj[0]
            print probs
            greatest=0
            index=0
            for probIndex in range(0, len(probs)):
                if probs[probIndex]>greatest:
                    index=probIndex
                    greatest=probs[probIndex]
            if index != fClassIndex:
                wrong +=1
            else:
                correct+=1
            if args.verbose:
                for classInd in range(0,len(returnObj[1])):
                    maxInflue=max(returnObj[1][classInd])
                    tagInd=returnObj[1][classInd].index(maxInflue)
                    print "Most influential tag for class: "+str(classInd)+" was:" +returnObj[2][tagInd]

    print (float(correct)/(correct+wrong))*100
    if nFile:
        parser.resetParser()
        dat=nFile.read()
        parser.feed(dat)
        nFileStruct=parser.files[0]
        probs=classifier.classify(nFileStruct,classSums)
        print probs.index(max(probs))
