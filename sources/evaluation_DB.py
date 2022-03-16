from os import path, listdir
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

PATH_FOLDER = "../DB_10/"
PATH_DAY = "DAY/seg"
PATH_NIGHT = "NIGHT/seg"
SCORE_FILE = "score.txt"


def im_load(folder):
    if not path.isdir(folder):
        print(f"{folder} folder does not exist.")
        exit(1)

    names = listdir(folder)
    names.sort()

    N = len(names)
    images = [plt.imread(folder + "/" + names[0])[:, :, 0:3]] * N

    for i in range(1, N):
        images[i] = plt.imread(folder + "/" + names[i])[:, :, 0:3]

    return images, names


def check_pair(id_days, id_nights):
    Nd = len(id_days)
    Nn = len(id_nights)

    if Nd != Nn:
        print(f"[Mismatching numbers]\tday: {Nd} /--/ night: {Nn}")
        exit(1)

    for i in range(Nd):
        if id_days[i] != id_nights[i]:
            print(
                f"[Mismatching names]\tday: {id_days[i]}"
                + f" /--/ night: {id_nights[i]}"
            )

    return 0


def score_im(day, night):
    score = 0
    w, h, _ = np.shape(day)

    for x in range(w):
        for y in range(h):
            score += not any(day[x, y, :] != night[x, y, :])

    score /= w * h
    return score


def score_database(days, nights):
    N = len(days)
    scores = np.zeros(N, dtype=float)

    for i in range(N):
        scores[i] = score_im(days[i], nights[i])

    return scores


def plot_score(scores):
    dataset_name = PATH_FOLDER.split("/", -1)[-2]
    global_score = round(np.mean(scores), 2)
    plt.plot(range(1, len(scores) + 1), scores)
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.ylim(0, 1.05)
    plt.xlabel("frames", fontsize=12)
    plt.ylabel("likeness", fontsize=12)
    plt.title(f"{dataset_name} score: {global_score}", fontsize=18)
    plt.show()
    return 0


def write_score(fpath, scores, id):
    f = open(fpath, "w")
    dataset_name = PATH_FOLDER.split("/", -1)[-2]
    f.write(f"{dataset_name} score\n\n")
    f.write(f"global: {round(np.mean(scores), 2)}\n\n")

    N = len(scores)
    for i in range(N):
        f.write(f"{id_days[i]}: {round(scores[i], 2)}\n")

    f.close()
    return 0


if __name__ == "__main__":
    days, id_days = im_load(PATH_FOLDER + PATH_DAY)
    nights, id_nights = im_load(PATH_FOLDER + PATH_NIGHT)

    check_pair(id_days, id_nights)

    scores = score_database(days, nights)
    write_score(PATH_FOLDER + SCORE_FILE, scores, id_days)
    plot_score(scores)
