import cv2
import time
from datetime import datetime
from pathlib import Path

def draw_rec_overlay(frame):
    # 좌상단에 빨간 원 + "REC" 텍스트
    cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (50, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

def main():
    # 0번 카메라 열기
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error : 카메라 열 수 없음")
        return

    # FPS 얻기(장치가 0을 반환하면 기본값 사용)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 1:
        fps = 30.0

    is_recording = False
    writer = None

    save_dir = Path(__file__).resolve().parent / "recordings"
    save_dir.mkdir(parents=True, exist_ok=True)

    # >>> NEW: 코덱 후보(확장자 포함) 자동 폴백 목록
    codec_candidates = [
        ("mp4v", ".mp4"),
        ("MJPG", ".avi"),
        ("XVID", ".avi"),
    ]

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error : 프레임을 읽을 수 없음")
                break

            # 거울 모드
            frame = cv2.flip(frame, 1)

            if is_recording:
                draw_rec_overlay(frame)
                writer.write(frame)

            # 프리뷰 창 표시
            cv2.imshow("Preview", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC : 종료
                break
            elif key == 32:  # Space : 녹화 토글
                if not is_recording:
                    h, w = frame.shape[:2]
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
                        print("Error: 모든 코덱 시도가 실패했습니다. 코덱/드라이버를 확인하세요.")
                    else:
                        is_recording = True
                        print(f"REC START (fps={fps}, size={w}x{h})")
                else:
                    is_recording = False
                    if writer is not None:
                        writer.release()
                        print("[INFO] VideoWriter released and file finalized.")
                        writer = None
                    print("REC STOP")

    finally:
        if writer is not None:
            writer.release()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()