import os
import numpy as np


def create_glotaran_input(datasets, comment1="comment1", comment2="comment2", filename="glotaran_input"):

    """
    Invoke create_glotaran_input to write the data to a file that can be opened with Glotaran
    :param datasets:    a pandas DataFrame storing the data (or a list thereof)
    :param comment1:    comment written to first line of glotaran input file
    :param comment2:    comment written to second line of glotaran input file
    :param filename:    the base filename of the created file(s)
    :return:            creates glotaran input file(s) based on the given input dataset(s)
    """

    if not isinstance(datasets, list):
        datasets = [datasets]

    if not os.path.exists(os.path.join(os.getcwd(), "glotaran")):
        os.makedirs(os.path.join(os.getcwd(), "glotaran"))

    # loop to write data
    for idx, dataset in enumerate(datasets):
        delay_axis = np.atleast_2d(dataset.columns.to_numpy())
        data_block = np.insert(dataset.to_numpy(), 0, dataset.index.to_numpy(), axis=1)

        filename_tmp = f"{filename}_{idx:02d}.ascii"

        file_path = os.path.join(os.getcwd(), "glotaran", filename_tmp)

        # writing to file
        # creating headers
        f = open(file_path, "w")
        f.writelines(f"{comment1}\n")
        f.writelines(f"{comment2}\n")
        f.writelines("Time explicit\n")
        f.writelines(f"Intervalnr   {len(dataset.columns)}\n")

        # writing delays and block of data
        np.savetxt(f, delay_axis, fmt='%.2f',)
        np.savetxt(f, data_block, fmt="%f")

        f.close()
