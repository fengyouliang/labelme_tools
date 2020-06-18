import numpy as np


def random_sample(img_scales):
    img_scale_long = [max(s) for s in img_scales]
    img_scale_short = [min(s) for s in img_scales]
    long_edge = np.random.randint(
        min(img_scale_long),
        max(img_scale_long) + 1)
    short_edge = np.random.randint(
        min(img_scale_short),
        max(img_scale_short) + 1)
    img_scale = (long_edge, short_edge)
    return img_scale, None


def random_select(img_scales):
    scale_idx = np.random.randint(len(img_scales))
    img_scale = img_scales[scale_idx]
    return img_scale, scale_idx


def check_random_sample():
    img_scales = [(1024, 1024), (512, 512)]  #
    # img_scales = [(1388, 800), (512, 512)]  #
    ret = random_select(img_scales)
    scale, scale_idx = ret
    print(scale, scale_idx)


def main():
    for i in range(10):
        check_random_sample()


if __name__ == '__main__':
    main()
