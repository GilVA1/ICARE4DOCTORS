import cv2
import dlib
import numpy as np


predictor_path = "shape_predictor_68_face_landmarks.dat"  
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
blink_count = 0


def check_eye_redness(eye_region):
    hsv = cv2.cvtColor(eye_region, cv2.COLOR_BGR2HSV)

    lower_dark_red1 = np.array([0, 70, 30])
    upper_dark_red1 = np.array([10, 255, 150])
    lower_dark_red2 = np.array([160, 70, 30])
    upper_dark_red2 = np.array([180, 255, 150])

    lower_light_red1 = np.array([0, 50, 150])
    upper_light_red1 = np.array([10, 180, 255])
    lower_light_red2 = np.array([160, 50, 150])
    upper_light_red2 = np.array([180, 180, 255])

    mask_dark_red1 = cv2.inRange(hsv, lower_dark_red1, upper_dark_red1)
    mask_dark_red2 = cv2.inRange(hsv, lower_dark_red2, upper_dark_red2)
    mask_light_red1 = cv2.inRange(hsv, lower_light_red1, upper_light_red1)
    mask_light_red2 = cv2.inRange(hsv, lower_light_red2, upper_light_red2)

    combined_red_mask = mask_dark_red1 | mask_dark_red2 | mask_light_red1 | mask_light_red2

    red_pixel_count = np.sum(combined_red_mask > 0)
    total_pixels = eye_region.shape[0] * eye_region.shape[1]
    non_red_pixel_count = total_pixels - red_pixel_count

    red_percentage = (red_pixel_count / total_pixels) * 100 if total_pixels > 0 else 0
    return red_percentage, red_pixel_count, non_red_pixel_count

def eye_aspect_ratio(eye_points):
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])

    ear = (A + B) / (2.0 * C)
    return ear

def main():
    global blink_count  

    cap = cv2.VideoCapture('/Users/albertomtz/Documents/test/white_eyes.mp4')  
    running = True
    blink_threshold = 0.2
    redness_percentages = []

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            left_eye_indices = list(range(36, 42))
            right_eye_indices = list(range(42, 48))

            left_eye_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in left_eye_indices])
            right_eye_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in right_eye_indices])

            for (x, y) in left_eye_points:
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            for (x, y) in right_eye_points:
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            left_ear = eye_aspect_ratio(left_eye_points)
            right_ear = eye_aspect_ratio(right_eye_points)
            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < blink_threshold:
                blink_count += 1

            left_eye_region = frame[landmarks.part(37).y - 10:landmarks.part(40).y + 10,
                                    landmarks.part(36).x - 10:landmarks.part(39).x + 10]
            right_eye_region = frame[landmarks.part(43).y - 10:landmarks.part(46).y + 10,
                                     landmarks.part(42).x - 10:landmarks.part(45).x + 10]

            left_red_percentage, _, _ = check_eye_redness(left_eye_region)
            right_red_percentage, _, _ = check_eye_redness(right_eye_region)
            avg_red_percentage = (left_red_percentage + right_red_percentage) / 2

            redness_percentages.append(avg_red_percentage)

        cv2.imshow("Video with Eye Markings", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

    if redness_percentages:
        mean_redness = np.mean(redness_percentages)
        # DETERMINE IF EYES ARE RED OR NOT
        if mean_redness >= 80:  
            print("The eyes are red.")
        else:
            print("The eyes are not red.")
    else:
        print("No redness data collected.")

    print(f"Total Blinks: {blink_count}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
