# Plasmid-ID
Tagging strains using high-density ID reporter plasmids


## Dependencies

In order to use ```Plasmid-ID``` you must install the following libraries:

    * Pandas
    * BioPython


```sh
pip3.7 install pandas
pip3.7 install biopython

```

## Input files

![Diagram](figures/Workflow_IT_PCR-01B.png)

### Plasmid ID sequences

The barcode sequence corresponding to each amplicon must be provided in a file with the following columns: ```Barcode name``` and ```ID plasmid sequence```. The headers of the columns ***must*** match the names described above. The file may have extra columns for reference in the downstream analysis. 

```csv
Barcode name,ID plasmid sequence
806rcbc0,TCCCTTGTCTCC
806rcbc1,ACGAGACTGATT
806rcbc2,GCTGTACGGATT
806rcbc3,ATCACCAGGTGT
806rcbc4,TGGTCAACGATA
806rcbc5,ATCGCACAGTAA
806rcbc6,GTCGTGTAGCCT
806rcbc7,AGCGGAGGTTAG
```


See ```examples/plasmids.csv``` for further reference. This corresponds to ```Column BC``` and ```Row BC``` in the diagram above. 

### Barcode sequences. 

The sequence of the forward and reverse primers that where used to amplify the different plasmids. The sequences must be in fasta format. ```Plasmid-ID``` uses the forward and reverse complement of each sequence.  This correspond to ```FW pad``` and ```RV pad``` in the figure above. 


FW_BC.fa
```
>1F_BC_IT   
GCTACATCACGCATGGTATGGA
>2F_BC_IT   
TGTGTCATCACGCATGGTATGGA
```

RV_BC.fa
```
>A1R    
GCTCCCCAGTCACGACGTTGTAAAACG
>B2R    
CTAGTCCCAGTCACGACGTTGTAAAACG
```


### IonTorrent reads

The raw sequences from IonTorrent in ```fastq.gz``` format. The quality is not used in the program, as the assumption is that the coverage is high enough that the number of amplicons will be enough to discard the noise. In general, the threshold is to remove sequences that appear less in than 2% of the sample. 




## Running the program 

To run the program, the following command can be used

```
python3.7 bin/tag_tables.py --plasmid=examples/plasmids.csv --forward=examples/FW_BC.fa --reverse=examples/RV_BC.fa --sequences=examples/10000_sample.fq.gz --output=plasmid_summary
```

All the arguments are required and the inputs are described above. 
