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
    Vheight = 1080
    Iwidth = int(Vwidth / 2)
    Iheight = int(Vheight / 2)

    day_rgb_files = get_images_path("../" + arg.dbname + "/DAY/rgb")
    day_seg_files = get_images_path("../" + arg.dbname + "/DAY/seg")
    ngt_rgb_files = get_images_path("../" + arg.dbname + "/NIGHT/rgb")
    ngt_seg_files = get_images_path("../" + arg.dbname + "/NIGHT/seg")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter("../" + arg.dbname + "/video.avi",
                            fourcc, arg.fps, (Vwidth, Vheight))

    for i in tqdm(range(1, len(day_rgb_files))):
        day_rgb = cv2.imread(day_rgb_files[i])
        day_seg = cv2.imread(day_seg_files[i])
        ngt_rgb = cv2.imread(ngt_rgb_files[i])
        ngt_seg = cv2.imread(ngt_seg_files[i])

        day_rgb = cv2.resize(day_rgb, (Iwidth, Iheight))
        day_seg = cv2.resize(day_seg, (Iwidth, Iheight))
        ngt_rgb = cv2.resize(ngt_rgb, (Iwidth, Iheight))
        ngt_seg = cv2.resize(ngt_seg, (Iwidth, Iheight))

        frame = cv2.vconcat([cv2.hconcat([day_rgb, day_seg]),
                            cv2.hconcat([ngt_rgb, ngt_seg])])
        video.write(frame)

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
