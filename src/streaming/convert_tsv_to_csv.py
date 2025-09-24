import csv


def convertTsvToCsv(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as fin, \
            open(output_file, "w", encoding="utf-8") as fout:
        reader = csv.reader(fin, delimiter="\t")
        for row in reader:
            if len(row) < 2:
                continue
            wav_path = row[0].strip()
            text = row[1].strip().strip('"')
            fout.write(f"{wav_path}|{text}\n")


convertTsvToCsv("meta_data.tsv", "meta_data.csv")

