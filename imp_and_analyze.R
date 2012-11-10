statistics_blogs <- read.csv("~/Dropbox/classes/sna/project/out/statistics_blogs.csv")
blog_clus <- read.delim("~/Dropbox/classes/sna/project/out/blog_clus.txt", header=F)

all_data <- merge(statistics_blogs,blog_clus,by.x="Id",by.y="V2")

with(all_data,chisq.test(V1,Modularity.Class))
with(all_data,table(V1,Modularity.Class))