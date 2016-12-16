import numpy as np

def min_result(list1, n):
	temp = list1
	result = list1
	window = 1
	for iter in range(n):
		temp = np.minimum(temp[0:(np.size(temp)-window)], temp[window:])
		result = np.concatenate((result, temp))
		window = window * 2
	return result


def max_result(list1, n):
	temp = list1
	result = list1
	window = 1
	for iter in range(n):
		temp = np.maximum(temp[0:(np.size(temp)-window)], temp[window:])
		result = np.concatenate((result, temp))
		window = window * 2
	return result

# list1, list2 are the average of the first and second moments of the datapoints
def avg_sd_result(list1, list2, n):
	temp1 = list1
	temp2 = list2
	result1 = temp1
	result2 = temp2
	window = 1
	for iter in range(n):
		temp1 = (temp1[0:(np.size(temp1)-window)] + temp1[window:])/2
		temp2 = (temp2[0:(np.size(temp2)-window)] + temp2[window:])/2
		result1 = np.concatenate((result1, temp1))
		result2 = np.concatenate((result2, temp2))
		window = window * 2
	result2 = np.sqrt(result2 - np.square(result1))
	return np.concatenate((result1, result2))

def min_max_avg_sd(stats, n):
	result_min = min_result(stats[:, 0], n)
	result_max = max_result(stats[:, 1], n)
	result_avg_sd = avg_sd_result(stats[:, 2], np.square(stats[:, 2]) + np.squares(stats[:, 3]), n)
	# result_avg_sd = avg_sd_result(stats[:, 2], np.square(stats[:, 2]) + np.squares(stats[:, 3]) * (1-1/np.stats[:, 4]), n)
	return np.concatenate((result_min, result_max, result_avg_sd))


# # Usage of the functions
# m = 168
# n = 7
# xx = np.concatenate((np.random.normal(0, 1, (m, 3)), np.zeros((m, 1))), axis = 1)
# result = min_max_avg_sd(xx, 7)
# np.size(result)
