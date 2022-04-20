import re
import numpy as np
import matplotlib.pyplot as plt
from os import path, listdir
from tqdm import tqdm

PATH_FOLDER = f"../DB_fps_0d8/"
PATH_DAY = "DAY/seg/"
PATH_NIGHT = "NIGHT/seg/"
SCORE_FILE = "score.txt"

SIGNIFICANT_NB = 4


def convert(text):
    return int(text) if text.isdigit() else text.lower()


def alphanum_key(key):
    return [convert(c) for c in re.split("([0-9]+)", key)]


def sorted_alphanumeric(data):
    return sorted(data, key=alphanum_key)


def check_pair(id_days, id_nights):
    print("Checking pairs...")

    Nd = len(id_days)
    Nn = len(id_nights)
    mismatch = 0

    if Nd != Nn:
        print(f"[Mismatching numbers]\tday: {Nd} /--/ night: {Nn}")
        exit(1)

    for i in range(Nd):
        if id_days[i] != id_nights[i]:
            print(
                f"[Mismatching names]\tday: {id_days[i]}"
                + f" /--/ night: {id_nights[i]}"
            )
            mismatch = 1

    if not mismatch:
        print("All pairs are well named")

    return 0


def score_im(day, night):
    error = 0
    w, h, _ = np.shape(day)

    error = np.sum(np.any(day != night, axis=2))

    error /= w * h
    return 1 - error


def evaluation(id_days, id_nights):
    print("Evaluation of the dataset...")

    N = len(id_days)
    scores = np.zeros(N, dtype=float)

    for i in tqdm(range(N)):
        im_day = plt.imread(PATH_FOLDER + PATH_DAY + id_days[i])[:, :, 0:3]
        im_night = plt.imread(PATH_FOLDER + PATH_NIGHT + id_nights[i])[:, :, 0:3]
        scores[i] = score_im(im_day, im_night)

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


def write_score(scores, id):
    f = open(PATH_FOLDER + SCORE_FILE, "w")
    dataset_name = PATH_FOLDER.split("/", -1)[-2]
    f.write(f"{dataset_name} score\n\n")
    f.write(f"global: {round(np.mean(scores), SIGNIFICANT_NB)}\n\n")

    N = len(scores)
    for i in range(N):
        f.write(f"{id[i]}: {scores[i]}\n")

    f.close()
    return 0


if __name__ == "__main__":
    id_days = sorted_alphanumeric(listdir(PATH_FOLDER + PATH_DAY))
    id_nights = sorted_alphanumeric(listdir(PATH_FOLDER + PATH_NIGHT))

    check_pair(id_days, id_nights)

    scores = evaluation(id_days, id_nights)

    print("Writting results")
    make_graph(scores)
    write_score(scores, id_days)
