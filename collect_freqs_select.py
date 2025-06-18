from sys import stdin

if __name__ == "__main__":
    with open("afr.vcf", 'a') as afr, \
         open("amr.vcf", 'a') as amr, \
         open("eas.vcf", 'a') as eas, \
         open("nfe.vcf", 'a') as nfe, \
         open("sas.vcf", 'a') as sas, \
         open("asj.vcf", 'a') as asj, \
         open("ami.vcf", 'a') as ami, \
         open("fin.vcf", 'a') as fin, \
         open("remaining.vcf", 'a') as rem:
        memory: dict[tuple[str, str, str, str], str] = {}
        with open("rs_dbsnp_joined.tsv", 'r') as template:
            for line in template.readlines()[1:]:
                line = line.strip().split('\t')
                line[1] = str(int(line[1]) + 1)
                for alt in line[4].split(','):
                    memory[(line[0], line[1], line[3], alt)] = line[7]
        pops_dict: dict[str, str] = {}
        for line in stdin:
            if line.startswith("#"):
                continue
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            chrom, pos, _, ref, alts = fields[:5]
            for alt in alts.split(','):
                key = (chrom, pos, ref, alt)
                if key not in memory:
                    continue
                pops_dict.clear()
                for attr in fields[-1].split(';'):
                    try:
                        name, value = attr.split('=')
                    except ValueError:
                        continue
                    if not name.startswith("AF_"):
                        continue
                    name_p = name[3:]
                    if name_p not in pops_dict:
                        pops_dict[name_p] = name[:2] + "=" + value
                for name, value in pops_dict.items():
                    if "AF" not in value:
                        continue
                    INFO = ";".join([value, "DESCR=" + memory[key]])
                    out_line = "\t".join([*fields[:4], alt, *fields[5:-1], INFO]) + "\n"
                    if name == "afr":
                        afr.write(out_line)
                    elif name == "amr":
                        amr.write(out_line)
                    elif name == "eas":
                        eas.write(out_line)
                    elif name == "nfe":
                        nfe.write(out_line)
                    elif name == "sas":
                        sas.write(out_line)
                    elif name == "asj":
                        asj.write(out_line)
                    elif name == "ami":
                        ami.write(out_line)
                    elif name == "fin":
                        fin.write(out_line)
                    else:
                        rem.write(out_line)
           