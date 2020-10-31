# chembl_sim
### ChEMBL Similarity Search
This code accompanies my blog post ["What Do Molecules That Look LIke This Tend To Do"](https://practicalcheminformatics.blogspot.com/2020/10/what-do-molecules-that-look-like-this.html)

### Installation

This code requires the RDKit.  For more information on installation set [this link](https://www.rdkit.org/docs/Install.html). 

Install the necessary python libraries
```
pip install SQLAlchemy tqdm docopt
conda install -c conda-forge fpsim2
```

 Download chembl_27_sqlite.tar.gz from [ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/](ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/)
```
wget ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_27_sqlite.tar.gz
```

Untar the file and put chembl_27.db somewhere, and put the attached scripts in the same directory. 

Create the fingerprint database, note that this takes a while
```
create_fpsim2_db.py chembl_27.db chembl_27.h5
```


### Usage
Get the biological data for similar molecules 
```
Usage: chembl_sim.py --query QUERY_SMI --out OUT_CSV [--sim SIM_CUTOFF]

--help print this help message
--query QUERY_SMI query SMILES file (takes the form SMILES name)
--out OUT_CSV output csv file
--sim SIM_CUTOFF similarity cutoff, default=0.7
```
As an example: 
```
chembl_sim_search.py --query query.smi --out out.csv
```
To set the similarity cutoff:
```
chembl_sim_search.py --query query.smi --out out.csv --sim 0.6
```


