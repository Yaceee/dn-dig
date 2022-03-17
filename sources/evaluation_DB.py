import re
import numpy as np
import matplotlib.pyplot as plt
import config as conf
from os import path, listdir
from tqdm import tqdm

PATH_FOLDER = f"../DB_{conf.IM_NUMBER}/"
PATH_DAY = "DAY/seg"
PATH_NIGHT = "NIGHT/seg"
SCORE_FILE = "score.txt"

SIGNIFICANT_NB = 4


def convert(text):
    return int(text) if text.isdigit() else text.lower()


def alphanum_key(key):
    return [convert(c) for c in re.split("([0-9]+)", key)]


def sorted_alphanumeric(data):
    return sorted(data, key=alphanum_key)


def im_load(folder):
    if not path.isdir(folder):
        print(f"{folder} folder does not exist.")
        exit(1)

    names = sorted_alphanumeric(listdir(folder))

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

    for i in tqdm(range(N)):
        scores[i] = score_im(days[i], nights[i])

    return scores


def make_graph(scores):
    dataset_name = PATH_FOLDER.split("/", -1)[-2]
    global_score = round(np.mean(scores), SIGNIFICANT_NB)
    plt.plot(range(1, len(scores) + 1), scores)
    plt.ylim(0, 1.05)
    plt.xlabel("frames", fontsize=12)
    plt.ylabel("likeness", fontsize=12)
    plt.title(f"{dataset_name} score: {global_score}", fontsize=18)
    plt.savefig(PATH_FOLDER + "score.png")
    return 0


def write_score(fpath, scores, id):
    f = open(fpath, "w")
    dataset_name = PATH_FOLDER.split("/", -1)[-2]
    f.write(f"{dataset_name} score\n\n")
    f.write(f"global: {round(np.mean(scores), SIGNIFICANT_NB)}\n\n")

    N = len(scores)
    for i in range(N):
        f.write(f"{id[i]}: {round(scores[i], SIGNIFICANT_NB)}\n")

    f.close()
    return 0


if __name__ == "__main__":
    days, id_days = im_load(PATH_FOLDER + PATH_DAY)
    nights, id_nights = im_load(PATH_FOLDER + PATH_NIGHT)

    check_pair(id_days, id_nights)

    scores = score_database(days, nights)
    write_score(PATH_FOLDER + SCORE_FILE, scores, id_days)
    make_graph(scores)
