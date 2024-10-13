import cv2
import dlib
import numpy as np


predictor_path = "shape_predictor_68_face_landmarks.dat"  
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def analyze_and_calculate_pupil_iris(eye_region, gray_frame, eye_color_frame):
    # Get the bounding box around the eye
    x, y, w, h = cv2.boundingRect(np.array([eye_region]))
    eye_gray = gray_frame[y:y + h, x:x + w]
    eye_color = eye_color_frame[y:y + h, x:x + w]

    # Apply GaussianBlur to reduce noise
    blurred_eye = cv2.GaussianBlur(eye_gray, (5, 5), 0)

    # Thresholding to isolate the pupil (black area)
    _, pupil_threshold = cv2.threshold(blurred_eye, 30, 255, cv2.THRESH_BINARY_INV)

    # Thresholding to capture the iris (gray area surrounding pupil)
    _, iris_threshold = cv2.threshold(blurred_eye, 70, 255, cv2.THRESH_BINARY)

    # Find contours for pupil and iris
    pupil_contours, _ = cv2.findContours(pupil_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    iris_contours, _ = cv2.findContours(iris_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pupil_area = 0
    iris_area = 0
    pupil_center = None
    iris_center = None

    pupil_radius = 0
    iris_radius = 0

    
    if pupil_contours:
        largest_pupil = max(pupil_contours, key=cv2.contourArea)
        pupil_area = cv2.contourArea(largest_pupil)

        if pupil_area > 10:  
            if len(largest_pupil) >= 5:
                ellipse = cv2.fitEllipse(largest_pupil)
                pupil_center = (int(ellipse[0][0] + x), int(ellipse[0][1] + y))
                
                
                pupil_radius = int(np.sqrt(pupil_area / np.pi))  
                cv2.circle(eye_color_frame, pupil_center, pupil_radius, (0, 255, 0), 2)  

    
    if iris_contours:
        largest_iris = max(iris_contours, key=cv2.contourArea)
        iris_area = cv2.contourArea(largest_iris)

        if iris_area > 10:  
            if len(largest_iris) >= 5:
                moments = cv2.moments(largest_iris)
                if moments["m00"] != 0:
                    iris_center = (int(moments["m10"] / moments["m00"] + x), int(moments["m01"] / moments["m00"] + y))
                iris_radius = int(np.sqrt(iris_area / np.pi))  
                cv2.circle(eye_color_frame, iris_center, iris_radius, (255, 0, 0), 2)  

    
    pupil_area_calculated = np.pi * (pupil_radius ** 2) if pupil_radius > 0 else 0
    iris_area_calculated = np.pi * (iris_radius ** 2) if iris_radius > 0 else 0

    percentage = 0
    if iris_area_calculated > 0 and pupil_area_calculated <= iris_area_calculated:  
        percentage = (pupil_area_calculated / iris_area_calculated) * 100

    return pupil_center, iris_center, pupil_area, iris_area, percentage if pupil_area_calculated <= iris_area_calculated else None

def main():
    cap = cv2.VideoCapture('/Users/albertomtz/Documents/test/white_eyes.mp4')  

    left_eye_percentages = []
    right_eye_percentages = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video ended or unable to read the frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            left_eye_indices = list(range(36, 42))
            right_eye_indices = list(range(42, 48))

            left_eye_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in left_eye_indices])
            right_eye_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in right_eye_indices])

            # Analyze and calculate pupil and iris for left eye
            left_pupil_center, left_iris_center, left_pupil_area, left_iris_area, left_percentage = analyze_and_calculate_pupil_iris(
                left_eye_points, gray, frame
            )
            if left_percentage is not None:
                left_eye_percentages.append(left_percentage)

            
            right_pupil_center, right_iris_center, right_pupil_area, right_iris_area, right_percentage = analyze_and_calculate_pupil_iris(
                right_eye_points, gray, frame
            )
            if right_percentage is not None:
                right_eye_percentages.append(right_percentage)

        
        cv2.imshow("Pupil and Iris Tracking", frame)

       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    
    if left_eye_percentages:
        left_mean = np.mean(left_eye_percentages)
        print(f"Mean Left Eye Pupil Percentage: {left_mean:.2f}%")

    if right_eye_percentages:
        right_mean = np.mean(right_eye_percentages)
        print(f"Mean Right Eye Pupil Percentage: {right_mean:.2f}%")

    if left_eye_percentages and right_eye_percentages:
        combined_mean = np.mean(left_eye_percentages + right_eye_percentages)
        print(f"Mean Combined Eye Pupil Percentage: {combined_mean:.2f}%")

if __name__ == "__main__":
    main()
