#Parsing protein blast results

#run at the commandline like this: python ./parsing_protein_blast_results_v.0.1.py <file_with_Blast_results>

import sys, re

def removeProteinDuplicates(blastpFile):

    prot = open(blastpFile, 'r')
    
    
    listOfSequences = []
    for line in prot:
        if line.startswith('# Query'):
            items = line.split()
            if items[2] not in listOfSequences:
                listOfSequences.append(items[2])
        if line.startswith('gene'):
            items = line.split()
            if items[1] not in listOfSequences:
                listOfSequences.append(items[1])
            
    #print "Length of sequences is: " + str(len(listOfSequences))        
    prot.close()
    
    prot = open(blastpFile, 'r')        
    
    for line in prot:
        if line.startswith('# Query'):
            items = line.split()
            query = items[2]
        elif line.startswith('gene'):
            items = line.split()
            subject = items[1]
            identity = float(items[2])
            subjectLen = int(items[11])
            queryLen = int(items[10])
            if query == subject:
                pass
            if query != subject:
                if identity == 100 and subjectLen == queryLen:
                    try:
                        position = listOfSequences.index(subject)
                        listOfSequences.pop(position)
                    except ValueError:
                        pass
                elif identity >= 80.0 and subjectLen <= queryLen:
                    try:
                        position = listOfSequences.index(subject)
                        listOfSequences.pop(position)
                    except ValueError:
                        pass
                elif identity >=80.0 and subjectLen > queryLen:
                    try:
                        position = listOfSequences.index(query)
                        listOfSequences.pop(position)
                    except ValueError:
                        pass
    prot.close()
    
    return listOfSequences
    
def extractProteins(blastPFile, fasta, newFileName):
    fileToWrite = open(newFileName, 'w')
    seqList = removeProteinDuplicates(blastPFile)
    regex = r'>(gene\d+)'
    for entry in seqList:
        fastaOpen = open(fasta, 'r')
        foundIt = 0 
        for line in fastaOpen:
            if foundIt == 2:
                fastaOpen.close()
                break
            if foundIt == 1:
                fileToWrite.write(line)
                foundIt = 2
            if line.startswith('>'):
                reLine = re.search(regex, line)
                geneName = reLine.groups()
                if geneName[0] == entry:
                    fileToWrite.write(line)
                    foundIt = 1
    print seqList   
    
if __name__ == "__main__":
    extractProteins(sys.argv[1], sys.argv[2], sys.argv[3])