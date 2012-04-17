import os
import pickle

from metadata import MetaData

data_dir = '../data/'

mData = MetaData('image_db')
for each in os.walk(data_dir):
	dirname, dirs, files = each
	if not files:
		continue
	for f in files:
		if f.endswith('.jpg') and not f.endswith('_contour.jpg'):
			mData.add(os.path.join(dirname, f))
mData.save()
print 'database saved'
