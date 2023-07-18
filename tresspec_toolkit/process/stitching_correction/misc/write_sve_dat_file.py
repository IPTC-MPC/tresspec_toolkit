import pandas as pd
import numpy as np
import os


def write_sve_dat_file(runs_sb, filename=None):
    filename = filename + "_sve.dat"

    pth = os.getcwd()

    merged = list()
    for run in runs_sb:
        tmp = pd.concat(run, axis=1)
        header = np.insert(tmp.columns.to_numpy(), 0, 0)
        body = np.insert(tmp.to_numpy(), 0, tmp.index.to_numpy(), axis=1)
        merged.append(np.insert(body, 0, header, axis=0))

    out = np.vstack(merged)

    try:
        np.savetxt(os.path.join(pth, "processed_data", filename), out, delimiter=' ')
    except FileNotFoundError:
        print("Creating directory 'processed_data' in ", pth)
        os.makedirs(os.path.join(pth, "processed_data"))
        np.savetxt(os.path.join(pth, "processed_data", filename), out, delimiter=' ')

    print("Data successfully written to\n", os.path.join(pth, "processed_data", filename), "\n")
