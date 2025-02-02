#After installing Anaconda 

source ~/.bashrc
conda --version

#Create and activate the RNA-seq environment:

conda create -n RNA-seq
conda activate RNA-seq


Step 2: Install the RNA-seq Tools

conda install -n RNA-seq -c bioconda fastqc
conda install -n RNA-seq -c bioconda fastp
conda install -n RNA-seq -c bioconda multiqc
conda install -n RNA-seq -c bioconda star
conda install -n RNA-seq -c bioconda samtools
conda install -n RNA-seq -c bioconda deeptools
conda install -n RNA-seq -c bioconda salmon

#Navigate to the Directory Containing Your Files
cd /mnt/c/Users/Lenovo/Documents/RNA_seq

#Create a directory for fastqc report 
mkdir fasctqc_reports 

1. Run FastQC on Your Files
fastqc SRR1039508_1.fastq.gz SRR1039508_2.fastq.gz -o ./fastqc_reports

2. Trimming 
fastp -i /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_1.fastq.gz -I 

/mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_2.fastq.gz \
  -o /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_1.trimmed.fastq.gz -O /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_2.trimmed.fastq.gz \
  --detect_adapter_for_pe -l 25 -j /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508.fastp.json -h /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508.fastp.html

3.Alignment
##Download the reference genome
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
##Download the gene annotation file (GTF):  will also need the gene annotation in .gtf format, which is typically available from sources like GENCODE.download the GENCODE v36 annotation file:
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_36/gencode.v36.annotation
##Decompress the above files 
gunzip /mnt/c/Users/Lenovo/Documents/RNA_seq/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
gunzip /mnt/c/Users/Lenovo/Documents/RNA_seq/gencode.v36.annotation.gtf.gz

Download the HITSAT2 
sudo apt-get update
sudo apt-get install hisat2

##Create Directory for Index Files:
mkdir -p /mnt/c/Users/Lenovo/Documents/RNA_seq/genome_index
##Build Genome Index:
##Run the hisat2-build command to generate the index:
hisat2-build /mnt/c/Users/Lenovo/Documents/RNA_seq/GCA_000001405.15_GRCh38_no_alt_analysis_
##Align RNA-seq Reads to the Reference Genome Using HISAT2
hisat2 -p 4 --dta -x /mnt/c/Users/Lenovo/Documents/RNA_seq/genome_index/GRCh38_no_alt \
       -1 /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_1.trimmed.fastq.gz \
       -2 /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_2.trimmed.fastq.gz \
       -S /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_aligned.sam

4.Convert SAM to BAM
SAM files are large and can be inefficient to work with, so it's common to convert them to BAM format. BAM is a binary format that is more efficient for storage and processing.
samtools view -bS /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_aligned.sam > /mnt/c/Users/L

5.Sort BAM File
#BAM files must be sorted by genomic coordinates (or read names) before they can be used in many downstream tools, like StringTie.
samtools sort /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_aligned.bam -o /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_sorted.bam

This will produce a sorted BAM file (SRR1039508_sorted.bam).

6.Index the Sorted BAM File
#Indexing the BAM file allows tools to quickly access specific reads based on their genomic coordinates.
samtools index /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_sorted.bam
This will create an index file (SRR1039508_sorted.bam.bai), which is needed for visualization and downstream analysis.

7.Transcript Assembly and Quantification Using StringTie
Now that your BAM file is sorted and indexed, you can use StringTie for transcript assembly and gene expression quantification. This step will generate a .gtf file containing the reconstructed transcript annotations.

Sudo apt install stringtie
ls /mnt/c/Users/Lenovo/Documents/RNA_seq/gencode.v36.annotation.gtf
stringtie /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_sorted.bam \
-o /mnt/c/Users/Lenovo/Documents/RNA_seq/SRR1039508_transcripts.gtf \
-G /mnt/c/Users/Lenovo/Documents/RNA_seq/gencode.v36.annotation.gtf \
-eB

