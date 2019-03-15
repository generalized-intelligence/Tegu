#TODO: Add reference.
import numpy as np
def grayscale(rgb):
    return rgb.dot([0.299, 0.587, 0.114])

def saturation(rgb, saturation_var=0.5):
    gs = grayscale(rgb)
    alpha = 2 * np.random.random() * saturation_var 
    alpha += 1 - saturation_var
    rgb = rgb * alpha + (1 - alpha) * gs[:, :, None]
    return np.clip(rgb, 0, 255)

def brightness( rgb, saturation_var=0.5):
    alpha = 2 * np.random.random() * brightness_var 
    alpha += 1 - saturation_var
    rgb = rgb * alpha
    return np.clip(rgb, 0, 255)

def contrast( rgb, contrast_var=0.5):
    gs = grayscale(rgb).mean() * np.ones_like(rgb)
    alpha = 2 * np.random.random() * contrast_var 
    alpha += 1 - contrast_var
    rgb = rgb * alpha + (1 - alpha) * gs
    return np.clip(rgb, 0, 255)

def lighting( img, lighting_std=0.5):
    cov = np.cov(img.reshape(-1, 3) / 255.0, rowvar=False)
    eigval, eigvec = np.linalg.eigh(cov)
    noise = np.random.randn(3) * lighting_std
    noise = eigvec.dot(eigval * noise) * 255
    img += noise
    return np.clip(img, 0, 255)

def horizontal_flip( img, y, hflip_prob=0.5):
    if np.random.random() < hflip_prob:
        img = img[:, ::-1]
        y[:, [0, 2]] = 1 - y[:, [2, 0]]
    return img, y

def vertical_flip( img, y, vflip_prob=0.5):
    if np.random.random() < vflip_prob:
        img = img[::-1]
        y[:, [1, 3]] = 1 - y[:, [3, 1]]
    return img, y

def random_sized_crop( img, targets, crop_area_range=[0.75, 1.0], aspect_ratio_range=[3./4., 4./3.]):
    img_w = img.shape[1]
    img_h = img.shape[0]
    img_area = img_w * img_h
    random_scale = np.random.random()
    random_scale *= (crop_area_range[1] -
                        crop_area_range[0])
    random_scale += crop_area_range[0]
    target_area = random_scale * img_area
    random_ratio = np.random.random()
    random_ratio *= (aspect_ratio_range[1] -
                        aspect_ratio_range[0])
    random_ratio += aspect_ratio_range[0]
    w = np.round(np.sqrt(target_area * random_ratio))     
    h = np.round(np.sqrt(target_area / random_ratio))
    if np.random.random() < 0.5:
        w, h = h, w
    w = min(w, img_w)
    w_rel = w / img_w
    w = int(w)
    h = min(h, img_h)
    h_rel = h / img_h
    h = int(h)
    x = np.random.random() * (img_w - w)
    x_rel = x / img_w
    x = int(x)
    y = np.random.random() * (img_h - h)
    y_rel = y / img_h
    y = int(y)
    img = img[y:y+h, x:x+w]
    new_targets = []
    for box in targets:
        cx = 0.5 * (box[0] + box[2])
        cy = 0.5 * (box[1] + box[3])
        if (x_rel < cx < x_rel + w_rel and
            y_rel < cy < y_rel + h_rel):
            xmin = (box[0] - x_rel) / w_rel
            ymin = (box[1] - y_rel) / h_rel
            xmax = (box[2] - x_rel) / w_rel
            ymax = (box[3] - y_rel) / h_rel
            xmin = max(0, xmin)
            ymin = max(0, ymin)
            xmax = min(1, xmax)
            ymax = min(1, ymax)
            box[:4] = [xmin, ymin, xmax, ymax]
            new_targets.append(box)
    new_targets = np.asarray(new_targets).reshape(-1, targets.shape[1])
    return img, new_targets