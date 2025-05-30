#!/usr/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2021 William H. Majoros bmajoros@alumni.duke.edu
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import gzip
import ProgramName
from Rex import Rex
import statistics
rex=Rex()

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <in:counts.txt.gz> <out:naive-theta.txt>")
(inCountsFile,output_dir)=sys.argv[1:]

IN_COUNTS=gzip.open(inCountsFile,"rt")

header=IN_COUNTS.readline()
if(not rex.find("DNA=(\d+)\s+RNA=(\d+)",header)):
    raise Exception("Can't parse header in counts file: "+header)
DNA_REPS=int(rex[1]); RNA_REPS=int(rex[2])
with open(output_dir, 'w') as f:
    for line in IN_COUNTS:
        fields=line.rstrip().split()
        fields=[float(x) for x in fields]
        DNA=fields[:DNA_REPS]
        RNA=fields[DNA_REPS:]
        sumDNA=sum(DNA)
        sumRNA=sum(RNA)
        naiveTheta=(sumRNA/RNA_REPS)/(sumDNA/DNA_REPS) # theta on original scale
        f.write(str(naiveTheta) + '\n')
IN_COUNTS.close()


