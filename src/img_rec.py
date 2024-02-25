import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from sklearn.cluster import KMeans

# Round to next smaller multiple of 8
def round_down_to_next_multiple_of(size, a):
    return a & (-size)

def recognize_image(image_path, board_size):
    img = cv2.imread(image_path)
    wh = np.min(round_down_to_next_multiple_of(board_size, np.array(img.shape[:2])))
    img = cv2.resize(img, (wh, wh))

    # Prepare some visualization output
    out = img.copy()

    # Blur image
    img = cv2.blur(img, (5, 5))

    # Iterate tiles, and count unique colors inside
    wh_t = wh // board_size
    count_unique_colors = np.zeros((board_size, board_size))
    for x in np.arange(board_size):
        for y in np.arange(board_size):
            tile = img[y*wh_t:(y+1)*wh_t, x*wh_t:(x+1)*wh_t]
            tile = tile[3:-3, 3:-3]
            count_unique_colors[y, x] = np.unique(tile.reshape(-1, tile.shape[-1]), axis=0).shape[0]

    # Mask empty squares using cutoff from Otsu's method
    val = threshold_otsu(count_unique_colors)
    mask_empty = count_unique_colors < val

    threshold = val
    indices = np.where(count_unique_colors > threshold)
    values_above_threshold = count_unique_colors[indices]

    # 将数组展平为一维
    flattened_array = values_above_threshold.flatten()

    # 将数组转换为列向量
    data = flattened_array.reshape(-1, 1)

    # 使用K均值聚类将数据分为两组
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(data)

    # 获取聚类结果
    labels = kmeans.labels_

    # 根据聚类结果将数组分组
    group1 = values_above_threshold[labels == 0]
    group2 = values_above_threshold[labels == 1]

    val2 = max(group1.min(), group2.min())
    mask_0 = count_unique_colors >= val2

    # Some more visualization output
    # plt.figure(1, figsize=(18, 6))
    # plt.subplot(1, 3, 1), plt.imshow(img)
    # for x in np.arange(board_size):
    #     for y in np.arange(board_size):
    #         if not mask_empty[y, x]:
    #             if mask_0[y, x]:
    #                 cv2.rectangle(out, (x * wh_t + 3, y * wh_t + 3),
    #                               ((x + 1) * wh_t - 3, (y + 1) * wh_t - 3), (0, 0, 255), 2)
    #             else:
    #                 cv2.rectangle(out, (x * wh_t + 3, y * wh_t + 3),
    #                               ((x + 1) * wh_t - 3, (y + 1) * wh_t - 3), (255, 0, 0), 2)
    #
    # plt.subplot(1, 3, 2), plt.imshow(count_unique_colors, cmap='gray')
    # plt.subplot(1, 3, 3), plt.imshow(out)
    # plt.tight_layout(), plt.show()

    return mask_empty, mask_0

# 示例用法
image_path = '../tests/board/takuzu_8x8.png'
board_size = 8
mask_empty, mask_0 = recognize_image(image_path, board_size)

# 打印结果或进一步处理
print("Mask Empty:")
print(mask_empty)
print("\nMask 0:")
print(mask_0)
