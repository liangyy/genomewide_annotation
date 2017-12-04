library(optparse)

option_list <- list(
  make_option(c("-s", "--score"), type="character", default=NULL,
              help="score to correct",
              metavar="character"),
  make_option(c("-r", "--reference"), type="character", default=NULL,
              help="reference model in RDS",
              metavar="character"),
  make_option(c("-o", "--output"), type="character", default=NULL,
              help="output file name",
              metavar="character")
)

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

library(stringr)
library(dplyr)

# score to be corrected
data <- read.table(opt$score, sep = '\t', header = F)

v11.good <- is.na(str_match(data$V7, '[ATGC]'))
v11.strategy1 <- str_match(data$V7, '(.+),(.+),(.+),(.+)')
v12.good <- is.na(str_match(data$V8, '[ATGC]'))
v12.strategy1 <- str_match(data$V8, '(.+),(.+),(.+),(.+)')
strategy1 <- v11.strategy1
strategy1[v12.good, ] <- v12.strategy1[v12.good, ]
# strategy1 <- str_match(data$V12, '(.+),.+,.+,.+')
strategy1 <- strategy1[, 2 : 5]
class(strategy1) <- 'numeric'
corrected <- matrix(0, nrow = nrow(strategy1), ncol = 4)

# load reference model
model <- readRDS(opt$reference)
for (i in names(model)) {
  model.sub <- model[[i]]
  ind.sub <- data$V5 == i
  strategy1.sub <- strategy1[ind.sub, ]
  corrected.sub <- matrix(0, nrow = nrow(strategy1.sub), ncol = 4)
  for (j in 1 : 4){
    corrected.sub[, j] <- predict(model.sub, data.frame(strategy1 = strategy1.sub[, j]))
  }
  corrected[ind.sub, ] <- corrected.sub
}

corrected_str <- apply(corrected, 1, function(x) {paste(x, collapse = ',')})
data[,'V7'] <- as.character(data[,'V7'])
data[,'V8'] <- as.character(data[,'V8'])
data[v11.good, 'V7'] <- corrected_str[v11.good]
data[v12.good, 'V8'] <- corrected_str[v12.good]

gz <- gzfile(opt$output, 'w')
write.table(data, gz, sep = '\t', quote = F, col.names = F, row.names = F)
close(gz)
