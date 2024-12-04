import cv2 as cv
import time
from collections import deque
import numpy as np
from scipy.signal import find_peaks

def detect_cars(video_file):
    Conf_threshold = 0.4
    NMS_threshold = 0.4

    COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0), 
              (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    class_name = []
    with open('classes.txt', 'r') as f:
        class_name = [cname.strip() for cname in f.readlines()]

    net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
    model = cv.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
    cap = cv.VideoCapture(video_file)
    starting_time = time.time()
    frame_counter = 0

    cv.namedWindow('frame', cv.WINDOW_NORMAL)
    cv.setWindowProperty('frame', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    car_counts = deque()  # Store (timestamp, car_count) tuples

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_counter += 1
        classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
        car_count = 0
        
        for (classid, score, box) in zip(classes, scores, boxes):
            if class_name[classid] == "car":  # assuming 'car' is the class name for cars in your classes.txt
                car_count += 1
                color = COLORS[int(classid) % len(COLORS)]
                label = f"{class_name[classid]} : {score:.2f}"
                cv.rectangle(frame, box, color, 2)
                cv.putText(frame, label, (box[0], box[1]-10), 
                           cv.FONT_HERSHEY_COMPLEX, 0.5, color, 2)

        current_time = time.time()
        car_counts.append((current_time, car_count))
        while car_counts and car_counts[0][0] < current_time - 30:
            car_counts.popleft()
        car_count_values = [count for _, count in car_counts]
        peaks, _ = find_peaks(car_count_values)
        if len(peaks) > 0:
            mean_peak_value = np.mean([car_count_values[i] for i in peaks])
        else:
            mean_peak_value = 0
        ending_time = time.time()
        fps = frame_counter / (ending_time - starting_time)
        cv.putText(frame, f'FPS: {fps:.2f}', (20, 50), 
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
        cv.putText(frame, f'Mean Peak Cars : {mean_peak_value:.2f}', (20, 80), 
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2)
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()
    return mean_peak_value

# Usage example:
#mean_peak_value = detect_cars('output.avi')
#print(f'Mean Peak Number of Cars Detected: {mean_peak_value}')