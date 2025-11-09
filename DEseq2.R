#Generation of the counts:
#The command you provided is for quantifying gene or transcript expression by counting the number of aligned reads from your BAM file that overlap with features in the GTF file
sudo apt install python3-htseq
htseq-count -f bam -r pos -s no -t transcript -i transcript_id \  /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_sorted.bam \ /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_transcripts.gtf > transcript_counts.txt

# ================================================================
#Install and Load Required Packages

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("DESeq2", "tximport", "biomaRt"))
install.packages(c("readr", "dplyr"))

library(DESeq2)
library(tximport)
library(biomaRt)
library(readr)
library(dplyr)


 # Import Transcript Quantification Data
setwd("C:/Users/Lenovo/Documents/RNA_seq")

# Example: Load one t_data.ctab file to extract tx2gene mapping
tmp <- read_tsv("t_data.ctab")

# Create transcript-to-gene mapping
tx2gene <- tmp[, c("t_name", "gene_name")]

# List your StringTie output files (replace with your sample paths)
files <- c("control1/t_data.ctab",
           "control2/t_data.ctab",
           "disease1/t_data.ctab",
           "disease2/t_data.ctab")

# Import transcript-level abundance data
txi <- tximport(files, type = "stringtie", tx2gene = tx2gene)

Create Metadata (Sample Information)
# Each sample corresponds to a condition (e.g., Control vs Disease)
sample_info <- data.frame(
  row.names = c("control1", "control2", "disease1", "disease2"),
  condition = c("Control", "Control", "Disease", "Disease")
)


#Create DESeq2 Dataset and Pre-filter Low Counts
dds <- DESeqDataSetFromTximport(txi, colData = sample_info, design = ~ condition)

# Pre-filter genes with very low counts (to remove noise)
dds <- dds[rowSums(counts(dds)) > 10, ]   # can adjust threshold


#Run DESeq2 Differential Expression Analysis
dds <- DESeq(dds)

# Obtain results (Control vs Disease)
res <- results(dds)

# Order results by adjusted p-value (FDR)
res <- res[order(res$padj), ]


# Post-filtering: Select Significant DE Genes
# Apply adjusted p-value and log2 fold change thresholds
resSig <- subset(res, padj < 0.05 & abs(log2FoldChange) > 1)

# View top significant genes
head(resSig)

# Save full and filtered results
write.csv(as.data.frame(res), "DESeq2_results_all.csv")
write.csv(as.data.frame(resSig), "DESeq2_results_significant.csv")


 Annotate DE Genes with Gene Symbols
mart <- useDataset("hsapiens_gene_ensembl", useMart("ensembl"))

gene_annots <- getBM(
  attributes = c("ensembl_gene_id", "hgnc_symbol", "description"),
  filters = "ensembl_gene_id",
  values = rownames(resSig),
  mart = mart
)

# Merge annotations with significant DE results
annotated_res <- merge(as.data.frame(resSig), gene_annots,
                       by.x = "row.names", by.y = "ensembl_gene_id", all.x = TRUE)

write.csv(annotated_res, "DESeq2_results_significant_annotated.csv", row.names = FALSE)


#Visualization 
# MA Plot
plotMA(res, main = "DESeq2 - MA Plot", ylim = c(-5, 5))

# Volcano Plot
with(res, plot(log2FoldChange, -log10(padj), pch=20, main="Volcano Plot",
               xlim=c(-6,6)))
abline(h=-log10(0.05), col="red", lty=2)
abline(v=c(-1,1), col="blue", lty=2)


