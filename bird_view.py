import numpy as np
import cv2


def perspective_transform(points, image_size, image):
	""" transform image to bird view.
	points: the 4 coordinates of image.
    """
	points_array = np.float32(points)
    width = image_size[0]
    height = image_size[1]
	image_dimensions = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
	transformation_matrix = cv2.getPerspectiveTransform(points_array, image_dimensions)
	transformed_image = cv2.warpPerspective(image, transformation_matrix, (width, height))
	return transformation_matrix, transformed_image


def perspective_transformation_for_points(matrix, points):
	""" transform every detected point to the bird view coordinate
    """
	detected_points = np.float32(points).reshape(-1, 1, 2)
	transformed_points = cv2.perspectiveTransform(detected_points, matrix)
	result = []
	for i in range(0,transformed_points.shape[0]):
		result += [[transformed_points[i][0][0], transformed_points[i][0][1]]]
	return result
