import cv2

# 밝기 조절
def apply_brightness(frame, beta: int):
    beta = max(-100, min(100, int(beta)))
    return cv2.convertScaleAbs(frame, alpha=1.0, beta=beta)

# 가우시안 블러
def apply_blur(frame):
    return cv2.GaussianBlur(frame, (11, 11), 0)

# 색 반전(보색)
def apply_invert(frame):
    return cv2.bitwise_not(frame)

def apply_pixelate(frame, block_size: int = 16):
    # 너무 큰 block_size로 인해 0이 되지 않도록 최소 1 보장
    h, w = frame.shape[:2]
    small_w = max(1, w // block_size)
    small_h = max(1, h // block_size)
    # 축소 → 최근접 보간으로 확대
    small = cv2.resize(frame, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)