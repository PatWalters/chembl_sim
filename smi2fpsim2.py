#!/usr/bin/env python

import sys
from FPSim2.io import create_db_file
from sqlalchemy import *
from sqlalchemy.orm import Session
import pandas as pd
from tqdm import tqdm
import os

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} smiles_file_name")
    sys.exit(0)

smiles_file_name = sys.argv[1]
sqlite_db_filename = smiles_file_name.replace(".smi",".db")
fpdb2_h5_filename = smiles_file_name.replace("smi","h5")

if os.path.exists(sqlite_db_filename):
    print(f"{sqlite_db_filename} exists, please remove or rename")
    sys.exit(0)

if os.path.exists(fpdb2_h5_filename):
    print(f"{fpdb2_h5_filename} exists, please remove or rename")
    sys.exit(0)
    
db_uri = f"sqlite:///{sqlite_db_filename}"
db = create_engine(db_uri,echo=False)
meta = MetaData(db)

mols = Table(
    'mols', meta,
    Column('id', Integer, primary_key=True),
    Column('smiles',String),
    Column('name',String),
    sqlite_autoincrement=True
)
mols.create()

df = pd.read_csv(smiles_file_name,sep=" ",names=["smiles","name"])

i = mols.insert()
for smiles,name in tqdm(df[['smiles','name']].values):
    i.execute({"smiles" : smiles,"name": name})

print(f"Created SQLite database {sqlite_db_filename}")

s = Session(db)
sql_query = "select smiles, id from mols where smiles is not null"
res_prox = s.execute(sql_query)
create_db_file(res_prox, fpdb2_h5_filename, 'Morgan', {'radius': 2, 'nBits': 2048})

print(f"Created FPSim2 database {fpdb2_h5_filename}")


#create_db_file(smiles_file_name, fpdb2_h5_filename, 'Morgan', {'radius': 2, 'nBits': 2048},gen_ids=True)





