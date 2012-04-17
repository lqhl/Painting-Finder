from numpy import *

def debug(msg):
	print 'debug: ', msg

edge_threshold = 0.1

def pyim2bw(x):
	if x >= edge_threshold:
		return 1
	else:
		return 0

im2bw = frompyfunc(pyim2bw, 1, 1)

def pyangle2c(x):
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

angle2c = frompyfunc(pyangle2c, 1, 1)

def extractOCM(pb):
	px, py = gradient(pb)
	pa = arctan2(py, px)
	pa = angle2c(pa)
	ocm = []
	for i in range(pb.shape[0]):
		for j in range(pb.shape[1]):
			if pb[i][j] == 1:
				ocm.append((i, j, pa[i][j]))
	return ocm

# using the same radius (8) in CAO Yang's master thesis
radius = 8

__dx = [ 1,-1, 0, 0]
__dy = [ 0, 0, 1,-1]

def hitMap(pb):
	q = {}
	ocm = extractOCM(pb)

	hmap = {}
	for theta in range(1, 7):
		b = zeros(pb.shape, dtype = int8)
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

