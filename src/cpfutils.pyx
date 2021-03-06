import numpy as np
cimport numpy as np
import operator
import math

def debug(msg):
	print 'debug_cpf: ', msg

cdef double edge_threshold = 0.1

def pyim2bw(double x):
	if x >= edge_threshold:
		return 1
	else:
		return 0

im2bw = np.frompyfunc(pyim2bw, 1, 1)
cdef double pi = np.pi

def pyangle2c(double x):
	if x < 0:
		x += pi

	if pi / 12 <= x < pi / 4:
		x = 1
	elif pi / 4 <= x < 5 * pi / 12:
		x = 2
	elif 5 * pi / 12 <= x < 7 * pi / 12:
		x = 3
	elif 7 * pi / 12 <= x < 3 * pi / 4:
		x = 4
	elif 3 * pi / 4 <= x < 11 * pi / 12:
		x = 5
	elif x < pi / 12 or x >= 11 * pi / 12:
		x = 6

	return x

angle2c = np.frompyfunc(pyangle2c, 1, 1)

def extractOCM(np.ndarray[np.uint8_t, ndim=2] pb):
	cdef np.ndarray[np.double_t, ndim=2] px, py
	px, py = np.gradient(pb)
	cdef np.ndarray[np.double_t, ndim=2] pa
	pa = np.arctan2(py, px)
	cdef np.ndarray[np.uint8_t, ndim=2] pc
	pc = angle2c(pa).astype(np.uint8)
	cdef list ocm = []
	cdef int i, j
	for i in range(pb.shape[0]):
		for j in range(pb.shape[1]):
			if pb[i][j] == 1:
				ocm.append((i, j, pc[i][j]))
	return ocm

# using the same radius (8) in CAO Yang's master thesis
cdef int radius = 8

cdef list __dx = [ 1,-1, 0, 0]
cdef list __dy = [ 0, 0, 1,-1]

def hitMap(np.ndarray[np.uint8_t, ndim=2] pb, list ocm):
	cdef dict q = {}

	cdef dict hmap = {}
	cdef int theta, pbs1, pbs2
	cdef np.ndarray[np.uint8_t, ndim=2] b
	cdef int x, y, t
	cdef int i, tx, ty, td, k

	for theta in range(1, 7):
		pbs1 = pb.shape[0]
		pbs2 = pb.shape[1]
		b = np.zeros([pbs1, pbs2], dtype = np.uint8)
		q[theta] = []

		for x, y, t in ocm:
			if t == theta:
				q[theta].append((x, y, 0))
				b[x, y] = 1

		i = 0
		while i < len(q[theta]):
			tx, ty, td = q[theta][i]
			if td < radius:
				for k in range(4):
					x = tx + __dx[k]
					y = ty + __dy[k]
					if 0 <= x < pb.shape[0] and 0 <= y < pb.shape[1] and not b[x][y]:
						b[x][y] = 1
						q[theta].append((x, y, td + 1))
			i += 1

		hmap[theta] = b

	return q, hmap

def getMatch(mData, np.ndarray[np.uint8_t, ndim=2] pb, list ocm):
	cdef dict hm
	cdef dict unused
	hm, unused = hitMap(pb, ocm)

	cdef dict match = {}
	cdef int theta, x, y, d, idx
	for theta in range(1, 7):
		for x, y, d in hm[theta]:
			if (x, y, theta) in mData.invIdx:
				for idx in mData.invIdx[(x, y, theta)]:
					if not idx in match:
						match[idx] = 1
					else:
						match[idx] += 1

	for idx in match:
		match[idx] = float(match[idx]) / mData.i2olen[idx]
		#match[idx] = float(match[idx]) / math.sqrt(mData.i2olen[idx])

	sorted_m = sorted(match.iteritems(), key = operator.itemgetter(1), reverse = True)

	return match, sorted_m

def getMatch2(mData, list qocm, list sorted_m, dict match, int topN):
	cdef int qocm_len = len(qocm)
	cdef dict hmap
	cdef int ind
	cdef double score1, score2
	cdef int x, y, theta
	for ind, score1 in sorted_m[:min(len(sorted_m), topN)]:
		hmap = mData.i2hmap[ind]
		score2 = 0
		for x, y, theta in qocm:
			if x < hmap[theta].shape[0] and y < hmap[theta].shape[1] and hmap[theta][x][y]:
				score2 += 1
		score2 = float(score2) / qocm_len
		match[ind] = math.sqrt(score1 * score2)
		#match[ind] = math.sqrt(score1 / math.sqrt(mData.i2olen[ind]) * score2)

	sorted_m = sorted(match.iteritems(), key = operator.itemgetter(1), reverse = True)

	return sorted_m

def normalize(pb):
	if pb.shape[0] != 200:
		l = (200 - pb.shape[0]) / 2
		r = 200 - pb.shape[0] - l
		lpb = np.zeros((l, 200))
		rpb = np.zeros((r, 200))
		pb = np.concatenate((lpb, pb, rpb))
	elif pb.shape[1] != 200:
		l = (200 - pb.shape[1]) / 2
		r = 200 - pb.shape[1] - l
		lpb = np.zeros((200, l))
		rpb = np.zeros((200, r))
		pb = np.concatenate((lpb, pb, rpb), 1)

	return pb
