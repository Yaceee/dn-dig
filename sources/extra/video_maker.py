import cv2
from tqdm import tqdm
from os.path import join
from glob import glob
import re
import argparse


def get_images_path(dir):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]

    return sorted(glob(join(dir, "*.png")), key=alphanum_key)


def main(arg):
    Vwidth = 1920
    Iwidth = 640
    height = 1080

    day_files = get_images_path("../" + arg.dbname + "/DAY/rgb")
    seg_files = get_images_path("../" + arg.dbname + "/DAY/seg")
    ngt_files = get_images_path("../" + arg.dbname + "/NIGHT/rgb")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter("../" + arg.dbname + "/video.avi",
                            fourcc, arg.fps, (Vwidth, height))

    for i in tqdm(range(1, len(day_files))):
        day = cv2.imread(day_files[i])
        ngt = cv2.imread(ngt_files[i])
        seg = cv2.imread(seg_files[i])

        ngt = cv2.resize(ngt, (Iwidth, height))
        day = cv2.resize(day, (Iwidth, height))
        seg = cv2.resize(seg, (Iwidth, height))

        img = cv2.hconcat([day, seg, ngt])
        video.write(img)

    cv2.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '--dbname', '-db',
        default='./DB',
        help='Path to the DB (default: ./DB)'
    )
    argparser.add_argument(
        '--fps', '-fps',
        default='20',
        type=int,
        help='Frame per seconds (default: 20)'
    )
    arg = argparser.parse_args()

    main(arg)
