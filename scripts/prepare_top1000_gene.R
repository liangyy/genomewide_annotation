bed <- read.table('data/refseq_id_promoter_1kb_upstream_pair_table.txt', sep = '\t', header = F)
map <- read.table('data/ref_id_to_genename_table.txt', sep = '\t')
gene <- read.table('data/Example_gene_coding_BF.txt', sep = '\t', header = T)

MatchRefseqidWithGenename <- function(refseqid, genename, refseqid.selected) {
  refseqid.selected.idx <- match(refseqid.selected, refseqid)
  return(genename[refseqid.selected.idx])
}

bed$genename <- MatchRefseqidWithGenename(map$V1, map$V2, bed$V4)
gene.ordered <- gene[order(gene$coding_BF, decreasing = T), 'genename']
gene.top.1000 <- gene.ordered[1 : 1000]

ExtractedRegionByGenename <- function(genename, region, genename.selected) {
  region.selected.idx <- which(genename %in% genename.selected)
  return(region[region.selected.idx, ])
}

bed.top.1000 <- ExtractedRegionByGenename(bed$genename, bed, gene.top.1000)

ExtendDownstream <- function(x) {
  if (x[5] == '+') {
    x[3] <- as.numeric(x[3]) + 1000
  } else {
    x[2] <- as.numeric(x[2]) - 1000
  }
  return(x)
}
bed.top.1000.extend <- apply(bed.top.1000, 1, ExtendDownstream)
bed.top.1000.extend <- as.data.frame(t(bed.top.1000.extend))
write.table(x = bed.top.1000.extend, 'data/refseq_id_promoter_1kb_upstream_downstream_pair_table_top1000_gene.txt', row.names = F, col.names = F, quote = F, sep = '\t')
