#!/usr/bin/env python
#========================================================================
# BlueSTARR-multitask Version 0.1
#
# Adapted from DeepSTARR by Bill Majoros (bmajoros@alumni.duke.edu)
# and Alexander Thomson.
# load trained model and do predictions for testing data
#========================================================================
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
import SequenceHelper
import random
from scipy import stats
from sklearn.metrics import mean_squared_error
from scipy.stats import spearmanr
from NeuralConfig import NeuralConfig
from Rex import Rex
from tensorflow.keras.models import model_from_json

rex=Rex()

def main(configFile,subdir,modeldir,outdir):
    startTime=time.time()
    #random.seed(RANDOM_SEED)
    
    # Load hyperparameters from configuration file
    global config
    config=NeuralConfig(configFile)

    # Load data
    print("loading testing data",flush=True)
    shouldRevComp=config.RevComp==1

    testing_set = [x for x in config.TestData]
    (X_test_sequence, X_test_seq_matrix, X_test, Y_test, idx) = \
        prepare_input(testing_set,subdir,shouldRevComp,config.MaxTest,config,'test') \
        if(config.ShouldTest!=0) else (None, None, None, None)
    
    model = loadModel(modeldir, testing_set)
    pred = model.predict(X_test, batch_size=config.BatchSize)

    if(config.ShouldTest!=0):
        numTasks=len(config.Tasks)
    
    if (config.useCustomLoss):
        true_theta, pred_theta, cor=naiveCorrelation(Y_test,pred,0,numTasks) # compute naive theta in naivecorrelation
        print(config.Tasks[0]+" rho=",cor.statistic,"p=",cor.pvalue)
        df = pd.DataFrame({'index':idx,'true':true_theta,'predicted': pred_theta})
        df.to_csv(outdir+'/'+testing_set[0]+'.csv', index = False)
    else:
        cor=stats.spearmanr(tf.math.exp(pred.squeeze()),tf.math.exp(Y_test)) # naive theta was computed when loading data
        print(config.Tasks[0]+" rho=",cor.statistic,"p=",cor.pvalue)
        df = pd.DataFrame({'index':idx,'true':tf.math.exp(Y_test.numpy().ravel()),'predicted': tf.math.exp(pred.squeeze())}) # pred and true are not in log scale
        df.to_csv(outdir+'/'+testing_set[0]+'.csv', index = False)

def loadCounts(counts_file_list,maxCases,config):
    linesRead=0
    lines=[]
    for chr_count in counts_file_list:
        IN=gzip.open(chr_count) if chr_count.endswith(".gz") else open(chr_count)
        header=IN.readline()
        if type(header) is bytes: header = header.decode("utf-8")
        if(not rex.find("DNA=([,\d]+)\s+RNA=([,\d]+)",header)):
            raise Exception("Can't parse counts file header: "+header)
        DNAreps=[int(x) for x in rex[1].split(",")]
        RNAreps=[int(x) for x in rex[2].split(",")]
        numTasks=len(DNAreps)

        for line in IN:
            if type(line) is bytes: line = line.decode("utf-8")
            fields=line.rstrip().split()
            # fields=[int(x) for x in fields]
            fields=[float(x) for x in fields]  # for normalized data
            if(config.useCustomLoss): lines.append(fields)
            else: lines.append(computeNaiveTheta(fields,DNAreps,RNAreps))  # for mse
            linesRead+=1
            if(linesRead>=maxCases): break
    lines=np.array(lines)
    print('number of counts: ',len(lines))
    return (DNAreps,RNAreps,lines)

def computeNaiveTheta(line,DNAreps,RNAreps):
    numTasks=len(DNAreps)
    a=0; rec=[]
    for i in range(numTasks):
        b=a+DNAreps[i]
        c=b+RNAreps[i]
        DNA=line[a:b] #+1
        RNA=line[b:c] #+1
        avgX=sum(DNA)/DNAreps[i]
        avgY=sum(RNA)/RNAreps[i]
        naiveTheta=avgY/avgX
        # sumX=sum(DNA)+1
        # sumY=sum(RNA)+1
        # naiveTheta=sumY/sumX
        rec.append(tf.math.log(naiveTheta))  # predicting log(theta), to be consistent with custom loss function
        a=c
    return rec

def loadModel(modeldir, testing_set):
    with open(modeldir + testing_set[0] +'.json', "r") as json_file:
        model_json = json_file.read()

    model = model_from_json(model_json)
    model.load_weights(modeldir + testing_set[0] + '.h5')
    model.summary()
    return model

def prepare_input(dataset,subdir,shouldRevComp,maxCases,config, set_name):
    # Convert sequences to one-hot encoding matrix
    if config.Tasks[0] == 'K562':
        fastas_file_list = [subdir+"/"+x+'-test.fasta' for x in dataset]
        counts_file_list = [subdir+"/"+x+"-test-counts.txt" for x in dataset]
    else:
        fastas_file_list = [subdir+"/"+x+'.fasta' for x in dataset]
        counts_file_list = [subdir+"/"+x+"-counts.txt" for x in dataset]
    input_fasta_data_A=loadFasta(fastas_file_list,uppercase=True,revcomp=shouldRevComp,
                                 stop_at=maxCases)
    sequence_length = len(input_fasta_data_A.sequence.iloc[0])
    seq_matrix_A = SequenceHelper.do_one_hot_encoding(input_fasta_data_A.sequence, sequence_length, SequenceHelper.parse_alpha_to_seq)
    X = np.nan_to_num(seq_matrix_A) # Replace NaN with 0 and inf w/big number
    X_reshaped = X.reshape((X.shape[0], X.shape[1], X.shape[2]))
    (DNAreps,RNAreps,Y)=loadCounts(counts_file_list,
                                   maxCases,config)
    global NUM_DNA
    global NUM_RNA
    NUM_DNA=DNAreps
    NUM_RNA=RNAreps
    matrix=pd.DataFrame(Y)
    matrix=tf.cast(matrix,tf.float32)
    idx=input_fasta_data_A.idx
    return (input_fasta_data_A.sequence, seq_matrix_A, X_reshaped, matrix, idx)

def loadFasta(fastas_file_list, as_dict=False,uppercase=False, stop_at=None,
              revcomp=False):
    fastas = []

    for chr_fasta in fastas_file_list:
        seq = None
        header = None
        for r in (gzip.open(chr_fasta) if chr_fasta.endswith(".gz") else open(chr_fasta)):
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
                         'idx': [e[0].split(' /coord')[0].split('>')[-1] for e in fastas],  # >7485398 /coord=chr10:47800-48100
                         'sequence': [e[1] for e in fastas]})



def naiveCorrelation(y_true, y_pred, taskNum, numTasks):
    a=0
    for i in range(taskNum): a+=NUM_DNA[i]+NUM_RNA[i]
    b=a+NUM_DNA[taskNum]
    c=b+NUM_RNA[taskNum]
    DNA=y_true[:,a:b]+1
    RNA=y_true[:,b:c]+1
    sumX=tf.reduce_sum(DNA,axis=1)
    sumY=tf.reduce_sum(RNA,axis=1)
    naiveTheta=sumY/sumX
    #print("naiveTheta=",naiveTheta)
    #print("y_pred=",tf.math.exp(y_pred[taskNum].squeeze()))
    cor=None
    if(numTasks==1):
        cor=stats.spearmanr(tf.math.exp(y_pred.squeeze()),naiveTheta)
    else:
        cor=stats.spearmanr(tf.math.exp(y_pred[taskNum].squeeze()),naiveTheta)
    return naiveTheta, y_pred.squeeze(), cor  # return raw input (theta)


#=========================================================================
#                         Command Line Interface
#=========================================================================
if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <parms.config> <data-subdir> <out:model-filestem>\n")
(configFile,subdir,modeldir,outdir)=sys.argv[1:]
main(configFile,subdir,modeldir,outdir)
