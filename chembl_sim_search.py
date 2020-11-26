#!/usr/bin/env python

"""Usage: chembl_sim.py --query QUERY_SMI --out OUT_CSV [--sim SIM_CUTOFF]

--help print this help message
--query QUERY_SMI query SMILES file (takes the form SMILES name)
--out OUT_CSV output csv file
--sim SIM_CUTOFF similarity cutoff, default=0.7
"""

import sys
import os
from FPSim2 import FPSim2Engine
import sqlite3
import pandas as pd
from tqdm import tqdm
from docopt import docopt


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


do_input = docopt(__doc__)
query_filename = do_input.get("--query")
output_filename = do_input.get("--out")
sim_cutoff = do_input.get("--sim") or 0.7
sim_cutoff = float(sim_cutoff)

# Open the SQLite database file
db_filename = "chembl_27.db"
if not os.path.exists(db_filename):
    print(f"Could not open database file {db_filename}", file=sys.stderr)
    sys.exit(0)
con = sqlite3.connect(db_filename)

# Open the fingerprint file
try:
    fp_filename = 'chembl_27.h5'
    fpe = FPSim2Engine(fp_filename)
except IOError:
    print(f"Could not open fingerprint file {fp_filename}", file=sys.stderr)

# Make sure we don't overwrite the output file
if os.path.exists(output_filename):
    print(f"Output file exists - please remove or choose another file name", file=sys.stderr)
    sys.exit(0)

# Open the input file
try:
    query_df = pd.read_csv(query_filename, names=["SMILES", "Name"], sep=" ")
except FileNotFoundError:
    print(f"Could not open {query_filename}")
    sys.exit(0)

# Process the input
for query_smi, query_name in tqdm(query_df.values):
    results = fpe.similarity(query_smi, sim_cutoff, n_workers=1)
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
print(f"Results written to {output_filename}", file=sys.stderr)
