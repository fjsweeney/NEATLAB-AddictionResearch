import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def find_smoking_episodes(dts, smoking_dts):
    episodes = []

    start = dts[0]
    end = dts[len(dts) - 1]

    for dt in smoking_dts:
        if start <= dt <= end:
            print("Smoking Event: %s" % dt.strftime("%I:%M %p"))
            episodes.append(dt)

    return episodes


def plot_timeseries(prob_df, smoking_dts):
    print("Generating heatmap...")
    datetimes = prob_df['datetime']
    times = [datetime.datetime.time(d) for d in prob_df['datetime']]
    times = [dt.strftime("%I:%M %p") for dt in times]

    # Locate any smoking episodes in the series
    episodes = find_smoking_episodes(datetimes, smoking_dts)

    # Prepare probability matrix
    prob_df = prob_df.drop(columns=["datetime"])
    models = list(prob_df.columns)
    prob_df = prob_df.T

    fig, ax1 = plt.subplots()
    heatmap = ax1.pcolor(prob_df, cmap=plt.get_cmap("OrRd"))

    # legend
    cbar = plt.colorbar(heatmap)
    cbar.set_label('Probability of Smoking Vulnerability', rotation=270,
                   labelpad=20)

    xlocs = np.arange(len(times))
    ylocs = np.arange(len(models))
    plt.xticks(xlocs, labels=times, rotation=45)
    plt.yticks(ylocs, labels=models)

    # Add markers for smoking episodes
    ax2 = ax1.twiny()
    ax2_labels = []
    ax2_ticks = []
    start_time = datetimes[0]
    for i, end_time in enumerate(datetimes[1:]):
        for episode in episodes:
            if start_time <= episode <= end_time:
                ax2_labels.append("")
                ax2_ticks.append(i)
                break

        start_time = end_time

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(ax2_ticks)
    ax2.set_xticklabels(ax2_labels)

    # Annotate the 2nd position with an image
    # cig_img = plt.imread("cig_icon.png", format='png')
    xl, yl, xh, yh = np.array(ax1.get_position()).ravel()
    w = xh - xl
    h = yh - yl
    xp = xl + w * 0.1  # if replace '0' label, can also be calculated systematically using xlim()
    size = 0.05

    img = mpimg.imread("cig_icon.png", format='png')
    ax3 = fig.add_axes([xp - size * 0.5, yh, size, size])
    ax3.axison = False
    imgplot = ax3.imshow(img, transform=ax2.transAxes)


    # Hide major tick labels & customize minor tick labels for y-axis
    ax1.set_yticklabels('')
    ax1.set_yticks([0.5, 1.5, 2.5, 3.5], minor=True)
    ax1.set_yticklabels(models, minor=True)
    ax1.tick_params(left="off", top="off")

    step = 30
    ax1.xaxis.set_ticklabels(times[::step])
    ax1.xaxis.set_ticks(xlocs[::step])

    plt.show()
