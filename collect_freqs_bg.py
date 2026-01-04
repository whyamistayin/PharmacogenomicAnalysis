def parse(handle_read, handle_write):
    global dict_p, nfe_memory
    for line in handle_read.readlines():
        if line.startswith("#"):
            continue
        line = line.strip()
        if not line:
            continue
        fields = line.split('\t')
        chrom, pos, _, ref, alts = fields[:5]
        _, af = fields[7].split(';')[0].split('=')
        af = float(af)
        if (chrom, pos) in dict_p:
            dict_p[(chrom, pos)] = max(dict_p[(chrom, pos)], af)
        else:
            dict_p[(chrom, pos)] = af
    for (chrom, pos), af in dict_p.items():
        if (chrom, pos) not in nfe_memory:
            continue
        diff: float = nfe_memory[(chrom, pos)] - af
        handle_write.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
    dict_p.clear()

if __name__ == "__main__":
    with open("afr.vcf", 'r') as afr, \
         open("amr.vcf", 'r') as amr, \
         open("eas.vcf", 'r') as eas, \
         open("nfe.vcf", 'r') as nfe, \
         open("sas.vcf", 'r') as sas, \
         open("asj.vcf", 'r') as asj, \
         open("ami.vcf", 'r') as ami, \
         open("fin.vcf", 'r') as fin, \
         open("remaining.vcf", 'r') as rem, \
         open("nfe-vs-asj.bedGraph", 'w') as nfe_vs_asj, \
         open("nfe-vs-ami.bedGraph", 'w') as nfe_vs_ami, \
         open("nfe-vs-fin.bedGraph", 'w') as nfe_vs_fin, \
         open("nfe-vs-rem.bedGraph", 'w') as nfe_vs_rem, \
         open("nfe-vs-sas.bedGraph", 'w') as nfe_vs_sas, \
         open("nfe-vs-eas.bedGraph", 'w') as nfe_vs_eas, \
         open("nfe-vs-amr.bedGraph", 'w') as nfe_vs_amr, \
         open("nfe-vs-afr.bedGraph", 'w') as nfe_vs_afr:
        nfe_memory: dict[tuple[str, str], float] = {}
        nfe_vs_asj.write('track type=bedGraph name="nfe vs asj" description="Comparison" visibility=full\n')
        nfe_vs_ami.write('track type=bedGraph name="nfe vs ami" description="Comparison" visibility=full\n')
        nfe_vs_fin.write('track type=bedGraph name="nfe vs fin" description="Comparison" visibility=full\n')
        nfe_vs_rem.write('track type=bedGraph name="nfe vs rem" description="Comparison" visibility=full\n')
        nfe_vs_sas.write('track type=bedGraph name="nfe vs sas" description="Comparison" visibility=full\n')
        nfe_vs_eas.write('track type=bedGraph name="nfe vs eas" description="Comparison" visibility=full\n')
        nfe_vs_amr.write('track type=bedGraph name="nfe vs amr" description="Comparison" visibility=full\n')
        nfe_vs_afr.write('track type=bedGraph name="nfe vs afr" description="Comparison" visibility=full\n')

        for line in nfe.readlines():
            if line.startswith("#"):
                continue
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            chrom, pos, _, ref, alts = fields[:5]
            _, af = fields[7].split(';')[0].split('=')
            af = float(af)
            if (chrom, pos) in nfe_memory:
                nfe_memory[(chrom, pos)] = max(nfe_memory[(chrom, pos)], af)
            else: 
                nfe_memory[(chrom, pos)] = af
        dict_p: dict[tuple[str, str], float] = {}
        parse(asj, nfe_vs_asj)
        parse(ami, nfe_vs_ami)
        parse(fin, nfe_vs_fin)
        parse(rem, nfe_vs_rem)
        parse(sas, nfe_vs_sas)
        parse(eas, nfe_vs_eas)
        parse(amr, nfe_vs_amr)
        parse(afr, nfe_vs_afr)
        nfe_memory.clear()
