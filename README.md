### Bulk_RNA Analysis workflow
This repository provides a complete end-to-end workflow for Bulk RNA-Seq data analysis — from preprocessing and alignment to differential expression analysis and visualization. The pipeline integrates industry-standard bioinformatics tools for reliable and reproducible transcriptomic analysis.

📁 Repository Structure

Bulk-RNAseq-Analysis/


├── Bulk_RNA Analysis.py    
├── DEseq2.R                 
└── README.md               

Step-by-Step Workflow

## Environment Setup

Set up a dedicated Conda environment for RNA-Seq analysis.
Install required tools (e.g., FastQC, fastp, MultiQC, HISAT2, SAMtools, StringTie, etc.) through the Bioconda channel.
Ensures reproducibility and dependency isolation.

## Quality Control (QC)

Perform initial QC on raw FASTQ files using FastQC to assess read quality, GC content, and adapter contamination.
Results are summarized using MultiQC for easy comparison across samples.

## Adapter Trimming and Filtering

Use fastp for adapter trimming, quality filtering, and base correction.
Generates both JSON and HTML reports summarizing trimming statistics.
Output files are clean, high-quality reads ready for alignment.

## Reference Genome Preparation

Download and decompress the GRCh38 human reference genome and GENCODE v36 annotation file.
Build a HISAT2 genome index for efficient alignment.

## Alignment

Align trimmed reads to the indexed reference genome using HISAT2.
Output is generated in SAM format, representing read-to-genome alignments.

## File Conversion and Sorting

Convert SAM to BAM (binary alignment format) using SAMtools for efficient storage.
Sort BAM files by genomic coordinates and index them for quick access and visualization in genome browsers.

## Transcript Assembly and Quantification

Assemble transcripts and estimate expression levels using StringTie.
Generates sample-specific GTF files with transcript-level abundance estimates.
The assembled transcripts can be merged later for cross-sample comparison.

## Gene-Level Count Generation

Use HTSeq-count to quantify the number of reads per transcript/gene.
The count data serves as input for differential expression analysis in R.

## Differential Expression Analysis (R Script)

Conduct downstream statistical analysis using DESeq2 in R.
Integrates results from tximport to combine transcript-level data into gene-level counts.
Performs normalization, statistical testing, and visualization of differentially expressed genes (DEGs).
Optionally, use biomaRt for gene annotation and mapping to biological pathways.



## Tools and Packages Used

| Category                | Tool / Package            | Purpose                                  |
| ----------------------- | ------------------------- | ---------------------------------------- |
| Environment             | Anaconda, Bioconda        | Dependency management                    |
| QC & Trimming           | FastQC, fastp, MultiQC    | Quality control and trimming             |
| Alignment               | HISAT2, SAMtools          | Read mapping and file handling           |
| Quantification          | StringTie, HTSeq          | Transcript assembly and count generation |
| Differential Expression | DESeq2, tximport, biomaRt | Gene-level analysis and annotation       |

## Output Summary

| Step      | Output File                  | Description                              |
| --------- | ---------------------------- | ---------------------------------------- |
| FastQC    | `.html`, `.zip`              | Quality reports                          |
| fastp     | `.trimmed.fastq.gz`, `.html` | Cleaned reads                            |
| HISAT2    | `.sam`, `.bam`, `.bai`       | Aligned and indexed reads                |
| StringTie | `.gtf`                       | Transcript-level abundance               |
| HTSeq     | `.txt`                       | Count matrix                             |
| DESeq2    | `.csv`, `.pdf`               | Differentially expressed genes and plots |


