from sys import stdin

if __name__ == "__main__":
    populations: set[str] = {"afr", "amr", "eas", "nfe", "sas", "asj", "ami", "fin"}
    for p in populations:
        open(f"{p}.vcf", 'w').write()
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
                AF, population_code = name.split('_', 1)
                if AF != "AF":
                    continue
                if population_code not in pops_dict:
                    pops_dict[population_code] = AF + "=" + value
            for name, value in pops_dict.items():
                if "AF" not in value:
                    continue
                INFO = ";".join([value, "DESCR=" + memory[key]])
                out_line = "\t".join([*fields[:4], alt, *fields[5:-1], INFO]) + "\n"
                name = name.lower()
                if name in populations:
                    open(f"{name}.vcf", 'a').write(out_line)

                
           