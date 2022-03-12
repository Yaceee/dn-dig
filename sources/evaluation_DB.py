from os import path, listdir
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


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
                f"[Mismatching images]\tday: {id_days[i]}"
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


if __name__ == "__main__":
    days, id_days = im_load("../Dataset_test_eval/_DAY_seg")
    nights, id_nights = im_load("../Dataset_test_eval/_NIGHT_seg")

    check_pair(id_days, id_nights)

    scores = score_database(days, nights)

    plt.plot(range(1, len(scores) + 1), scores)
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.ylim(0, 1.05)
    plt.xlabel("frames", fontsize=12)
    plt.ylabel("likeness", fontsize=12)
    plt.title(f"Dataset score: {np.mean(scores)}", fontsize=18)
    plt.show()
