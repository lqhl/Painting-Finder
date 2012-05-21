import scipy as sp
import operator
from pylab import *
from numpy import *
from PIL import Image
from time import clock
import cProfile as profile

from metadata import *
try:
	from cpfutils import *
except:
	from pfutils import *

def debug_t(msg):
	debug('time used: %f' % (clock() - debug_t.tstamp))
	debug(msg)
	debug_t.tstamp = clock()
debug_t.tstamp = clock()

def test():
	debug('loading database')
	mData = MetaData()
	mData.load()

	debug_t('loading mat file')

	fnames = ['test%d.jpg' % i for i in range(1, 7)]
	figure(figsize = (30, 18))
	for i, fname in enumerate(fnames):
		pb = (255 - array(Image.open(fname))) / 255.0

		imnames = query(mData, pb)

		subplot(6, 10, i * 10 + 1)
		gray()
		imshow(pb)
		axis('off')

		# figure()
		for j, imname in enumerate(imnames[:9]):
			subplot(6, 10, i * 10 + 2 + j)
			imshow(array(Image.open(imname)))
			axis('off')
	savefig('6-result.eps')

def test2():
	debug('loading database')
	mData = MetaData()
	mData.load()

	debug_t('loading mat file')


	fnames = ['apple', 'pisa tower', 'eiffel tower', 'golden gate', 'butterfly', 'teapot']
	figure(figsize = (30, 18))
	for i, fname in enumerate(fnames):
		matname = '../data/%s/3.mat' % fname
		data = sp.io.loadmat(matname)
		pb = data['pb']
		pb = normalize(pb)

		imnames = query(mData, pb)

		subplot(6, 10, i * 10 + 1)
		gray()
		imshow(pb)
		axis('off')

		# figure()
		for j, imname in enumerate(imnames[:9]):
			subplot(6, 10, i * 10 + 2 + j)
			imshow(array(Image.open(imname)))
			axis('off')
	savefig('6-result.eps')

def test_topN():
	debug('loading database')
	mData = MetaData()
	mData.load()

	res = []
	dp = '../data'
	fnames = os.listdir(dp)
	fnames = ['folding fan', 'dragonfly', 'letter a', 'daisy', 'gun', 'bag', 'desk lamp', 'eiffel tower', 'teapot', 'apple', 'golden gate', 'stapler', 'horse', 'temple of heaven', 'watch', 'starfish', 'smiley face']
	topNs = [10, 20, 40, 60, 80, 100, 160, 200, 500]
	ans = []
	for topN in topNs:
		for fname in fnames:
			if not os.path.isdir(os.path.join(dp, fname)) or fname.startswith('2'):
				continue
			debug_t('calc %s' % fname)
			matname = os.path.join(dp, fname, '1.mat')
			data = sp.io.loadmat(matname)
			pb = data['pb']
			pb = normalize(pb)

			imnames = query(mData, pb, topN)[:10]
			hits = 0
			for imname in imnames:
				if imname.startswith(os.path.join(dp, fname)):
					hits += 1
			res.append((fname, float(hits) / len(imnames)))
		with open('top%d.txt' % topN, 'w') as fo:
			for each in res:
				fo.write('%s: %f\n' % each)
			tmp = map(lambda x : x[1], res)
			avg = sum(tmp) / len(tmp)
			fo.write('average: %f\n' % avg)
			ans.append(avg)
	print topNs
	print ans
	#plot(topN, ans)
	#savefig('topN.eps')

def query(mData, pb, topN = 200):
	debug_t('one side match')

	pb = im2bw(pb).astype(uint8)
	qocm = extractOCM(pb)
	match, sorted_m = getMatch(mData, pb, qocm)

	debug_t('two side match')

	sorted_m = getMatch2(mData, qocm, sorted_m, match, topN)

	debug_t('finish two side match')

	lenRes = 30
	imnames = []
	for i in range(min(lenRes, len(sorted_m))):
		imname = mData.i2name[sorted_m[i][0]]
		imnames.append(imname)
		debug('name: %s, score: %f' % (imname, sorted_m[i][1]))

	return imnames

if __name__ == '__main__':
	test_topN()
	# profile.run('test()')
