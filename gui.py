"""gui.py creates an updating matplotlib bar chart displaying predictions
 when run alongside MainApp"""


def gui_main_loop():

    #  The Main Loop that generates/updates the Prediction Bar Chart till stopped
    import os
    from file_read_backwards import FileReadBackwards
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import matplotlib as mpl

    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # changing working directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(str(dir_path))
    print("current directory is - " + str(dir_path))

    def animate(i):
        CT = [0]
        T = [0]

        with FileReadBackwards("predictions.txt") as file:
            pred = None
            iterator = 0
            for line in file:
                if iterator < 1:
                    pred = str(line)
                    iterator += 1
                else:
                    break
        pred = pred[1:-1]
        pred = pred.split(", ", 1)
        pred[0] = float(pred[0])
        pred[1] = float(pred[1])
        CT[0] = pred[0]
        T[0] = pred[1]
        X = "Preds"

        ax.clear()
        ax.barh(X, CT, color="b")
        ax.barh(X, T, left=CT, color="orange")
        ax.set_yticklabels([])
        ax.set_xticklabels([])

        teams = ["CT\n", "T\n"]

        iterator = 0
        for bar in ax.containers:
            lab = teams[iterator] + str(pred[iterator])[:5] + "%"
            labels = [lab]
            ax.bar_label(bar, labels=labels, label_type='center', fontsize=16, color="w", fontweight='bold')
            iterator += 1


    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

if __name__ == "__main__":
    gui_main_loop()
