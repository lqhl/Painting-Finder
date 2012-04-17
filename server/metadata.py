from numpy import *
import scipy.io as spio
import os
try:
	import cPickle as pickle
except:
	import pickle

from pfutils import *

class MetaData:
	def __init__(self, dbname = 'image_db'):
		self.dbname = dbname

		self.tot = 0
		self.i2name = {}
		self.name2i = {}
		self.invIdx = {}
		self.i2olen = {}
		self.i2hmap = {}

	def load(self, dbname = 'image_db'):
		self.dbname = dbname
		with open(dbname + '.pkl', 'rb') as f:
			self.tot = pickle.load(f)
			self.i2name = pickle.load(f)
			self.name2i = pickle.load(f)
			self.invIdx = pickle.load(f)
			self.i2olen = pickle.load(f)
		with open(dbname + '.hmap.pkl', 'rb') as f:
			self.i2hmap = pickle.load(f)

	def save(self):
		with open(self.dbname + '.pkl', 'wb') as f:
			pickle.dump(self.tot, f, protocol = pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.i2name, f, protocol = pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.name2i, f, protocol = pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.invIdx, f, protocol = pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.i2olen, f, protocol = pickle.HIGHEST_PROTOCOL)
		with open(self.dbname + '.hmap.pkl', 'wb') as f:
			pickle.dump(self.i2hmap, f, protocol = pickle.HIGHEST_PROTOCOL)

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

		pb = im2bw(pb).astype(int8)
		unused, hmap = hitMap(pb)
		self.i2hmap[ind] = hmap

		ocm = extractOCM(pb)
		self.i2olen[ind] = len(ocm)
		for each in ocm:
			self.addIndex(each, ind)

	def addIndex(self, item, ind):
		if not item in self.invIdx:
			self.invIdx[item] = []
		self.invIdx[item].append(ind)
