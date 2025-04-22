import gzip
import time
import math
import tensorflow as tf
import keras
import keras.layers as kl
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.layers import Dropout, Reshape, Dense, Activation, Flatten
from keras.layers import BatchNormalization, InputLayer, Input, LSTM, GRU, Bidirectional, Add, Concatenate, LayerNormalization, MultiHeadAttention
import keras_nlp
from keras_nlp.layers import SinePositionEncoding
from keras import models
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, History, ModelCheckpoint
import keras.backend as backend
from keras.backend import int_shape
import pandas as pd
import numpy as np
import ProgramName
import sys
import IOHelper
import SequenceHelper
import random
from scipy import stats
from sklearn.metrics import mean_squared_error
from scipy.stats import spearmanr
from NeuralConfig import NeuralConfig
from Rex import Rex
from tensorflow.keras.models import model_from_json

rex=Rex()

shouldRevComp = 0
MaxTest=999999999
def prepare_input(set,subdir,shouldRevComp,maxCases):
    # Convert sequences to one-hot encoding matrix
    file_seq = str(subdir+"/" + set + ".fasta.gz")
    input_fasta_data_A=loadFasta(file_seq,uppercase=True,revcomp=shouldRevComp,
                                 stop_at=maxCases)
    sequence_length = len(input_fasta_data_A.sequence.iloc[0])
    seq_matrix_A = SequenceHelper.do_one_hot_encoding(input_fasta_data_A.sequence, sequence_length, SequenceHelper.parse_alpha_to_seq)
    X = np.nan_to_num(seq_matrix_A) # Replace NaN with 0 and inf w/big number
    X_reshaped = X.reshape((X.shape[0], X.shape[1], X.shape[2]))
    (DNAreps,RNAreps,Y)=loadCounts(subdir+"/"+set+"-counts.txt.gz",
                                   maxCases)
    global NUM_DNA
    global NUM_RNA
    NUM_DNA=DNAreps
    NUM_RNA=RNAreps
    matrix=pd.DataFrame(Y)
    matrix=tf.cast(matrix,tf.float32)
    return (input_fasta_data_A.sequence, seq_matrix_A, X_reshaped, matrix)






def loadFasta(fasta_path, as_dict=False,uppercase=False, stop_at=None,
              revcomp=False):
    fastas = []
    seq = None
    header = None
    for r in (gzip.open(fasta_path) if fasta_path.endswith(".gz") else open(fasta_path)):
        if type(r) is bytes: r = r.decode("utf-8")
        r = r.strip()
        if r.startswith(">"):
            if seq != None and header != None:
                fastas.append([header, seq])
                if stop_at != None and len(fastas) >= stop_at:
                    break
            seq = ""
            header = r[1:]
        else:
            if seq != None:
                seq += r.upper() if uppercase else r
            else:
                seq = r.upper() if uppercase else r
    if stop_at != None and len(fastas) < stop_at:
        fastas.append([header, seq])
    elif stop_at == None:
        fastas.append([header, seq])
    if as_dict:
        return {h: s for h, s in fastas}
    if(revcomp):
        for rec in fastas:
            rc=generate_complementary_sequence(rec[1])
            rec[1]=rec[1]+"NNNNNNNNNNNNNNNNNNNN"+rc
    return pd.DataFrame({'location': [e[0] for e in fastas],
                         'sequence': [e[1] for e in fastas]})


def loadCounts(filename,maxCases):
    IN=gzip.open(filename) if filename.endswith(".gz") else open(filename)
    header=IN.readline()
    if type(header) is bytes: header = header.decode("utf-8")
    if(not rex.find("DNA=([,\d]+)\s+RNA=([,\d]+)",header)):
        raise Exception("Can't parse counts file header: "+header)
    DNAreps=[int(x) for x in rex[1].split(",")]
    RNAreps=[int(x) for x in rex[2].split(",")]
    numTasks=len(DNAreps)
    linesRead=0
    lines=[]
    for line in IN:
        if type(line) is bytes: line = line.decode("utf-8")
        fields=line.rstrip().split()
        fields=[float(x) for x in fields]
        lines.append(computeNaiveTheta(fields,DNAreps,RNAreps))
        # if(config.useCustomLoss): lines.append(fields)
        # else: lines.append(computeNaiveTheta(fields,DNAreps,RNAreps))
        linesRead+=1
        if(linesRead>=maxCases): break
    lines=np.array(lines)
    return (DNAreps,RNAreps,lines)


def computeNaiveTheta(line,DNAreps,RNAreps):
    numTasks=len(DNAreps)
    a=0; rec=[]
    for i in range(numTasks):
        b=a+DNAreps[i]
        c=b+RNAreps[i]
        DNA=line[a:b] #+1
        RNA=line[b:c] #+1
        # sumX=sum(DNA)+1
        # sumY=sum(RNA)+1
        # naiveTheta=sumY/sumX
        avgX = sum(DNA)/DNAreps[i]
        avgY = sum(RNA)/RNAreps[i]
        naiveTheta=avgY/avgX
        rec.append(tf.math.log(naiveTheta))
        a=c
    return rec

def loadModel(modeldir):
    with open(modeldir +'.json', "r") as json_file:
        model_json = json_file.read()

    model = model_from_json(model_json)
    model.load_weights(modeldir + '.h5')
    model.summary()
    return model

subdir="/datacommons/igvf-pm/A549/full-set/Dex-200/data-normalized"
(X_test_sequence, X_test_seq_matrix, X_test, Y_test) = \
    prepare_input("test",subdir,shouldRevComp,MaxTest)
model = loadModel('/datacommons/igvf-pm/A549/full-set/Dex-200/Dex-200-attention')

pred = model.predict(X_test, batch_size=128)
cor=stats.spearmanr(tf.math.exp(pred.squeeze()),tf.math.exp(Y_test))
print(" rho=",cor.statistic,"p=",cor.pvalue)