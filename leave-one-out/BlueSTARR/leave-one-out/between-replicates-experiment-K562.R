
plots = function(df, outfile){
  pdf(outfile, width=7, height=5)  # Open PDF inside the function
  par(mfrow=c(1,3), mar=c(3, 3, 1, 1), mgp=c(2, 1, 0))

  plot(df$rep1, df$rep2, main=paste("rho=",rho_cal(df$rep1, df$rep2)), xlab="Replicate1", ylab="Replicate2")
  abline(a=0, b=1, col="red")

  plot(df$rep1, df$rep3, main=paste("rho=",rho_cal(df$rep1, df$rep3)), xlab="Replicate1", ylab="Replicate3")
  abline(a=0, b=1, col="red")

  plot(df$rep2, df$rep3, main=paste("rho=",rho_cal(df$rep2, df$rep3)), xlab="Replicate2", ylab="Replicate3")
  abline(a=0, b=1, col="red")

  dev.off()  # Close PDF device
}

rho_cal = function(x,y){
  print(round(cor(x,y,method = "spearman"),2))
  return (round(cor(x,y,method = "spearman"),2))
}

read_data = function(dir){
  header = c('DNA1','DNA2','DNA3','RNA1','RNA2','RNA3')
  df = read.table(gzfile(dir), sep="\t", skip=1, header=FALSE, col.names=header)
  num_dna = 3

  #DNA
  input_rep1 = 123384250
  input_rep2 = 130680200
  input_rep3 = 134539576

  #RNA
  output_rep1 = 116270841
  output_rep2	= 217503220
  output_rep3	= 219086330

  # normalize counts
  c = 1000000
  df$DNA1 = df$DNA1/input_rep1
  df$DNA2 = df$DNA2/input_rep2
  df$DNA3 = df$DNA3/input_rep3
  df$RNA1 = df$RNA1/output_rep1*c
  df$RNA2 = df$RNA2/output_rep2*c
  df$RNA3 = df$RNA3/output_rep3*c
  

  df$DNA_aver = (df$DNA1+df$DNA2+df$DNA3)/num_dna
  df$rep1 = df$RNA1/df$DNA_aver
  df$rep2 = df$RNA2/df$DNA_aver
  df$rep3 = df$RNA3/df$DNA_aver
  subset = df[1:10000,]
  return (subset)
}



dir = "/work/igvf-pm/K562/full-set/600bp/data-normalized/all-counts.txt.gz"

df = read_data(dir)
plots(df, "/work/igvf-pm/K562/full-set/600bp/data-normalized/between-replicates-experiment-K562.pdf")
