import numpy as np
import pandas as pd
import os


def write_to_drive(data, filename="processed_and_averaged_data.dat"):
    pth1 = os.getcwd()
    # os.path.isfile(os.path.join(
    # , "processed_data\denoised_data_sve.dat"))

    filename = os.path.join(os.getcwd(), filename)

    data.to_csv(filename, sep="\t")

    print(pth1)
