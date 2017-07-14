# genomewide_annotation
Given a bed file, annotate each position of the given regions in allele-specific manner (but not strand-specific) and generate TSV file. For further usage, it also provides scripts to convert TSV to BED by applying some customized filtering rules.

## Overview

The pipeline can be divided into four major modules:

  1. **BED2Input**: Given a genome-wide BED file, split it into chunks for downstream analysis and generate input list. The format is determined by the annotation method downstream. In the current annotation methods, it should contain all possible SNVs.
  2. **Input2Score**: This module is annotation-method-specific. For each annotation method, it is expected to take some input format (SNV in current version) and output four scores for all possible alleles at a position.
  3. **Score2TSV**: Convert the score per allele to score per SNV (reference + alternative allele).
  4. **TSV2BED**: Determine if a position is positive or negative by user-specified rules and generate the corresponding BED file.

## BED2Input

Split part is shared across different downstream calculation but user can specify the input format.

## Input2Score

For each annotation method, it will work in an independent directory and even work collaboratively with other pipeline. The naming convention is `input2score-[name]`.

**Caution**: The standard format of score indicates reference allele information by setting the first allele as reference allele.

## Score2TSV

It is shared across methods. Convert the score (for each position + allele pair, it has a score) to the score for each possible SNV. It allows customized converting function but it should be general enough to minimize the method-specificity. Say, only involve the basic calculation between reference and alternative, i.e. subtract, divide

## TSV2BED

Convert TSV to BED by applying customized filtering rules. It should be general but not method-specific.
