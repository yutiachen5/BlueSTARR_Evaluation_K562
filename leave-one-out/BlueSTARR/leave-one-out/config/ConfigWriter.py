def write_custom_config(subdir, config, chr_ls):
    for i in range(len(chr_ls)):
        filename = subdir+"chr"+str(chr_ls[i])+'.config'
        with open(filename, 'w') as file:
            if i != len(chr_ls)-1:
                tmp = [x for x in chr_ls if x != chr_ls[i] and x!= chr_ls[i+1]]
                train = ','.join(list(map(lambda x: f"chr{x}", tmp)))
                config['TrainData']=train
                config['TestData']='chr'+ str(chr_ls[i])
                config['ValidationData']='chr'+str(chr_ls[i+1])
            else:
                tmp = [x for x in chr_ls if x != chr_ls[i] and x!= chr_ls[0]]
                train = ','.join(list(map(lambda x: f"chr{x}", tmp)))
                config['TrainData']=train
                config['TestData']='chr'+ str(chr_ls[i])
                config['ValidationData']='chr'+str(chr_ls[0])
            for key, value in config.items():
                file.write(f"{key} = {value}\n")

config = {
    'UseCustomLoss': '1',
    'Tasks': 'A549',
    'TaskWeights': '1',
    'Verbose': '2',
    'NumConvLayers': '5',
    'KernelSizes': '8,16,32,64,128',
    'NumKernels': '1024,512,256,128,64',
    'MaxTrain': '3000000',
    'MaxTest': '999999999',
    'ShouldTest': '1',
    'Epochs': '200',
    'RevComp': '0',
    'BatchSize': '128',
    'EarlyStop': '10',
    'DropoutRate': '0.5',
    'LearningRate': '0.002',
    'ConvResidualSkip': '0',
    'ConvDropout': '1',
    'ConvPad': 'same',
    'DilationFactor': '1',
    'ConvPoolSize': '1',
    'GlobalMaxPool': '0',
    'GlobalAvePool': '1',
    'NumDense': '0',
    'DenseSizes': '0',
    'NumAttentionLayers': '0',
    'AttentionHeads': '0',
    'AttentionKeyDim': '0',
    'AttentionResidualSkip': '0'
}

attention_config = {
    'UseCustomLoss': '0',
    'Tasks': 'K562',
    'TaskWeights': '1',
    'Verbose': '2',
    'NumConvLayers': '0',
    'KernelSizes': '8,16,32,64,128',
    'NumKernels': '1024,512,256,128,64',
    'MaxTrain': '3000000',
    'MaxTest': '999999999',
    'ShouldTest': '1',
    'Epochs': '200',
    'RevComp': '0',
    'BatchSize': '128',
    'EarlyStop': '10',
    'DropoutRate': '0.5',
    'LearningRate': '0.002',
    'ConvResidualSkip': '0',
    'ConvDropout': '1',
    'ConvPad': 'same',
    'DilationFactor': '1',
    'ConvPoolSize': '1',
    'GlobalMaxPool': '0',
    'GlobalAvePool': '1',
    'NumDense': '0',
    'DenseSizes': '0',
    'NumAttentionLayers': '5',
    'AttentionHeads': '8,8,8,16,32',
    'AttentionKeyDim': '8,8,8,16,32',
    'AttentionResidualSkip': '0'
}

chr_ls = [x for x in range(1,23)]+["X","Y"]
# write_custom_config('/datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_', config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/A549/leave-one-out/config/A549_', config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/K562/leave-one-out/config-mse/K562_', config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-custom/A549_', config, chr_ls)
write_custom_config('/datacommons/igvf-pm/K562/leave-one-out/attention-layer/config/K562_', attention_config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-mse/A549_', config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/config-mse/A549_', config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-custom/A549_', config, chr_ls)
# write_custom_config('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/config-custom/A549_', config, chr_ls)
