#!/usr/bin/env python

import sys
import os
from FPSim2 import FPSim2Engine
import sqlite3
import pandas as pd
from tqdm import tqdm


def get_assay_data(con, molregno):
    sql = f"""select canonical_smiles, cs.molregno, standard_type, standard_value, standard_units, doi, a.description 
from compound_structures cs
join activities act on  cs.molregno = act.molregno
join docs d on act.doc_id = d.doc_id
join assays a on act.assay_id = a.assay_id
where cs.molregno = {molregno}
and act.standard_relation = '='
and act.standard_type in ('IC50', 'Ki', 'EC50')"""
    return pd.read_sql(sql, con)


if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} query_file.smi outfile.csv")
    sys.exit(0)

con = sqlite3.connect("chembl_27.db")

query_filename = sys.argv[1]
output_filename = sys.argv[2]

if os.path.exists(output_filename):
    print("Output file exists - please remove or choose another file name", file=sys.stderr)
    sys.exit(0)

fp_filename = 'chembl_27.h5'
fpe = FPSim2Engine(fp_filename)

query_df = pd.read_csv(query_filename, names=["SMILES", "Name"], sep=" ")
for query_smi, query_name in tqdm(query_df.values):
    results = fpe.similarity(query_smi, 0.7, n_workers=1)
    for molregno, sim in results:
        res = get_assay_data(con, molregno)
        res['query_smiles'] = query_smi
        res['query_name'] = query_name
        res['query_sim'] = sim
        col_names = list(res.columns)
        col_names = col_names[-3:] + col_names[:-3]
        res = res[col_names]
        if res.shape[0] > 0:
            if not os.path.isfile(output_filename):
                res.to_csv(output_filename, index=False)
            else:
                res.to_csv(output_filename, mode='a', header=False, index=False)
