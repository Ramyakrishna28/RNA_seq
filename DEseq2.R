#Generation of the counts:
#The command you provided is for quantifying gene or transcript expression by counting the number of aligned reads from your BAM file that overlap with features in the GTF file
sudo apt install python3-htseq
htseq-count -f bam -r pos -s no -t transcript -i transcript_id \  /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_sorted.bam \ /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_transcripts.gtf > transcript_counts.txt

# Install DESeq2 and tximport (for quantification)
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("DESeq2")
BiocManager::install("tximport")
BiocManager::install("biomaRt")

# Load necessary libraries
library(DESeq2)
library(tximport)
library(biomaRt)

install.packages("readr")
install.packages("dplyr")
BiocManager::install("tximport")
library(tximport)


setwd("C:/Users/Lenovo/Documents/RNA_seq")  # Set the correct directory path
tmp <- read_tsv("t_data.ctab")
# Create the tx2gene mapping (transcript -> gene)
tx2gene <- tmp[, c("t_name", "gene_name")]
# Load the necessary library
library(readr)
# View the first few rows of tx2gene to ensure it looks correct
head(tx2gene)


library(tximport)
# Specify the file paths to your `t_data.ctab` files (adjust the paths based on your system)
files <- c("t_data.ctab")
# Import the data using tximport
txi <- tximport(files, type = "stringtie", tx2gene = tx2gene)


