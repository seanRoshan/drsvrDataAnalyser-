import glob
import os
import sys
import shutil
import re



print("Welcome DRSVR! Lets analyze a file!")

rootDirectory = os.getcwd()  # Root Directory

def closeAndSaveTemp(newFile,analysedFileName):
    cwd = os.getcwd()  # Current Working Directory
    newTempDirectory = cwd + "//temp"  # Temp Directory

    createDirectory('temp')  # create a temp directory

    newFile.close()

    # Copy the src file to the temp folder
    dst = newTempDirectory  # Destination Location
    src = newFile.name  # Source Location

    print("Source: "+src)
    print("Destination: "+dst)


    shutil.copy(src, dst)  # Make the copy

    if (src.endswith('.drsvr')):
        extensionSize = len('.drsvr')  # get the length of the extension
        extensionNSize = extensionSize * (-1)  # '-1' for removing the extension
        newSrc = src[:extensionNSize]  # remove the extension from the file name

        tempStr = src.replace(cwd +"//Processed"+ "//", '')  # Remove working directory to extract the file name
        tempStr = tempStr.replace('//', '')  # Concatenation of benchmarkfolder and file name
        benchmarkFolder = tempStr.replace(analysedFileName, '')  # Benchmark folder name
        originalFileName = tempStr.replace(benchmarkFolder, '')  # original fileName
        oldTemp = cwd + "//" + 'temp' + "//" + originalFileName  # oldTemp file
        newTemp = cwd + "//" + 'temp' + "//" + benchmarkFolder + "_" + originalFileName  # Original fileName

        print("oldTemp: " + oldTemp)
        print("newTemp: " + newTemp)

        if (os.path.isfile(newTemp) == False):
            os.rename(oldTemp, newTemp)
        else:
            if (os.path.isfile(oldTemp)):
                os.remove(oldTemp)

    return



def saveFile(fileName, extension, analysedFileName):
    if (fileName.endswith(extension)):
        extensionSize = len(extension)  # get the length of the extension
        extensionNSize = extensionSize * (-1)  # '-1' for removing the extension
        filePath = "Processed//"+fileName[:extensionNSize]  # remove the extension from the file name
        newdirectory = createDirectory(filePath)  # create a new directory
        analysedFileName = '//'+analysedFileName  # the name of Timing options file
        newFilePath = newdirectory + analysedFileName  #
        print("DRSVR NewFilePath: " + newFilePath)
        newFile = open(newFilePath, 'w')
        print("New file hase been opened! " + newFilePath)
        return newFile
    else:
        print("Something is wrong with the file extension!")
        sys.exit()
        return

def createDirectory(directory):

    cwd = os.getcwd()  # Current Working Directory
    newdirectory = cwd + '//' + directory;


    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory '"+newdirectory+"' has been created!")
    else:
        print("Directory '" + newdirectory + "' does already exist!")

    return newdirectory

def processAllFiles(extension):
    print("The program will process,")

    path = getDirectoryInfo(extension)  # get files in the working directory

    for file in glob.glob(path):
        print ("Processing of a "+file+"has been started!")
        extractTimingOptions(file,extension)  # extract timing options
        #extractFCL(file, extension)
        #extractINTRAWARP(file, extension)
        #extractOCCLUSION(file, extension)
        extractgpuParameters(file, extension)
    return

def getDirectoryInfo(extension):
    cwd = os.getcwd() # Current Working Directory
    os.chdir(cwd)     # Set to Current Working DIrectory
    path = "*"+extension
    print ("\tAll files with '"+extension+ "' extension in "+cwd+":")
    for file in glob.glob(path):
        print ("\t\t"+file)
    print("")
    return path


def findTwoStrings (String1, String2, fileName):

    myfile = open(fileName, 'r')

    flag = False
    valid = False

    # read lines inside my file

    for myLine in myfile:

     if (flag is not True):
        if (String1 in myLine):
            #print("String1: ",myLine)
            flag = True

     else:
        if (String2 in myLine):
            flag = False
            valid = True
            myfile.close()
            return valid

    myfile.close()
    return valid





def extractDataBetweenTwoStrings(String1, String2, analysedFileName, fileName, extension):

    myfile = open(fileName, 'r')

    flag = False
    # read lines inside my file



    for myLine in myfile:

     if (flag is not True):
        if (String1 in myLine):
            print myLine
            #print("String1: ",myLine)
            flag = True
            newFile = saveFile(fileName, extension, analysedFileName)
            newFile.write(myLine)

     else:
        if (String2 in myLine):
            #print("String2: ",myLine)
            closeAndSaveTemp(newFile, analysedFileName)
            flag = False
            newFile.close()
            myfile.close()
            return newFile.name
        else:
            newFile.write(myLine)

    return



def extractDataBetweenTwoStringsInclusive(String1, String2, analysedFileName, fileName, extension):

    myfile = open(fileName, 'r')

    flag = False
    # read lines inside my file

    for myLine in myfile:

     if (flag is not True):
        if (String1 in myLine):
            #print("String1: ",myLine)
            flag = True
            newFile = saveFile(fileName, extension, analysedFileName)
            newFile.write(myLine)

     else:
        if (String2 in myLine):
            #print("String2: ",myLine)
            newFile.write(myLine)
            closeAndSaveTemp(newFile, analysedFileName)
            flag = False
            newFile.close()
            myfile.close()
            return newFile.name
        else:
            newFile.write(myLine)

    return newFile.name







def removeMe(filePath):
    if (os.path.isfile(filePath)):
        os.remove(filePath)
    return


def copyMe(fileName):
    cwd = os.getcwd()  # Current Working Directory
    shutil.copy(fileName, cwd)  # Make the copy

    return


def swapNames(SRC, DST):
    TEMP_DST = DST + "_temp"
    TEMP_SRC = SRC + "_temp"

    #print("DRSVR SRC: ", SRC)
    #print("DRSVR DST: ", DST)
    #print("DRSVR TEMP SRC: ", TEMP_SRC)
    #print("DRSVR TEMP DST: ", TEMP_DST)

    shutil.copy(DST, TEMP_DST)  # Make the copy
    shutil.copy(SRC, TEMP_SRC)  # Make the copy

    os.remove(DST)
    os.remove(SRC)

    os.rename(TEMP_DST,SRC)

    os.rename(TEMP_SRC, DST)

    print (SRC," and ",DST," have been swapped!")
    return


def TEST(fileName,extension):

    "This function extracts the timing option from the result file!"

    print("TEST Started!")

    myfile = open(fileName, 'r')

    newfile = open("TEST.DRSVR",'w')

    for myLine in myfile:
        newfile.write(myLine)

    print("TEST ENDED!")

    return


def extractTimingOptions(fileName,extension):

    "This function extracts the timing option from the result file!"

    print("Timing options extraction has been Started!")

    myfile = open(fileName, 'r')

    extractDataBetweenTwoStrings("DRAM Timing Options:", "Total number of memory sub partition",
                               'Timing-Options.drsvr', fileName, extension)

    print("Timing options have been extracted successfully!")

    myfile.close()

    return

def extractFCL(fileName,extension):

    "This function extracts the timing option from the result file!"

    print("FCL options extraction has been Started!")

    myfile = open(fileName, 'r')

    extractDataBetweenTwoStrings("FCL DETAILS", "END OF FCL DETAILS",
                                 'FCL.drsvr', fileName, extension)

    print("FCL options have been extracted successfully!")

    myfile.close()

    return



def extractOCCLUSION(fileName,extension):

    "This function extracts the timing option from the result file!"

    print("OCCLUSION options extraction has been Started!")

    myfile = open(fileName, 'r')

    extractDataBetweenTwoStrings("OCCLUSION DETAILS", "END OF OCCLUSION DETAILS",
                                 'OCCLUSION.drsvr', fileName, extension)

    print("OCCLUSION options have been extracted successfully!")

    myfile.close()

    return

def extractINTRAWARP(fileName,extension):

    "This function extracts the timing option from the result file!"

    print("INTRAWARP options extraction has been Started!")

    myfile = open(fileName, 'r')

    extractDataBetweenTwoStrings("INTRA_WARP_CONTENTION DETAILS", "END OF INTRA_WARP_CONTENTION DETAILS",
                                 'INTRAWARP.drsvr', fileName, extension)

    print("INTRAWARP options have been extracted successfully!")

    myfile.close()

    return

def extractgpuParameters(fileName,extension):

    "This function extracts the gpu parameters type 1 from the result file!"

    print("GPU parameters extraction has been Started!")

    myfile = open(fileName, 'r')

    # First find the last kernel

    myString = "kernel_launch_uid"

    print("myFile: ", myfile)

    for myLine in myfile:
        if (myString in myLine):
            lastString = myLine

    myfile.close()

    # GPU_Result contains the information of the last kernel
    # Now we should extract information from this file

    fileTemp = extractDataBetweenTwoStringsInclusive(lastString, "END OF OCCLUSION DETAILS",
                               'GPU-Result.drsvr', fileName, extension)

    copyMe(fileTemp)

    fileTemp = 'GPU-Result.drsvr'

    #print("DRSVR1: ",fileTemp)
    #print("DRSVR2: ", fileName)

    swapNames(fileTemp, fileName)

    #print("fileName: ",fileName)
    #print("lastString: ",lastString)

    extractDataBetweenTwoStrings(lastString, "Core cache stats", 'General.drsvr', fileName, extension)

    extractDataBetweenTwoStrings("Core cache stats", "warp_id issue ditsribution:", 'L1Cache.drsvr', fileName,
                                 extension)

    extractDataBetweenTwoStringsInclusive("Interconnect-DETAILS", "END-of-Interconnect-DETAILS",
                                          'Interconnection.drsvr', fileName,
                                          extension)

    extractDataBetweenTwoStrings("========= L2 cache stats =========", "Interconnect-DETAILS",
                                          'L2Cache.drsvr', fileName,
                                          extension)

    extractDataBetweenTwoStrings("gpgpu_n_tot_thrd_icount", "Warp Occupancy Distribution",
                                 'GPU-STATS.drsvr', fileName,
                                 extension)


    extractDataBetweenTwoStrings("Warp Occupancy Distribution:", "========= L2 cache stats =========",
                                 'DRAM.drsvr', fileName,
                                 extension)

    extractDataBetweenTwoStrings("FCL DETAILS", "END OF FCL DETAILS",
                                 'FCL.drsvr', fileName, extension)

    extractDataBetweenTwoStrings("INTRA_WARP_CONTENTION DETAILS", "END OF INTRA_WARP_CONTENTION DETAILS",
                                 'INTRAWARP.drsvr', fileName, extension)

    extractDataBetweenTwoStrings("OCCLUSION DETAILS", "END OF OCCLUSION DETAILS",
                                 'OCCLUSION.drsvr', fileName, extension)

    swapNames(fileTemp, fileName)


    removeMe(fileTemp)


    """

    # If you want all karnels, use this part DRSVR! :D

    totalKernelCount = int(re.findall('\d+', lastString)[0])
    print("totalKernelCount: ",totalKernelCount)


    for index in range (0,totalKernelCount):
        for myLine in myfile:
            if (myString in myLine):
    """

    print("GPU parameters have been extracted successfully!")

    return
#getDirectoryInfo(".drsvr") # get files in the working directory
#getDirectoryInfo(".txt") # get files in the working directory


# This function creates a several folders for each parameter type
# for Example: temp/DRAM
#              temp/GPU_STATS
def createGroupDirectories():

    createDirectory("DRAM")
    createDirectory("GPU-Result")
    createDirectory("GPU-STATS")
    createDirectory("Interconnection")
    createDirectory("General")
    createDirectory("L1Cache")
    createDirectory("L2Cache")
    createDirectory("Timing-Options")
    createDirectory("FCL")
    createDirectory("INTRAWARP")
    createDirectory("OCCLUSION")


    return

def removeExtension (srcName, extension):
    if (srcName.endswith(extension)):
        extensionSize = len(extension)  # get the length of the extension
        extensionNSize = extensionSize * (-1)  # '-1' for removing the extension
        dstName = srcName[:extensionNSize]  # remove the extension from the file name
        # print("New dstName: " + dstName)
        return dstName
    else:
        print("Something is wrong with the file extension!")
        sys.exit()

def splitName (srcName,deli,extension):
    tmpName = removeExtension(srcName, extension)
    nameArray = tmpName.split(deli)
    return nameArray

def getBenchmarkName (srcName,extension):
    nameArray = splitName(srcName,"_",extension)
    return (nameArray[0])

def getGroupName (srcName,extension):
    nameArray = splitName(srcName, "_",extension)
    return nameArray[3]

def getExperimentName (srcName,extension):
    nameArray = splitName(srcName, "_",extension)
    return nameArray[2]

def getDSTName (srcName,extension):
    benchmarkName = getBenchmarkName(srcName,extension)+"_"+getExperimentName (srcName,extension)+extension
    return benchmarkName

def sortMe (srcName,extension):

    cwd = os.getcwd()  # Current Working Directory


    dstName = getDSTName(srcName, extension)
    groupName = getGroupName(srcName,extension)

    shutil.copy(srcName, dstName)  # Make the copy

    groupDirectory = cwd + "//" + groupName
    subGroupDirectory = groupDirectory +"//"+ getBenchmarkName(srcName,extension)

    createDirectory(subGroupDirectory)

    print("subGroupDirectory: ",subGroupDirectory)

    shutil.copy(dstName, subGroupDirectory)  # Make the copy
    os.remove(dstName)
    os.remove(srcName)

    return

def extractParameters():

    def getExperimentName (fileName,folderName,Extension):
        experimentName = removeExtension(fileName,extension)
        experimentName = experimentName.replace(folderName+"_","")
        return experimentName

    def findWriteParameter (parameterString,sumfile,myfile,newDirectory):

        bufferedWriter = parameterString.replace("=","")+"\t\t"
        flag = False
        for myfile in os.listdir(newDirectory):
            if ".drsvr" in myfile:
                tempFile = open(myfile,'r')
                flag = True
                for myLine in tempFile:
                    if parameterString in myLine:
                       pureData = myLine.replace(parameterString,"").rstrip("\n")
                       bufferedWriter = bufferedWriter + pureData+ "\t\t\t"
        if (flag is True):
             bufferedWriter = bufferedWriter + "\n"
             sumfile.write(bufferedWriter)
             tempFile.close()
        return

    def findWriteParameterWReplace (parameterString, replaceString, sumfile,myfile,newDirectory):

        #bufferedWriter = parameterString.replace("=","")+"\t\t"
        bufferedWriter = replaceString
        flag = False
        found = False
        for myfile in os.listdir(newDirectory):
            if ".drsvr" in myfile:
                tempFile = open(myfile,'r')
                flag = True
                for myLine in tempFile:
                    if parameterString in myLine:
                       pureData = myLine.replace(parameterString,"").rstrip("\n")
                       bufferedWriter = bufferedWriter + pureData+ "\t\t\t"
                if (found is False):
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\t\t\t"
        if (flag is True):
             bufferedWriter = bufferedWriter + "\n"
             sumfile.write(bufferedWriter)
             tempFile.close()
        return

    def findWriteParameterHorizontal (headString,parameterString,sumfile,myfile,newDirectory,deli,space):

        flag1 = False
        flag2 = False
        for myfile in os.listdir(newDirectory):
            if ".drsvr" in myfile:
                tempFile = open(myfile,'r')
                for myLine in tempFile:
                    if headString in myLine:
                       array = myLine.split(space)
                       for token in array:
                           if (parameterString in token):
                               if (bool(re.compile(token.split(deli)[0]).search(parameterString))):
                                    flag2 = True
                                    bufferedWriter = (token.split(deli)[0])+"\t\t\t"
                tempFile.close()

        for myfile in os.listdir(newDirectory):
            if ".drsvr" in myfile:
                tempFile = open(myfile, 'r')
                flag = True
                for myLine in tempFile:
                    if headString in myLine:
                        array = myLine.split(space)
                        for token in array:
                            if (parameterString in token):
                                if (bool(re.compile(token.split(deli)[0]).search(parameterString))):
                                    bufferedWriter = bufferedWriter + token.split(deli)[1].strip("\n")+ "\t\t\t"

        if (flag is True) and (flag2 is True):
            bufferedWriter = bufferedWriter + "\n"
            sumfile.write(bufferedWriter)
            tempFile.close()
        return

    def analyze_general():

        generalDirectory = tempDirectory + "//General"  # General Directory
        os.chdir(generalDirectory)

        #print("General Directory: ")
        for folder in os.listdir(generalDirectory):
            #print("\t",folder)
            newDirectory = generalDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if ".drsvr" not in myfile:
                    removeMe(myfile)
            newFile = open("General.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("General.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameter("gpu_sim_cycle =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_sim_insn =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_ipc =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_tot_sim_cycle =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_tot_ipc =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_total_sim_rate=", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_bottleNeck():

        gpuResultDirectory = tempDirectory + "//GPU-Result"  # General Directory
        os.chdir(gpuResultDirectory)

        #print("General Directory: ")
        for folder in os.listdir(gpuResultDirectory):
            #print("\t",folder)
            newDirectory = gpuResultDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile) :
                    removeMe(myfile)
            newFile = open("bottleNeck.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("bottleNeck.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameter("gpgpu_n_stall_shd_mem =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_stall_dramfull =", newFile, myfile, newDirectory)
            findWriteParameter("gpu_stall_icnt2sh    =", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_MemoryAccessStats():

        gpuResultDirectory = tempDirectory + "//GPU-Result"  # General Directory
        os.chdir(gpuResultDirectory)

        #print("General Directory: ")
        for folder in os.listdir(gpuResultDirectory):
            #print("\t",folder)
            newDirectory = gpuResultDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile):
                    removeMe(myfile)
            newFile = open("MemoryAccessStats.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("MemoryAccessStats.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameter("gpgpu_n_load_insn  =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_store_insn =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_shmem_insn =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_tex_insn =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_const_mem_insn =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_param_mem_insn =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_cmem_portconflict =", newFile, myfile, newDirectory)
            findWriteParameter("maxmrqlatency =", newFile, myfile, newDirectory)
            findWriteParameter("maxmflatency =", newFile, myfile, newDirectory)
            findWriteParameter("averagemflatency =", newFile, myfile, newDirectory)
            findWriteParameter("max_icnt2mem_latency =", newFile, myfile, newDirectory)
            findWriteParameter("max_icnt2sh_latency =", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_MemorySubSystemStats():

        gpuStatsDirectory = tempDirectory + "//GPU-STATS"  # General Directory
        os.chdir(gpuStatsDirectory)

        #print("General Directory: ")
        for folder in os.listdir(gpuStatsDirectory):
            #print("\t",folder)
            newDirectory = gpuStatsDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile):
                    removeMe(myfile)
            newFile = open("MemorySubSystemStats.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("MemorySubSystemStats.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameter("gpgpu_n_mem_read_local =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_mem_write_local =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_mem_read_global =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_mem_write_global =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_mem_texture =", newFile, myfile, newDirectory)
            findWriteParameter("gpgpu_n_mem_const =", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return
    def analyze_controlFlowStats():

        dramDirectory = tempDirectory + "//DRAM"  # General Directory
        os.chdir(dramDirectory)

        #print("General Directory: ")
        for folder in os.listdir(dramDirectory):
            #print("\t",folder)
            newDirectory = dramDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile):
                    removeMe(myfile)
            newFile = open("controlFlowStats.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("controlFlowStats.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameterHorizontal("Stall", "Stall", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W0_Idle", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W0_Scoreboard", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W1", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W2", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W3", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W4", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W5", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W6", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W7", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W8", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W9", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W10", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W11", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W12", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W13", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W14", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W15", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W16", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W17", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W18", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W19", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W20", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W21", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W22", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W23", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W24", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W25", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W26", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W27", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W28", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W29", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W30", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W31", newFile, myfile, newDirectory,":","	")
            findWriteParameterHorizontal("Stall", "W32", newFile, myfile, newDirectory,":","	")
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_dramStats():

        dramDirectory = tempDirectory + "//DRAM"  # General Directory
        os.chdir(dramDirectory)

        #print("General Directory: ")
        for folder in os.listdir(dramDirectory):
            #print("\t",folder)
            newDirectory = dramDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile):
                    removeMe(myfile)
            newFile = open("dramStats.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("dramStats.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameterHorizontal("n_cmd", "n_cmd", newFile, myfile, newDirectory,"="," ")
            findWriteParameterHorizontal("n_cmd", "n_nop", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_cmd", "n_act", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_cmd", "n_pre", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_cmd", "n_req", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_cmd", "n_rd", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_cmd", "n_write", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_cmd", "bw_util", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_activity", "n_activity", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("n_activity", "dram_eff", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("mrqq:", "max", newFile, myfile, newDirectory, "=", " ")
            findWriteParameterHorizontal("mrqq:", "avg", newFile, myfile, newDirectory, "=", " ")
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_cacheStats():

        L1CacheDirectory = tempDirectory + "//L1Cache"  # General Directory
        os.chdir(L1CacheDirectory)

        #print("General Directory: ")
        for folder in os.listdir(L1CacheDirectory):
            #print("\t",folder)
            newDirectory = L1CacheDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile):
                    removeMe(myfile)
            newFile = open("cacheStats.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("cacheStats.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameter("L1I_total_cache_accesses =", newFile, myfile, newDirectory)
            findWriteParameter("L1I_total_cache_misses =", newFile, myfile, newDirectory)
            findWriteParameter("L1I_total_cache_miss_rate =", newFile, myfile, newDirectory)
            findWriteParameter("L1I_total_cache_pending_hits =", newFile, myfile, newDirectory)
            findWriteParameter("L1I_total_cache_reservation_fails =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_total_cache_accesses =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_total_cache_misses =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_total_cache_miss_rate =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_total_cache_pending_hits =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_total_cache_reservation_fails =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_cache_data_port_util =", newFile, myfile, newDirectory)
            findWriteParameter("L1D_cache_fill_port_util =", newFile, myfile, newDirectory)
            findWriteParameter("L1C_total_cache_accesses =", newFile, myfile, newDirectory)
            findWriteParameter("L1C_total_cache_miss_rate =", newFile, myfile, newDirectory)
            findWriteParameter("L1C_total_cache_miss_rate =", newFile, myfile, newDirectory)
            findWriteParameter("L1C_total_cache_pending_hits =", newFile, myfile, newDirectory)
            findWriteParameter("L1C_total_cache_reservation_fails =", newFile, myfile, newDirectory)
            findWriteParameter("L1T_total_cache_accesses =", newFile, myfile, newDirectory)
            findWriteParameter("L1T_total_cache_misses =", newFile, myfile, newDirectory)
            findWriteParameter("L1T_total_cache_pending_hits =", newFile, myfile, newDirectory)
            findWriteParameter("L1T_total_cache_reservation_fails =", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_interconnectStats():

        interconnectionDirectory = tempDirectory + "//Interconnection"  # General Directory
        os.chdir(interconnectionDirectory)

        #print("General Directory: ")
        for folder in os.listdir(interconnectionDirectory):
            #print("\t",folder)
            newDirectory = interconnectionDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if (".drsvr" not in myfile) and (".DRSVRSUM" not in myfile):
                    removeMe(myfile)
            newFile = open("interconnectStats.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("interconnectStats.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameter("Packet latency average =", newFile, myfile, newDirectory)
            findWriteParameter("Network latency average =", newFile, myfile, newDirectory)
            findWriteParameter("Flit latency average =", newFile, myfile, newDirectory)
            findWriteParameter("Fragmentation average =", newFile, myfile, newDirectory)
            findWriteParameter("Injected packet rate average =", newFile, myfile, newDirectory)
            findWriteParameter("Accepted packet rate average =", newFile, myfile, newDirectory)
            findWriteParameter("Injected flit rate average =", newFile, myfile, newDirectory)
            findWriteParameter("Accepted flit rate average=", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_fcl():

        fclDirectory = tempDirectory + "//FCL"  # General Directory
        os.chdir(fclDirectory)

        for folder in os.listdir(fclDirectory):
            newDirectory = fclDirectory+"//"+folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if ".drsvr" not in myfile:
                    removeMe(myfile)
            newFile = open("FCL.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t["+\
                                   getExperimentName(myfile,folder,".drsvr")+"]"
            newFile = open("FCL.DRSVRSUM", 'a')
            bufferWriter = bufferWriter+"\n"
            newFile.write(bufferWriter)
            findWriteParameterWReplace("SUM FCL[0] =", "FCL" , newFile, myfile, newDirectory)
            findWriteParameterWReplace("SUM FCL[1] =", "NFCL", newFile, myfile, newDirectory)
            findWriteParameterWReplace("TOTAL FCL =", "TFCL", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    def analyze_intrawarp():

        intrawarpDirectory = tempDirectory + "//INTRAWARP"  # General Directory
        os.chdir(intrawarpDirectory)

        for folder in os.listdir(intrawarpDirectory):
            newDirectory = intrawarpDirectory + "//" + folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if ".drsvr" not in myfile:
                    removeMe(myfile)
            newFile = open("INTRAWARP.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t[" + \
                                   getExperimentName(myfile, folder, ".drsvr") + "]"
            newFile = open("INTRAWARP.DRSVRSUM", 'a')
            bufferWriter = bufferWriter + "\n"
            newFile.write(bufferWriter)

            findWriteParameterWReplace("SUM INTRA_WARP_CONTENTION[0] =", "CROSS_WARP_CONTENTION", newFile, myfile, newDirectory)
            findWriteParameterWReplace("SUM INTRA_WARP_CONTENTION[1] =", "INTRA_WARP_CONTENTION", newFile, myfile, newDirectory)
            findWriteParameterWReplace("TOTAL INTRA_WARP_CONTENTION =", "TOTAL_WARP_CONTENTION", newFile, myfile, newDirectory)

            newFile.close()
            os.chdir(tempDirectory)
        return


    def analyze_occlusion():

        occlusionDirectory = tempDirectory + "//OCCLUSION"  # General Directory
        os.chdir(occlusionDirectory)

        for folder in os.listdir(occlusionDirectory):
            newDirectory = occlusionDirectory + "//" + folder
            os.chdir(newDirectory)
            for myfile in os.listdir(newDirectory):
                if ".drsvr" not in myfile:
                    removeMe(myfile)
            newFile = open("OCCLUSION.DRSVRSUM", 'w')
            bufferWriter = folder
            newFile.close()
            for myfile in os.listdir(newDirectory):
                if ".drsvr" in myfile:
                    bufferWriter = bufferWriter + "\t\t\t[" + \
                                   getExperimentName(myfile, folder, ".drsvr") + "]"
            newFile = open("OCCLUSION.DRSVRSUM", 'a')
            bufferWriter = bufferWriter + "\n"
            newFile.write(bufferWriter)
            findWriteParameterWReplace("TOTAL OCCLUSION =", "OCCLUSION", newFile, myfile, newDirectory)
            newFile.close()
            os.chdir(tempDirectory)
        return

    tempDirectory = rootDirectory + "//temp"  # Temp Directory

    os.chdir(tempDirectory)

    extension = '.drsvr'

    path = getDirectoryInfo(extension)  # get files in the working directory

    createGroupDirectories()

    for fileName in glob.glob(path):
        #print("SORT: ",fileName)
        sortMe(fileName,extension)

    analyze_general()
    analyze_bottleNeck()
    analyze_MemoryAccessStats()
    analyze_MemorySubSystemStats()
    analyze_controlFlowStats()
    analyze_dramStats()
    analyze_cacheStats()
    analyze_interconnectStats()
    analyze_fcl()
    analyze_intrawarp()
    analyze_occlusion()


    os.chdir(rootDirectory)

    return

def addExtension(fileName, Extenstion):

    return fileName+Extenstion


def verifyBenchmark(fileName):

    valid = False

    myfile = open(fileName, 'r')

    # First find the last kernel

    myString = "kernel_launch_uid"

    lastString = ""

    for myLine in myfile:
        if (myString in myLine):
            lastString = myLine

    myfile.close()

    if myString in lastString:
        valid = findTwoStrings(lastString,"gpgpu_simulation_time", fileName)

    return valid

def preProcess():

    # This function preprocess all benchmarks to verify them
    # please put all benchmarks in the benchmark folder

    #rootDirectory = os.getcwd()  # Current Working Directory
    benchmarksDirectory = rootDirectory + "//Benchmarks"  # Temp Director

    os.chdir(benchmarksDirectory)  # Change to Benchmark Directory

    for folderName in os.listdir(benchmarksDirectory):
        if (os.path.isdir(folderName)):
            tempDirectory = benchmarksDirectory + "//" + folderName
            os.chdir(tempDirectory) # go inside benchmark folder
            if (os.path.isfile("log.txt")): # remove log.txt file
                removeMe("log.txt")
            for fileName in os.listdir(tempDirectory):
                if (verifyBenchmark(fileName) is True):
                    tempFileName = removeExtension(fileName,".txt")
                    tempFileName = tempFileName + "_" + folderName + ".txt"
                    dst = rootDirectory+"//"+tempFileName
                    shutil.copy(fileName, dst)
                else:
                    print("FileName: "+fileName+" is not complete!")

            os.chdir(benchmarksDirectory)

    os.chdir(rootDirectory)

    return

def cleanProcess():

    os.chdir(rootDirectory)

    for fileName in os.listdir(rootDirectory):
        if (".txt" in fileName):
            removeMe(fileName)

    tempDirectory = rootDirectory+"//temp"

    if (os.path.isdir(tempDirectory)):
        shutil.rmtree(tempDirectory)
    return



def categorizeIt(sumTerm, summeryDirectory, fileNamePrefix):

    #print ("Lets categorize "+sumTerm)
    sumFolder = sumTerm

    for fileName in os.listdir("."):
        if (sumFolder in fileName):
            #print fileName
            if (fileNamePrefix not in fileName):
                newName = fileNamePrefix + '_' + fileName
                os.rename(fileName, fileNamePrefix + '_' + fileName)
            else:
                newName = fileName

            dst = summeryDirectory + "/" + sumFolder
            shutil.copy(newName, dst)

            print("NewName: " + newName)


def catagorizationProcess():

    def fixOCCLUSION(sumTerm, summeryDirectory, folderDirectory):

        sumFolder = sumTerm

        for fileName in os.listdir("."):
            if (sumFolder in fileName):
                newName = "temp_" + fileName
                srcFile = os.path.join(folderDirectory,fileName)
                dstFile = os.path.join(folderDirectory,newName)


                newFile = open(dstFile, 'w+')

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("TOTAL OCCLUSION = " in line):
                        bufferedWriter = "OCCLUSION = "
                        pureData = line.replace("TOTAL OCCLUSION = ", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "OCCLUSION = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                newFile.close()

                swapNames(srcFile,dstFile)

                removeMe(dstFile)

                return

    def fixINTRAWARP(sumTerm, summeryDirectory, folderDirectory):

        # print ("Lets categorize "+sumTerm)
        sumFolder = sumTerm

        for fileName in os.listdir("."):
            if (sumFolder in fileName):
                newName = "temp_" + fileName
                srcFile = os.path.join(folderDirectory,fileName)
                dstFile = os.path.join(folderDirectory,newName)


                newFile = open(dstFile, 'w+')

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("SUM INTRA_WARP_CONTENTION[0] = " in line):
                        bufferedWriter = "CROSS_WARP_CONTENTION = "
                        pureData = line.replace("SUM INTRA_WARP_CONTENTION[0] =", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "CROSS_WARP_CONTENTION = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("SUM INTRA_WARP_CONTENTION[1] " in line):
                        bufferedWriter = "INTRA_WARP_CONTENTION = "
                        pureData = line.replace("SUM INTRA_WARP_CONTENTION[1] =", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "INTRA_WARP_CONTENTION = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("TOTAL INTRA_WARP_CONTENTION =" in line):
                        bufferedWriter = "TOTAL_WARP_CONTENTION = "
                        pureData = line.replace("TOTAL INTRA_WARP_CONTENTION = ", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "TOTAL_WARP_CONTENTION = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                newFile.close()

                swapNames(srcFile,dstFile)

                removeMe(dstFile)

                return


    def fixFCL(sumTerm, summeryDirectory, folderDirectory):

        # print ("Lets categorize "+sumTerm)
        sumFolder = sumTerm

        for fileName in os.listdir("."):
            if (sumFolder in fileName):
                newName = "temp_" + fileName
                srcFile = os.path.join(folderDirectory,fileName)
                dstFile = os.path.join(folderDirectory,newName)


                newFile = open(dstFile, 'w+')

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("SUM FCL[0] = " in line):
                        bufferedWriter = "NFCL = "
                        pureData = line.replace("SUM FCL[0] = ", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "NFCL = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("SUM FCL[1] = " in line):
                        bufferedWriter = "FCL = "
                        pureData = line.replace("SUM FCL[1] = ", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "FCL = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                found = False
                f = open(srcFile, 'r')
                for line in f:
                    if ("TOTAL FCL =" in line):
                        bufferedWriter = "TFCL = "
                        pureData = line.replace("TOTAL FCL = ", "").rstrip("\n")
                        bufferedWriter = bufferedWriter + pureData + "\n"
                        newFile.write(bufferedWriter)
                        found = True
                if (found is False):
                    bufferedWriter = "TFCL = "
                    pureData = "0"
                    bufferedWriter = bufferedWriter + pureData + "\n"
                    newFile.write(bufferedWriter)
                f.close()

                newFile.close()

                swapNames(srcFile,dstFile)

                removeMe(dstFile)


                return








    #print(rootDirectory)

    processDirectory = rootDirectory + "/Processed"

    #print("tempDirectory: "+tempDirectory)

    os.chdir(processDirectory)

    summeryDirectory = processDirectory + "/Summery"

    createDirectory(summeryDirectory)

    os.chdir(summeryDirectory)

    createGroupDirectories()

    os.chdir(processDirectory)


    for folderName in os.listdir(processDirectory):
        if (os.path.isdir(folderName)):
            if "Summery" not in folderName:
                fileNamePrefix = folderName.replace("_RESULT_","_")
                folderDirectory = processDirectory + "/" + folderName
                print("FileName Prefix:"+fileNamePrefix)
                print("Directory:"+folderDirectory)

                os.chdir(folderDirectory)

                fixFCL('FCL', summeryDirectory, folderDirectory)
                fixINTRAWARP('INTRAWARP', summeryDirectory, folderDirectory)
                fixOCCLUSION('OCCLUSION', summeryDirectory, folderDirectory)

                categorizeIt('General', summeryDirectory, fileNamePrefix)
                categorizeIt('DRAM', summeryDirectory, fileNamePrefix)
                categorizeIt('GPU-Result', summeryDirectory, fileNamePrefix)
                categorizeIt('GPU-STATS', summeryDirectory, fileNamePrefix)
                categorizeIt('Interconnection', summeryDirectory, fileNamePrefix)
                categorizeIt('L1Cache', summeryDirectory, fileNamePrefix)
                categorizeIt('L2Cache', summeryDirectory, fileNamePrefix)
                categorizeIt('Timing-Options', summeryDirectory, fileNamePrefix)
                categorizeIt('FCL', summeryDirectory, fileNamePrefix)
                categorizeIt('INTRAWARP', summeryDirectory, fileNamePrefix)
                categorizeIt('OCCLUSION', summeryDirectory, fileNamePrefix)

                os.chdir(processDirectory)


def summerizationProcess():

    summeryDirectory = rootDirectory + "/Processed/Summery"
    os.chdir(summeryDirectory)

    createDirectory("Summery")
    finalSummeryDirectory = summeryDirectory + "/Summery"


    for folderName in os.listdir(summeryDirectory):
        print summeryDirectory + ":"
        print "\t" + folderName

        #if (os.path.isdir(folderName)):
        if ("Summery" not in folderName):
            folderDir = summeryDirectory+"/"+folderName
            os.chdir(folderDir)
            summeryFileName = "Summery_"+folderName+".drsvr"
            f = open(summeryFileName, "w+")
            for fileName in os.listdir("."):
                if ("Summery" not in fileName):
                    tokens = fileName.split("_")
                    benchmarkName = tokens[0]
                    tokensSize = len(tokens)
                    if (tokensSize>3):
                        testName = tokens[1]+"_"+tokens[2]
                    else:
                        testName = tokens[1]
                    oldFile = open(fileName, "r")
                    f.write(benchmarkName + "@" + testName + "\n")
                    for line in oldFile:
                        f.write(line)
            f.close()
            shutil.copy(summeryFileName, finalSummeryDirectory)
            os.chdir(finalSummeryDirectory)

    for fileName in os.listdir("."):
        newfileName = fileName.replace("Summery_","")
        os.rename(fileName, newfileName)
    os.chdir(summeryDirectory)


#preProcess()

#processAllFiles(".txt")

#extractParameters()

#catagorizationProcess()

#summerizationProcess()

#cleanProcess()
#print(array)