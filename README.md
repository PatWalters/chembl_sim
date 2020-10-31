# chembl_sim
ChEMBL Similarity Search

0. Install necessary libraries
```
pip install SQLAlchemy
conda install -c conda-forge fpsim2
```

1. Download chembl_27_sqlite.tar.gz from [ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/](ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/)

2. Untar the file and put chembl_27.db somewhere, and put the attached scripts in the same directory. 

3. Create the fingerprint database, note that this takes a while
```
create_fpsim2_db.py chembl_27.db chembl_27.h5
```

4. Get the biological data for similar molecules 
```
chembl_sim_search.py query.smi out.csv
```

[link](https://www.google.com)
