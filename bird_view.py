import cv2
import numpy as np


# points: the 4 points of the region that we picked by hand
def get_perspective_transform(points, height, width):
    source = np.float32(np.array(points))
    destination = np.float32([[0, height], [width, height], [width, 0], [0, 0]])
    perspective_transform = cv2.getPerspectiveTransform(source, destination)
    return perspective_transform


# human_boxes: the points of bounding box of all detected human
def get_perspective_points(human_boxes, prespective_transform):
    perspective_points = []
    for human in human_boxes:
        points = np.array([[[int(human[0] + (human[2] * 0.5)), int(human[1] + human[3])]]], dtype="float32")
        perspective_point = cv2.perspectiveTransform(points, prespective_transform)[0][0]
        point = (int(perspective_point[0]), int(perspective_point[1]))
        perspective_points += [point]
    return perspective_points


# measured_distance: list of list, the 1st element is distance, the 2nd and 3rd elements are the points of the boxes of two people
# height, width: height and width of bird eye view
def bird_eye_view(height, width, measured_distance, perspective_points):
    red = (0, 0, 255)
    green = (0, 255, 0)
    white = (200, 200, 200)

    # white picture, 8-bit unsigned integer (0 to 255)
    result_frame = np.zeros((int(height), int(width), 3), np.uint8)
    result_frame[:] = white
    unsafe = []
    safe = []

    for i in range(len(measured_distance)):
        if measured_distance[i][0] <= 2:  # the unsafe distance is 2m
            if (measured_distance[i][1] not in unsafe) and (measured_distance[i][1] not in safe):
                unsafe += [measured_distance[i][1]]
            if (measured_distance[i][2] not in unsafe) and (measured_distance[i][2] not in safe):
                unsafe += [measured_distance[i][2]]
            result_frame = cv2.line(result_frame, int(measured_distance[i][1][0]), int(measured_distance[i][1][1]),
									int(measured_distance[i][2][0]), int(measured_distance[i][2][1]), red, 2)

    for human in perspective_points:
        if human not in unsafe:
            safe += [human]

    for plot in safe:
        result_frame = cv2.circle(result_frame, (int(plot[0]), int(plot[1])), 5, green, 10)
    for plot in unsafe:
        result_frame = cv2.circle(result_frame, (int(plot[0]), int(plot[1])), 5, red, 10)

    return result_frame


# safe_distance_points: the 3 points we picked for safe distance
# the 1st and 2nd points define horizontal distance
# the 1st and 3rd points define vertical distance
def measure_distance(safe_distance_points, prespective_transform, perspective_points):
    safe_distance_points = np.float32(np.array(safe_distance_points))
    safe_distance_point = cv2.perspectiveTransform(safe_distance_points, prespective_transform)[0]
    horizontal_distance = np.sqrt((safe_distance_point[0][0] - safe_distance_point[1][0]) ** 2 +
								  (safe_distance_point[0][1] - safe_distance_point[1][1]) ** 2)
    vertical_distance = np.sqrt((safe_distance_point[0][0] - safe_distance_point[2][0]) ** 2 +
								(safe_distance_point[0][1] - safe_distance_point[2][1]) ** 2)

    measured_distance = []
    for human1 in perspective_points:
        for human2 in perspective_points:
            if human1 != human2:
                dis_x = float((abs(human2[0] - human1[0]) / horizontal_distance) * 2)
                dis_y = float((abs(human2[1] - human1[1]) / vertical_distance) * 2)
                distance = int(np.sqrt(((dis_x) ** 2) + ((dis_y) ** 2)))
                measured_distance.append([distance, human1, human2])
    return measured_distance
