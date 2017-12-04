library(optparse)

option_list <- list(
  make_option(c("-r", "--reference"), type="character", default=NULL,
              help="reference scores",
              metavar="character"),
  make_option(c("-o", "--output"), type="character", default=NULL,
              help="output file name",
              metavar="character")
)

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

library(stringr)
library(dplyr)

data <- read.table(opt$reference, sep = '\t', header = F)

v11.good <- is.na(str_match(data$V14, '[ATGC]'))
v11.strategy1 <- str_match(data$V14, '(.+),.+,.+,.+')
v12.good <- is.na(str_match(data$V15, '[ATGC]'))
v12.strategy1 <- str_match(data$V15, '(.+),.+,.+,.+')
strategy1 <- v11.strategy1
strategy1[v12.good, ] <- v12.strategy1[v12.good, ]
# strategy1 <- str_match(data$V12, '(.+),.+,.+,.+')
strategy1 <- strategy1[, 2]
class(strategy1) <- 'numeric'
data <- data.frame(strategy1 = strategy1, centisnp = data$V7, motif = data$V4, position = data$V2, strand = data$V6)
data <- unique(data)
motifs <- unique(data$motif)

model <- list()
for (i in motifs) {
    data.sub <- data[data$motif == i, ]
    model.sub <- lm(centisnp ~ strategy1, data = data.sub)
    model[[i]] <- model.sub
}
saveRDS(object = model, file = opt$output)
