## split bed file into CRE chunks

from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Interval import Interval
import TempFilename
from Pipe import Pipe
from FastaReader import FastaReader
import sys
import pandas as pd
import re
import os


TWO_BIT_TO_FA="twoBitToFa"
TWO_BIT="/hpc/group/igvf/A549/extra_GCs/hg38.2bit"
ALPHA = ['G','C','A','T']

class Bed3Record:
    """Bed3Record represents a record in a BED3 file"""
    def __init__(self,chr,begin,end):
        self.chr=chr
        self.interval=Interval(begin,end)

    def isBed3(self):
        return True

    def isBed6(self):
        return False

    def getBegin(self):
        return self.interval.begin

    def getEnd(self):
        return self.interval.end

    def toString(self):
        return self.chr+"\t"+str(self.interval.begin)+"\t"+\
            str(self.interval.end)

class Bed6Record(Bed3Record):
    """Bed6Record represents a record in a BED6 file"""
    def __init__(self,chr,begin,end,name,score,strand):
        Bed3Record.__init__(self,chr,begin,end)
        self.name=name
        self.score=score
        self.strand=strand

    def isBed3(self):
        return False

    def isBed6(self):
        return True

    def toString(self):
        s=self.chr+"\t"+str(self.interval.begin)+"\t"+str(self.interval.end)\
            +"\t"+self.name
        if(self.score is not None): s+="\t"+str(self.score)
        if(self.strand is not None): s+="\t"+self.strand
        return s

class BedReader:
    """BedReader reads bed3 and/or bed6 files"""
    def __init__(self,filename):
        self.fh=open(filename,"r")
    def close(self):
        self.fh.close()
    def nextRecord(self):
        while(True):
            line=self.fh.readline()
            if(not line): return None
            if(not re.search("\S",line)): continue
            line=line.rstrip()
            line=line.lstrip()
            fields=line.split()
            n=len(fields)
            if(n==6):
                return Bed6Record(fields[0],int(fields[1]),int(fields[2]),
                                    fields[3],fields[4],fields[5])
            raise Exception("wrong number of fields in bed file: "+line)


def makeFasta(coordFile,fastaFile):
    # twoBitToFa needs 0-based half-open coordinates
    cmd="module load BigWig && "+TWO_BIT_TO_FA+" -noMask -seqList="+coordFile+" "+TWO_BIT+" "+fastaFile
    Pipe.run(cmd)

def makeCoords(coordFile,BedFile,seqlen):
    reader=BedReader(BedFile)
    COORD=open(coordFile,"wt")
    while(True):
        record=reader.nextRecord()
        if(not record): break
        chrom=record.chr
        oldBegin=record.interval.begin
        oldEnd=record.interval.end
        globalBegin=int((oldBegin+oldEnd)/2)-int(seqlen/2)  
        globalEnd=int((oldBegin+oldEnd)/2)+int(seqlen/2)  
        print(chrom+":"+str(globalBegin)+'-'+str(globalEnd),file=COORD)
    reader.close()
    COORD.close()

# NOTE: old indexes are cCRE index from bed file
#       global indexes are indexes which have been shrink or grown
#       to fit the length of seq (300)

def makeCREchunks(fastaFile,outputDir,seqlen,BedFile):
    fastareader=FastaReader(fastaFile)
    bedreader=BedReader(BedFile)
    n=0  # split into subfiles, 1000 lines per file
    chunk=1
    OUT=open(outputDir+str(chunk)+'.txt',"wt")
    while(True):
        pair=fastareader.nextSequence()
        record=bedreader.nextRecord()
        if (pair is None and record is not None) or (pair is not None and record is None): 
            raise Exception('length of old and global indexes do not match')
        if(pair is None): break
        (defline,seq)=pair  
        oldBegin=int(record.interval.begin)
        oldEnd=int(record.interval.end)
        head=record.chr+":"+str(oldBegin)+"-"+str(oldEnd)+'\t'
        
        globalBegin=int((oldBegin+oldEnd)/2)-int(seqlen/2)  
        globalEnd=int((oldBegin+oldEnd)/2)+int(seqlen/2)   
        if(oldBegin<=globalBegin):
            localBegin=0; localEnd=seqlen
            begin=globalBegin; end=globalEnd
        else:
            localBegin=oldBegin-globalBegin; localEnd=oldEnd-globalBegin
            begin=oldBegin; end=oldEnd

        head+=str(begin)+':ref='+seq[localBegin]+':'+','.join([x for x in ALPHA])+'\t'
        for i in range(1,localEnd-localBegin):
            BETA = [x for x in ALPHA if x!=seq[localBegin+i]]
            head+=str(begin+i)+':ref='+seq[localBegin+i]+':'+','.join([x for x in BETA])+'\t'

        print(head,file=OUT)
        n+=1
        if n%1000==0:
            OUT.close()
            chunk+=1
            OUT=open(outputDir+str(chunk)+'.txt',"wt")

    fastareader.close();bedreader.close();OUT.close()




#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=4):
    exit(ProgramName.get()+" <BedFile> <output dir CRE subfiles> <sequence length>\n")
(BedFile,outputDir,seqlen)=sys.argv[1:]

# for reference
# makeCoords('/datacommons/igvf-pm/K562/CRE-preds/all-CREs.txt',BedFile,int(seqlen))
# makeFasta('/datacommons/igvf-pm/K562/CRE-preds/all-CREs.txt','/datacommons/igvf-pm/K562/CRE-preds/all-CREs.fasta')

coordFile=TempFilename.generate(".coords")
fastaFile=TempFilename.generate(".fasta") 
makeCoords(coordFile,BedFile,int(seqlen))
makeFasta(coordFile,fastaFile)
makeCREchunks(fastaFile,outputDir,int(seqlen),BedFile)
os.remove(coordFile); os.remove(fastaFile)


