# Plasmid-ID
Tagging strains using high-density ID reporter plasmids


##Dependencies

In order to use ```Plasmid-ID``` you must install the following libraries:
    * Pandas
    * BioPython


```sh
pip3.7 install pandas
pip3.7 install biopython

```

##Input files

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

