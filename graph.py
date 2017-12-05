import plotly.plotly as py
import plotly.graph_objs as go
import os
import sys


print("Welcome to DRSVR Graph Generator:")




if (len(sys.argv)!=4):
    print("Invalid Arguments! Arguments in order: filename.drsvr parameter testName:D ")
    sys.exit(0)


fileName = sys.argv[1]
searchParameter = sys.argv[2]
graphName = sys.argv[3]


print "fileName: "+fileName
print "searchParameter: "+searchParameter
print "graphName:" + graphName



def createDirectory(directory):

    cwd = os.getcwd()  # Current Working Directory
    newdirectory = cwd + '//' + directory;


    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory '"+newdirectory+"' has been created! Please put your results inside it!")
    return newdirectory


def SearchArray (myArray, testCase):
    index = 0
    for element in myArray:
        if (element == testCase):
            return index
        index = index + 1

    return -1


def findInArray (myArray, testCase):
    for element in myArray:
        if (testCase in element):
            return True

rootDirectory = os.getcwd();

myDirectory = rootDirectory + "/Processed/Summery/Summery"

createDirectory(myDirectory)


os.chdir(myDirectory)

#searchParameter = "gpu_tot_ipc"
#fileName = "General.drsvr"

logFileName = searchParameter+".drsvrLog"

if (not os.path.isfile(fileName)):
    print(fileName+" does not Exist!")
    sys.exit(0)

f = open(logFileName, "w+")
sumFile = open(fileName,"r")

for line in sumFile:
    if ('@' in line):
        f.write(line)
    if (searchParameter in line):
        f.write(line)

sumFile.close()
f.close()


f = open(logFileName,"r")

TestNames = []
BenchmarkNames = []





for line in f:
    if ('@' in line):
        tokens = line.split('@')
        benchmarkName = tokens[0]
        testName = tokens[1].replace("\n","")

        if (SearchArray(BenchmarkNames,benchmarkName) is -1):
            BenchmarkNames.append(benchmarkName)
        if (SearchArray(TestNames,testName) is -1):
            TestNames.append(testName)



f.close()


#print BenchmarkNames
#print TestNames













results = []

found = False

tubDim = len(TestNames)

#print tubDim

#print("---------------------------------------------------------")

incompleteBenchmarks = []

for benchmark in BenchmarkNames:
    ##print benchmark + ":"
    resultTub = []
    for test in TestNames:
        #print benchmark +"\t"+ test + ":"
        f = open(logFileName, "r")
        foundServiced = False
        found = False
        for line in f:
            if (foundServiced == True):
                continue
            ##print("L: "+line)
            if (benchmark in line):
                if (test in line):
                    found = True
                    continue
            if (found is True):
                #print line
                tokens = line.split('=')
                data = tokens[1].replace(" ","")
                data = data.replace("\n","")
                resultTub.append(float(data))
                found = False
                foundServiced = True

        f.close()
        #print("---------------------------------------------------------")



    if (len(resultTub) == tubDim):
        results.append(resultTub)
    else:
        #print("No enough data for benchmark: " + benchmark + "!")
        incompleteBenchmarks.append(benchmark)

for benchmark in incompleteBenchmarks:
    BenchmarkNames.remove(benchmark)

#print TestNames
#print BenchmarkNames
#print results



adjustedResults = []

index = 0
for test in TestNames:
    resultSet = []
    for set in results:
        resultSet.append(set[index])
    index = index + 1
    adjustedResults.append(resultSet)

print adjustedResults





myTraces = []


index = 0
for test in TestNames:
    x = BenchmarkNames
    #print x;
    y = adjustedResults[index]
    #print y;
    name = test
    #print name
    traceSet = go.Bar(x=x,y=y,name=name)
    ##print traceSet
    myTraces.append(traceSet)
    index = index + 1

layout = go.Layout(
    title=searchParameter,
    barmode='group'
)

fig = go.Figure(data=myTraces,layout=layout)
#graphName=testName+"/"+searchParameter
print graphName;
py.plot(fig, filename=graphName)
