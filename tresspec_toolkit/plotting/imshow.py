import matplotlib.pyplot as plt


def imshow(datasets):

    if not isinstance(datasets, list):
        datasets = [datasets]

    for data in datasets:
        fig, ax = plt.subplots()
        ax.imshow(data)