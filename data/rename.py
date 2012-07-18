import os

for each in os.walk('.'):
	dirname, dirs, files = each
	if not files:
		continue
	i = 0
	for jpg in files:
		if jpg.endswith('.jpg'):
			i += 1
			newfile = '%d.jpg' % i
			os.rename(os.path.join(dirname, jpg), os.path.join(dirname, newfile))
