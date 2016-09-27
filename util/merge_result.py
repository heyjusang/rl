####################################################
# merge output as one file  for cytoscape          #
####################################################

import glob

output_list = glob.glob("../out/*.txt")

value_info = {}
selected_info = {}
filenames = []
for output_path in output_list:
    filename = output_path.split("/")[-1].split(".")[0]
    filenames.append(filename)
    output_file = open(output_path, 'r')
    header = output_file.readline().replace("\n", "").replace("\r", "").split("\t") # "gene" "value" "selected"
    header.pop(0) # remove "gene"
    for line in output_file.readlines():
        elements = line.replace("\n", "").replace("\r", "").split("\t")
        gene = elements[0]
        value = elements[1]
        selected = elements[2]

        if gene not in value_info:
            value_info[gene] = []
        value_info[gene].append(value)
        
        if gene not in selected_info:
            selected_info[gene] = []
        selected_info[gene].append(selected)

    output_file.close()

header = [f + "_value" for f in filenames] + [f + "_selected" for f in filenames]

merged_file = open("../out/merged.txt", 'w')
merged_file.write("gene\t" + "\t".join(header) + "\n")

for gene in value_info:
    values = value_info[gene]
    selecteds = selected_info[gene]
    merged_file.write(gene + "\t" + "\t".join(values) + "\t" + "\t".join(selecteds) + "\n")

merged_file.close()
