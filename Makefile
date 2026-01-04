SHELL := /bin/bash
SHRINK := ./shrink_vcf
SELECT := collect_freqs_select.py
POPULATIONS := afr amr eas nfe sas asj ami fin remaining
POP_VCF_FILES := $(POPULATIONS:%=%.vcf)
VCF_BZG_FILES := $(wildcard *.vcf.bgz)
VCF_OUTPUT_FILES := $(VCF_BZG_FILES:.vcf.bgz=.vcf.gz)

all: $(VCF_OUTPUT_FILES) collect bedgraphs

%.vcf.gz : %.vcf.bgz
	@echo "Processing $< ..."
	zcat "$<" | $(SHRINK) | bgzip > "$@"; \
	if [ $$? -eq 0 ]; then \
		echo "Success: Deleting $<"; \
		rm -f "$<"; \
	else \
		echo "Error occurred while processing $<"; \
		exit 1; \
	fi
	

collect: 
	zcat gnomad.genomes.v4.1.sites.chrY.vcf.gz | grep "^#" > tmp.txt; \
	for f in $(POP_VCF_FILES); do \
		cat tmp.txt > "$${f}"; \
	done; \
	for f in $(POP_VCF_FILES); do \
		echo "Collecting $${f} ..."; \
		zcat "$${f}" | pypy3 $(SELECT) > tmp.txt; \
	done; \

bedgraphs:
	python3 collect_freqs_bg.py