# Comparative Analysis of Drug-Related Genetic Variant Frequencies Across Populations

## Project Overview

This project investigates allele frequency differences in variants known to affect drug response, comparing major populations using data from the [gnomAD v4 database](https://gnomad.broadinstitute.org/downloads). The data-driven approach includes preprocessing of large `.vcf.gz` files, extracting relevant pharmacogenomic variants, and visualizing allele frequency differences — with a focus on how population genetics may influence drug efficacy.

---

## Goals & Workflow

### Goal 1: Preprocessing gnomAD Data

**Description:**  
gnomAD v4 variant files are extremely large and contain excessive information. The key data of interest — allele frequencies — are stored in the `INFO` column of the VCF format (column 8).

**Solution:**  
A custom C++ script, `shrink_vcf.cpp`, was developed to extract only necessary INFO fields (e.g., allele frequency per population). It reads from standard input and outputs streamlined VCF data. This reduced memory usage significantly, allowing storage and processing on machines with limited disk space.

A `Makefile` rule automates this process when raw data is present. The preprocessed files are not included in this repository due to size, but the method is reproducible by running:

```bash
make
```

### Goal 2: Visualizing Population Data as a Matrix

**Description:**  
The aim was to visualize allele frequencies per variant across populations in a matrix-style layout, with rows as populations and columns as genomic positions.

**Solution:**  
JBrowse2 could not support this style for gnomAD summary data, since it’s designed for sample-based datasets. IGV (Integrative Genomics Viewer) was used instead, by splitting VCFs by population and loading them as tracks. Changing the display mode to `COLLAPSED` allowed simultaneous view of all populations.

**Population codes used:**

- `AFR` – African/African American  
- `AMR` – Admixed American  
- `ASJ` – Ashkenazi Jewish  
- `EAS` – East Asian  
- `FIN` – Finnish  
- `NFE` – Non-Finnish European  
- `SAS` – South Asian  
- `REMAINING` – Other / unassigned  

Variants are color-coded in IGV based on allele frequency, which provided a useful approximation of a heatmap/matrix.

---

### Goal 3: Extracting Drug-Associated Variants

**Description:**  
Only specific variants known to affect drug response (listed in `rs_dbsnp_joined.tsv`) were of interest for downstream analysis.

**Solution:**  
The script `collect_freqs_select.py` filters preprocessed VCFs and extracts allele frequencies for only those pharmacogenomic variants, grouped by population.

**Execution example:**

```bash
zcat *.vcf.gz | pypy3 collect_freqs_select.py
```
Or using Make:
```bash
make collect
```
Note: Python scripts were executed with PyPy3 for better performance on large data.

### Goal 4: Comparing Non-Finnish Europeans to Other Populations

**Description:**  
The goal was to quantify and visualize the difference in allele frequencies between the Non-Finnish European (NFE) population and others for drug-relevant variants.

**Solution:**  
The script collect_freqs_bg.py computes absolute differences in allele frequencies between NFE and each other population, generating .bedGraph files: nfe-vs-{}.bedGraph.
These files can be loaded into IGV to visualize population-specific allele frequency divergence across the genome.

### Example findings

#### Chromosome X

- **Loc 45,781,104-45,781,104**  
  **Variant:** T vs C  
  **Associated Drugs:** Cisplatin, Fluorouracil, Mitoxantrone  
  **Condition:** Hepatocellular carcinoma  
  **Insight:** Allele C is significantly more frequent in East/South Asian, African, and American populations than in Non-Finnish Europeans. Thus, these drugs are more effective in Europeans and may be less effective in other populations.

- **Loc 123,183,391-123,183,391**  
  **Genotype:** TT vs CC + CT  
  **Drug:** SSRIs or Venlafaxine  
  **Condition:** Major Depressive Disorder  
  **Insight:** The C allele is less frequent in Non-Finnish Europeans. Most Europeans have the TT genotype, making treatment with these antidepressants less effective in this population.

---

#### Chromosome 22

- **Loc 41,682,662-41,682,662**  
  **Variant:** G vs A  
  **Drug:** Vincristine  
  **Conditions:** Various childhood cancers (e.g., Glioma, Medulloblastoma)  
  **Insight:** G allele is more frequent in Non-Finnish Europeans (and East Asians), indicating that checking vincristine concentrations is more relevant in Europe.

---

#### Chromosome 19

- **Loc 13,410,714-13,410,714**  
  **Variant:** G vs A  
  **Drug:** Antiepileptics  
  **Condition:** Epilepsy  
  **Insight:** G allele is less frequent in Europeans; majority have AA genotype, indicating better resistance to antiepileptics.

- **Loc 11,333,455-11,333,455**  
  **Variant:** G vs C  
  **Drug:** Platinum compounds  
  **Condition:** Lung Neoplasms  
  **Insight:** G allele is more common in Europeans (except Ashkenazi Jews). This may hinder drug response.

---

#### Chromosome 18

- **Loc 58,227,849-58,227,849**  
  **Variant:** C vs G  
  **Drug:** Hydrochlorothiazide  
  **Condition:** Hypertension  
  **Insight:** G allele is less common in Europeans; drug is more effective in this population.

- **Loc 58,792,367-58,792,367**  
  **Variant:** G vs A  
  **Drug:** Cyclosporine  
  **Condition:** Psoriasis  
  **Insight:** G allele is more frequent in Non-Finnish Europeans than in Africans, Asians, or even Finnish Europeans.

- **Loc 4,970,507-4,970,507**  
  **Variant:** C vs A  
  **Drug:** SSRIs  
  **Condition:** Major Depressive Disorder  
  **Insight:** C allele is more frequent in Non-Finnish Europeans, potentially reducing effectiveness of SSRIs.

---

#### Chromosome 17

- **Loc 61,406,405-61,406,405**  
  **Variant:** C vs T  
  **Drug:** Atenolol  
  **Condition:** Hypertension  
  **Insight:** C allele is less frequent in Europeans; T is more frequent, suggesting atenolol is effective.

- **Loc 63,488,670-63,488,670**  
  **Genotype:** GG vs others  
  **Drug:** Sertraline  
  **Condition:** Major Depressive Disorder  
  **Insight:** A allele is less common in Europeans; majority have GG genotype, suggesting low drug response.

- **Loc 46,024,197-46,024,197**  
  **Variant:** C vs T  
  **Drug:** Corticosteroids  
  **Condition:** Asthma  
  **Insight:** C allele is frequent in Europeans (second only to Jewish population). May reduce treatment effectiveness.

---

#### Chromosome 16

- **Loc 1,202,369-1,202,369**  
  **Variant:** T vs C  
  **Drug:** Ethosuximide  
  **Condition:** Epilepsy  
  **Insight:** T allele is less frequent in Europeans; drug is more effective.

- **Loc 1,220,162-1,220,162**  
  **Variant:** A vs G  
  **Drug:** Antiepileptics  
  **Condition:** Epilepsy  
  **Insight:** A allele is least frequent in Europeans, suggesting greater drug resistance.

---

#### Chromosome 15

- **Loc 45,253,280-45,253,280**  
  **Variant:** T vs C  
  **Drug:** Tenofovir  
  **Condition:** HIV  
  **Insight:** T allele is most frequent in Europeans, increasing pharmacokinetic risks.

- **Loc 45,262,069-45,262,069**  
  **Genotype:** AA vs AC + CC  
  **Drug:** Gemcitabine  
  **Condition:** Pancreatic Neoplasms  
  **Insight:** A allele is highly frequent in Europeans; treatment may be less effective.

- **Loc 74,785,026-74,785,026**  
  **Variant:** C vs A  
  **Drug:** Hydrochlorothiazide  
  **Condition:** Hypertension  
  **Insight:** T allele (likely typo for C) is most frequent in Europeans, making treatment effective.

- **Loc 74,751,897-74,751,897**  
  **Variant:** A vs G  
  **Drug:** Escitalopram  
  **Condition:** Major Depressive Disorder  
  **Insight:** A allele is much more frequent in Europeans, possibly affecting metabolism.

---

#### Chromosome 14

- **Loc 103,699,416-103,699,416**  
  **Variant:** A vs G  
  **Drug:** Radiotherapy  
  **Condition:** Nasopharyngeal Neoplasms  
  **Insight:** A allele more frequent in Europeans; treatment may be less effective.

- **Loc 90,397,013-90,397,013**  
  **Variant:** T vs C  
  **Drug:** Cyclosporine  
  **Condition:** Psoriasis  
  **Insight:** T allele more common in Europeans; drug more effective.

---

#### Chromosome 13

- **Loc 20,988,809-20,988,809**  
  **Variant:** A vs G  
  **Drug:** Cetuximab  
  **Condition:** Colorectal Neoplasms  
  **Insight:** A allele common in Europeans (~81%); drug less effective.

---

#### Chromosome 12

- **Loc 111,446,804-111,446,804**  
  **Variant:** T vs C  
  **Drug:** Hydrochlorothiazide  
  **Condition:** Hypertension  
  **Insight:** T allele common in Europeans; reduced treatment effectiveness.

- **Loc 111,634,620-111,634,620**  
  **Genotype:** AA + AG vs GG  
  **Insight:** G allele less frequent in Europeans; hydrochlorothiazide less effective.

---

#### Chromosome 11

- **Loc 126,157,578-126,157,578**  
  **Variant:** A vs G  
  **Drugs:** Interferon beta-1a, beta-1b  
  **Condition:** Multiple Sclerosis  
  **Insight:** G allele less frequent in Europeans; better response expected.

- **Loc 101,117,303-101,117,303**  
  **Genotypes:** CT + TT vs CC  
  **Drug:** Etonogestrel  
  **Insight:** T allele very common in Europeans (~80%); caution advised.

---

#### Chromosome 10

- **Loc 107,285,113-107,285,113**  
  **Genotype:** GG vs AA + AG  
  **Drug:** Exenatide  
  **Condition:** Type 2 Diabetes  
  **Insight:** G allele common in Europeans; drug more effective.

- **Loc 62,045,858-62,045,858**  
  **Variant:** C vs T  
  **Drug:** Methotrexate  
  **Condition:** Leukemia  
  **Insight:** C allele rare in Europeans; good diagnostic marker.

---

#### Chromosome 9

- **Loc 85,025,721-85,025,721**  
  **Genotype:** AA  
  **Drug:** Lithium  
  **Condition:** Bipolar Disorder  
  **Insight:** A allele less frequent in Europeans; lower response expected.

- **Loc 100,301,363-100,301,363**  
  **Variant:** G vs A  
  **Drug:** Duloxetine  
  **Condition:** Major Depressive Disorder  
  **Insight:** G allele rare in Europeans; lower drug effectiveness.

---

#### Chromosome 7

- **Loc 99,647,457-99,647,457**  
  **Variant:** C vs A  
  **Drug:** Tacrolimus  
  **Condition:** Kidney Transplant  
  **Insight:** C allele less frequent in Europeans; immune responses less likely.

---

#### Chromosome 6

- **Loc 154,117,494-154,117,494**  
  **Variant 1:** C vs A (Opioids)  
  **Variant 2:** G vs A (Ethanol)  
  **Gene:** OPRM1  
  **Insight:** Variants are common in Europeans and may reduce sensitivity to opioids and alcohol, suggesting evolutionary adaptation.

---

#### Chromosome 5

- **Loc 132,660,151-132,660,151**  
  **Variant:** T vs C  
  **Drug:** Hepatitis vaccines  
  **Insight:** C allele common in Europeans (~80%), possibly due to early vaccination campaigns.

- **Loc 132,660,808-132,660,808**  
  **Genotypes:** AA + AC vs CC  
  **Drug:** Ustekinumab  
  **Condition:** Psoriasis  
  **Insight:** CC genotype common in Europeans; treatment effective.

---

#### Chromosome 4

- **Loc 14,788,854-14,788,854**  
  **Variant:** G vs A  
  **Drug:** Duloxetine  
  **Condition:** Major Depressive Disorder  
  **Insight:** G allele rare in Europeans; drug less effective.

- **Loc 61,914,104-61,914,104**  
  **Genotypes:** AG + GG vs AA  
  **Drug:** Methylphenidate  
  **Condition:** ADHD  
  **Insight:** G allele common in Europeans; drug more effective.

- **Loc 61,828,999-61,828,999**  
  **Genotype:** AA vs AT + TT  
  **Condition:** ADHD  
  **Insight:** A allele less common in Europeans; reinforces above.

---

#### Chromosome 3

- **Loc 54,220,102-54,220,102**  
  **Genotype:** AA vs GG  
  **Drug:** Antipsychotics  
  **Condition:** Schizophrenia  
  **Insight:** A allele rare in Europeans; treatment more difficult.

- **Loc 14,801,652-14,801,652**  
  **Variant:** A vs C  
  **Drugs:** Atenolol, Metoprolol  
  **Condition:** Hypertension  
  **Insight:** A allele less frequent in Europeans; lower efficacy.

---

#### Chromosome 2

- **Loc 233,916,448-233,916,448**  
  **Variant:** C vs T  
  **Drug:** Botulinum toxin A  
  **Condition:** Migraine (Women)  
  **Insight:** C allele rare in Europeans; higher risk of side effects.

- **Loc 60,908,994-60,908,994**  
  **Variant:** T vs G  
  **Drug:** TNF-alpha inhibitors  
  **Condition:** Rheumatoid Arthritis  
  **Insight:** T allele more common in Europeans; better treatment outcomes.

---

#### Chromosome 1

- **Loc 156,882,671-156,882,671**  
  **Genotypes:** AC + CC vs AA  
  **Drugs:** Aspirin, Prasugrel  
  **Insight:** C allele is common in Europeans (~73%); weaker drug response.

- **Loc 32,290,838-32,290,838**  
  **Genotype:** CC vs CT + TT  
  **Drug:** Corticosteroids  
  **Condition:** Asthma (children)  
  **Insight:** C allele less common in Non-Finnish Europeans; treatment effective.

---

## Requirements

- g++ for compiling shrink_vcf.cpp
- PyPy3 (recommended) or CPython 3.x
- IGV for visualization
- make, zcat, and standard UNIX tools

## Licence
This project is open for academic and research use. No license restrictions, but please credit the author and cite the data source: gnomAD v4.
