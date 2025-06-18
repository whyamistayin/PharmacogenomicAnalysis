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
        for line in asj.readlines():
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
            nfe_vs_asj.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in ami.readlines():
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
            nfe_vs_ami.write("\t".join([chrom, pos,str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in fin.readlines():
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
            nfe_vs_fin.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in rem.readlines():
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
            nfe_vs_rem.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in sas.readlines():
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
            nfe_vs_sas.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in eas.readlines():
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
            nfe_vs_eas.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in amr.readlines():
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
            nfe_vs_amr.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        for line in afr.readlines():
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
            nfe_vs_afr.write("\t".join([chrom, pos, str(int(pos) + 1), f"{diff:.5}"]) + "\n")
        dict_p.clear()
        nfe_memory.clear()
