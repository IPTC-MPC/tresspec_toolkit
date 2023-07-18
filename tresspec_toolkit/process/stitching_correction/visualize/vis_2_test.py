import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def vis_2_test(runs, runs_sb):

    fig = plt.figure(figsize=(10, 8))
    outer = gridspec.GridSpec(2, 2, wspace=0.0, hspace=0.1)


#    # stitching_blocks
#    inner[0] = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[0], wspace=0.1, hspace=0.1)



    for i in range(4):
        inner = gridspec.GridSpecFromSubplotSpec(2, 1,
                                                 subplot_spec=outer[i], wspace=0.1, hspace=0.1)

        for j in range(2):
            ax = plt.Subplot(fig, inner[j])
            t = ax.text(0.5, 0.5, 'outer=%d, inner=%d' % (i, j))
            t.set_ha('center')
            ax.set_xticks([])
            ax.set_yticks([])
            fig.add_subplot(ax)

    fig.show()