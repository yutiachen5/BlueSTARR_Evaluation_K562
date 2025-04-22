
pdf("/work/igvf-pm/A549/extra_GCs/AZD2906/unbiased_vs_biased_thetas.pdf")
df1 <- read.table("/work/igvf-pm/A549/extra_GCs/AZD2906/unbiased-normalized-thetas.txt",header=F)
df2 <- read.table("/work/igvf-pm/A549/extra_GCs/AZD2906/biased-normalized-thetas.txt",header=F)


max_y = max(density(log2(df1$V1))$y, density(log2(df2$V1))$y)
max_x = max(density(log2(df1$V1))$x, density(log2(df2$V1))$x)
min_x = min(density(log2(df1$V1))$x, density(log2(df2$V1))$x)

plot(density(log2(df1$V1)), lwd = 3, lty = 1, col = "lightblue", 
     xlab = "log2 Theta", main = 'biased vs unbaised downsampling for AZD2906', 
     ylim = c(0, max_y), xlim = c(min_x, max_x))
lines(density(log2(df2$V1)), lwd = 3, lty = 1, col = "orange")    
legend("topright", legend = c("unbiased","biased"), col = c("lightblue", "orange"), lwd = 2)
