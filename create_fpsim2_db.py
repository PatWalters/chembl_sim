#!/usr/bin/env python

import sys
from FPSim2.io import create_db_file
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} chembl_database_file fingerprint_file")
    sys.exit(0)

chembl_database_file = sys.argv[1]
fpdb2_h5_file = sys.argv[2]

engine = create_engine(f'sqlite:///{chembl_database_file}')
s = Session(engine)
sql_query = "select canonical_smiles, molregno from compound_structures where canonical_smiles is not null"
res_prox = s.execute(sql_query)
create_db_file(res_prox, fpdb2_h5_file, 'Morgan', {'radius': 2, 'nBits': 2048})
