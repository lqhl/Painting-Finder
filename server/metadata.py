from numpy import *
import scipy.io as spio
import os

from pfutils import *

class MetaData:
	def __init__(self):
		self.tot = 0
		self.i2name = {}
		self.name2i = {}
		self.invIdx = {}
		self.i2olen = {}

	def add(self, name):
		# check name is '*.jpg', not contour image (not '*_contour.jpg') and was preprocessed (has '*.mat')
		if name in self.name2i:
			return False
		matname = name[:-4] + '.mat'
		if not (os.path.exists(matname) and os.path.exists(name[:-4] + '_contour.jpg')):
			return False

		self.tot += 1
		debug('adding %dth: %s' % (self.tot, name))
		ind = self.tot
		self.i2name[ind] = name
		self.name2i[name] = ind

		data = spio.loadmat(matname)
		pb = data['pb']

		ocm = extractOCM(pb)
		self.i2olen[ind] = len(ocm)
		for each in ocm:
			self.addIndex(each, ind)

	def addIndex(self, item, ind):
		if not item in self.invIdx:
			self.invIdx[item] = []
		self.invIdx[item].append(ind)
