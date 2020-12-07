import numpy as np
import itertools


def human_detection(boxes, scores, classes, image_size):
	"""
	human detect.
	"""
	box_list = []
    height = image_size[0]
    width = image_size[1]
	for i in range(boxes.shape[1]):
		if int(classes[i]) == 1 and scores[i] > 0.75:
			box = [boxes[0,i,0],boxes[0,i,1],boxes[0,i,2],boxes[0,i,3]] * np.array([height, width, height, width])
			box_list += [(int(box[0]), int(box[1]), int(box[2]), int(box[3]))]
	return box_list


def box_points(box):
	"""
	center point and ground point of box.
	"""
	center = (int(((box[1]+box[3])/2)), int(((box[0]+box[2])/2)))
	ground = (int(((box[1]+box[3])/2)), center[1] + ((box[2] - box[0])/2))
	return center, ground


def box_list_points(box_list):
	"""
	find center points and ground points for box list.
	"""
    center_list = []
    ground_list = []
	for i in enumerate(box_list):
        center, ground = box_points(i[1])
        center_list += [center]
		ground_list += [ground]
	return centroid_list, ground_list
