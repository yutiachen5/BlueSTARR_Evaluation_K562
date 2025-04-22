plots = function(df){
  par(mfrow=c(2,3), mar=c(3, 3, 1, 1), mgp=c(2, 1, 0))

  plot(df$rep2, df$rep3, main=paste("rho=",rho_cal(df$rep2, df$rep3)), xlab="Replicate2", ylab="Replicate3")
  abline(a=0, b=1, col="red")
  print(rho_cal(df$rep2, df$rep3))
  
  plot(df$rep2, df$rep4, main=paste("rho=",rho_cal(df$rep2, df$rep4)), xlab="Replicate2", ylab="Replicate4")
  abline(a=0, b=1, col="red")
  print(rho_cal(df$rep2, df$rep4))
  
  plot(df$rep2, df$rep5, main=paste("rho=",rho_cal(df$rep2, df$rep5)), xlab="Replicate2", ylab="Replicate5")
  abline(a=0, b=1, col="red")
  print(rho_cal(df$rep2, df$rep5))

  plot(df$rep3, df$rep4, main=paste("rho=",rho_cal(df$rep3, df$rep4)), xlab="Replicate3", ylab="Replicate4")
  abline(a=0, b=1, col="red")
  print(rho_cal(df$rep3, df$rep4))
  
  plot(df$rep3, df$rep5, main=paste("rho=",rho_cal(df$rep3, df$rep5)), xlab="Replicate3", ylab="Replicate5")
  abline(a=0, b=1, col="red")
  print(rho_cal(df$rep3, df$rep5))
  
  plot(df$rep4, df$rep5, main=paste("rho=",rho_cal(df$rep4, df$rep5)), xlab="Replicate4", ylab="Replicate5")
  abline(a=0, b=1, col="red")
  print(rho_cal(df$rep4, df$rep5))
  
}

rho_cal = function(x,y){
  return (round(cor(x,y,method = "spearman"),2))
}

read_data = function(dir,data){
  header = c('DNA1','DNA2','DNA3','DNA4','DNA5','RNA2','RNA3','RNA4','RNA5')
  df = read.table(gzfile(dir), sep="\t", skip=1, header=FALSE, col.names=header)
  num_dna = 5
  
  # DNA
  input1_size = 447623565
  input2_size = 418854359
  input3_size = 421697434
  input4_size = 496906399
  input5_size = 410434753

  # RNA
  TFX2_Dex = 45413539
  TFX2_DMSO = 43844606
  TFX3_Dex = 26400671 
  TFX3_DMSO = 26819569
  TFX4_Dex = 34590086 
  TFX4_DMSO = 30951533 
  TFX5_Dex = 42310249 
  TFX5_DMSO = 28859151 

  # normalize counts
  c = 1000000
  df$DNA1 = df$DNA1/input1_size
  df$DNA2 = df$DNA2/input2_size
  df$DNA3 = df$DNA3/input3_size
  df$DNA4 = df$DNA4/input4_size
  df$DNA5 = df$DNA5/input5_size
  
  if (data == 'DMSO'){
    df$RNA2 = df$RNA2/TFX2_DMSO*c
    df$RNA3 = df$RNA3/TFX3_DMSO*c
    df$RNA4 = df$RNA4/TFX4_DMSO*c
    df$RNA5 = df$RNA5/TFX5_DMSO*c
  }
  else{
    df$RNA2 = df$RNA2/TFX2_Dex*c
    df$RNA3 = df$RNA3/TFX3_Dex*c
    df$RNA4 = df$RNA4/TFX4_Dex*c
    df$RNA5 = df$RNA5/TFX5_Dex*c
  }

  df$DNA_aver = (df$DNA1+df$DNA2+df$DNA3+df$DNA4+df$DNA5)/num_dna
  df$rep2 = df$RNA2/df$DNA_aver
  df$rep3 = df$RNA3/df$DNA_aver
  df$rep4 = df$RNA4/df$DNA_aver
  df$rep5 = df$RNA5/df$DNA_aver
  subset = df[1:10000,]
  #subset = df
  return (subset)
}


# dir = "/datacommons/igvf-pm/A549/processed-data/600-bases/DMSO-200/DMSO-200-all-normalized-counts.txt"
# df = read_data(dir,'DMSO')
# pdf("/datacommons/igvf-pm/A549/full-set/DMSO-200/600-bases/data-normalized/between-rep-exp-DMSO-200-test.pdf")
# plots(df)

dir = "/hpc/group/igvf/A549/full-set/Dex-200/300-bases/data-normalized/train-counts.txt.gz"
df = read_data(dir,'Dex')
# pdf("/datacommons/igvf-pm/A549/full-set/Dex-200/600-bases/data-normalized/between-rep-exp-Dex-200-test.pdf")
plots(df)




  
