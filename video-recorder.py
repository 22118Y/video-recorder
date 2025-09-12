import cv2
from datetime import datetime
from pathlib import Path

from filters import apply_brightness, apply_blur, apply_invert, apply_pixelate

def draw_rec_overlay(frame):
    cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (50, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

KEY_UPS   = {2490368, 82}
KEY_DOWNS = {2621440, 84}

def main():
    # 0번 카메라 열기
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error : 카메라 열 수 없음.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 1:
        fps = 30.0

    is_recording = False
    writer = None

    save_dir = Path(__file__).resolve().parent / "recordings"
    save_dir.mkdir(parents=True, exist_ok=True)

    codec_candidates = [
        ("mp4v", ".mp4"),
        ("MJPG", ".avi"),
        ("XVID", ".avi"),
    ]

    current_filter = None
    brightness_beta = 0

    pixel_block_size = 16

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error : 프레임을 읽을 수 없음.")
                break

            # 거울 모드
            frame = cv2.flip(frame, 1)

            filtered = frame
            if current_filter == 'brightness':
                filtered = apply_brightness(filtered, brightness_beta)
            elif current_filter == 'blur':
                filtered = apply_blur(filtered)
            elif current_filter == 'invert':
                filtered = apply_invert(filtered)
            elif current_filter == 'pixelate':
                filtered = apply_pixelate(filtered, block_size=pixel_block_size)

            preview_frame = filtered.copy()
            if is_recording:
                if writer is not None and writer.isOpened():
                    writer.write(filtered)
                else:
                    print("[WARN] writer가 열려있지 않아 프레임을 쓰지 못함.")
                draw_rec_overlay(preview_frame)

            cv2.imshow("Preview", preview_frame)

            key = cv2.waitKeyEx(1) & 0xFFFFFFFF

            if key == 27:
                break

            elif key == 32:
                if not is_recording:
                    h, w = filtered.shape[:2]
                    opened = False
                    for fourcc_name, ext in codec_candidates:
                        fourcc = cv2.VideoWriter_fourcc(*fourcc_name)
                        filename = save_dir / f"record_{datetime.now():%Y%m%d_%H%M%S}{ext}"
                        writer = cv2.VideoWriter(str(filename), fourcc, fps, (w, h))
                        if writer.isOpened():
                            opened = True
                            print(f"[INFO] VideoWriter opened with {fourcc_name}, file: {filename}")
                            break
                        else:
                            writer.release()
                            writer = None
                            print(f"[WARN] Failed to open writer with {fourcc_name}, trying next...")

                    if not opened:
                        print("Error: 모든 코덱 시도 실패. 코덱/드라이버 확인 바람.")
                    else:
                        is_recording = True
                        print(f"REC START (fps={fps}, size={w}x{h}, filter={current_filter}, beta={brightness_beta})")
                else:
                    is_recording = False
                    if writer is not None:
                        writer.release()
                        print("[INFO] VideoWriter released and file finalized.")
                        writer = None
                    print("REC STOP")


            elif key in (ord('a'), ord('A')):   # 밝기 모드 토글
                if current_filter == 'brightness':
                    current_filter = None
                    print("Filter OFF: brightness")
                else:
                    current_filter = 'brightness'
                    print("Filter ON : brightness (↑/↓로 밝기 조절)")

            elif key in (ord('s'), ord('S')):   # 블러 토글
                if current_filter == 'blur':
                    current_filter = None
                    print("Filter OFF: blur")
                else:
                    current_filter = 'blur'
                    print("Filter ON : blur")

            elif key in (ord('d'), ord('D')):   # 반전(보색) 토글
                if current_filter == 'invert':
                    current_filter = None
                    print("Filter OFF: invert")
                else:
                    current_filter = 'invert'
                    print("Filter ON : invert")

            elif key in (ord('f'), ord('F')):   # 픽셀화 토글
                if current_filter == 'pixelate':
                    current_filter = None
                    print("Filter OFF: pixelate")
                else:
                    current_filter = 'pixelate'
                    print("Filter ON : pixelate")

            # --- 밝기 모드에서만 ↑/↓로 밝기 조절 ---
            elif current_filter == 'brightness' and (key in KEY_UPS or key in KEY_DOWNS):
                step = 5
                if key in KEY_UPS:
                    brightness_beta = min(100, brightness_beta + step)
                elif key in KEY_DOWNS:
                    brightness_beta = max(-100, brightness_beta - step)
                print(f"brightness beta = {brightness_beta}")

    finally:
        if writer is not None:
            writer.release()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()