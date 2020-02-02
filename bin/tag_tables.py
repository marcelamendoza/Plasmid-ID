import sys
import getopt
import csv
import gzip
import itertools
import pandas as pd
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq


def fasta_to_dict(path, reverse):
	ret_dict = SeqIO.to_dict(SeqIO.parse(path, "fasta"))
	ret_dict = {k:v.seq for k, v in ret_dict.items()}
	if(reverse):
		ret_dict = {k:v.reverse_complement() for k, v in ret_dict.items()}
	ret_dict = {k:str(v) for k, v in ret_dict.items()}
	#print(ret_dict)
	return(ret_dict)

def read_plasmids_table(path):
	plasmids = {}
	with open(path, 'r') as csvfile:
		table_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for row in table_reader:
			plasmids[row["Barcode name"]]= row["ID plasmid sequence"]
	return(plasmids)

def find_hash_position(sequence, tags):
	for key, value in tags.items():
		position = sequence.find(value)
		if position != -1:
			return (key, position)
	return ("none", -1)

def find_plasmid_positions(sequence, forward_dict, reverse_dict, plasmids, orientation):
	fw_name, fw_pos = find_hash_position(sequence, forward_dict)
	rv_name, rv_pos = find_hash_position(sequence, reverse_dict)
	pl_name, pl_pos = find_hash_position(sequence, plasmids)

	if(fw_pos + rv_pos + pl_pos == -3 ):
		orientation = "."

	return ([fw_name, str(fw_pos), rv_name, str(rv_pos), pl_name,str(pl_pos), orientation])


def write_raw_counts(fq, output_prefix, forward_dict, reverse_dict, plasmids):
	fw_f = fq
	distances_f = output_prefix + "_distances_merge.txt"
	with gzip.open(fw_f, "rt") as r1,open(distances_f,"w") as f3:
		f3.write("fw_name,fw_pos,rev_name,rev_pos,pl_name,pl_pos,orientation\n")
		for fw in SeqIO.parse(r1, "fastq") :
			str_seq = str(fw.seq)
			values = find_plasmid_positions(str_seq, forward_dict, reverse_dict, plasmids, "+")
			 
			if values[6] == ".":
				str_seq = str(fw.seq.reverse_complement())
				values = find_plasmid_positions(str_seq, forward_dict, reverse_dict, plasmids, "-")

			f3.write(",".join(values)) 
			f3.write("\n")

def write_summary(output_prefix):
	distances_f = output_prefix + "_distances_merge.txt"
	df = pd.read_csv(distances_f)
	summ=df[['fw_name', 'rev_name', 'pl_name', 'pl_pos']].groupby(['fw_name', 'rev_name', 'pl_name']).agg( ['count','mean'])
	summ.to_csv(output_prefix + "summary_merge.csv", sep=',')

def usage():
	print ("Usage: " + sys.argv[0]  + " --plasmid=<plasmids.csv> --forward=<forward_ids.fa> --reverse=<reverse_ids.fa> --sequences=<sequences.fq.gz> --output_prefix=<file_prefix>")


def main(argv):
	try: 
		opts, args = getopt.getopt(argv,'p:f:r:s:o:h', ['plasmid=','forward=','reverse=','sequences=', 'output_prefix=', 'help'])
	except getopt.GetOptError:
		usage()
		sys.exit(2)

	if not opts: 
			print ('No options supplied')
			usage()

	for opt, arg in opts: 
		if opt in ('h', '--help'):
			usage()
			sys.exit(2)
		elif opt in ('p', '--plasmid'):
			plasmid_path = arg 
			plamids_dict = read_plasmids_table(plasmid_path)
		elif opt in ('f', '--forward'):
			forward_path = arg 
			forward_dict = fasta_to_dict(forward_path, False)
		elif opt in ('r', '--reverse'):
			reverse_path = arg 
			reverse_dict = fasta_to_dict(reverse_path, True)
		elif opt in ('s', '--sequences'):
			sequences_path = arg
			print(arg)
		elif opt in ('o', '--output_prefix'):
			output_prefix = arg

	write_raw_counts(sequences_path, output_prefix, forward_dict, reverse_dict, plamids_dict)
	write_summary(output_prefix)

if __name__ == '__main__':
	main(sys.argv[1:])