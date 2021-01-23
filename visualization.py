
import numpy as np 
import matplotlib.pyplot as plt
import os.path
import os
import re

# %%
def open_and_reshape(filename, n1, n2):
	X = np.fromfile(filename, dtype=np.float64)
	if (X.size != n1*n2):
		raise ValueError("Size of %s does not equal %dx%d" % (filename, n1, n2) )
		quit()
	X.shape = (n1, n2)
	return X



def view_heatmap(rho, cmap_name='inferno'):
	
	# fig, ax = plt.subplots(figsize=(4,4))
	fig, ax = plt.subplots()
	# n1, n2 = rho.shape 
	# fig, ax = plt.subplots(figsize=(1,n2/n1))
	ax.set_axis_off()
	fig.subplots_adjust(bottom=0, top=1, right=1, left=0)

	# colomaps I like: plasma, inferno, cividis, binary
	cmap = plt.get_cmap(cmap_name)
	ax.imshow(rho, cmap=cmap, interpolation='nearest')
	plt.show()



# Don't need this, use built-in plt.imsave() instead
# def create_heatmap(filename, rho, cmap_name='inferno'):
# 	# Create 4in x 4in figure (4in in case we also want to show() it -- better than 1in)
# 	# fig, ax = plt.subplots(figsize=(4,4))
# 	fig, ax = plt.subplots()
# 	ax.set_axis_off()
# 	fig.subplots_adjust(bottom=0, top=1, right=1, left=0)
# 	n1, n2 = rho.shape
# 	dpi = n1 / 4.0

# 	cmap = plt.get_cmap(cmap_name)
# 	ax.imshow(rho, cmap=cmap, interpolation='bicubic')
	
# 	fig.savefig(filename, dpi=dpi)



def parse_filename(filename):
	"""Parse filename of a frame. Example:
	
	Input:
	filename = '/fol/der/rho-001.data'

	Output:
	dirname 	= '/fol/der'
	prefix 	 	= 'rho-'
	index		= 1 		(integer)
	index_width = 3			(integer)
	extension	= '.data'	(can be empty)	   
	"""
	tmp, extension = os.path.splitext(filename)
	dirname, basename = os.path.split(tmp)

	prefix, index_string = re.split(r'(.*?)([0-9]+$)', basename)[1:3]
	index_width = len(index_string)		# number of digits, e.g. rho-0001.dat: 4, rho_000: 3
	index = int(index_string)

	return dirname, prefix, index, index_width, extension



def create_heatmap_movie(initial_filename, num_frames, n1, n2, cmap_name='inferno', movie_name='movie.mp4'):
	"""Create heatmap image files from binary files and assemble them into a movie.
	"""
	dirname, prefix, index, index_width, extension = parse_filename(initial_filename)

	rho = open_and_reshape(initial_filename, n1, n2)

	for k in range(num_frames+1):
		print(f'\rCreating frame {k}/{num_frames}...', end='')
		
		basename = os.path.join(dirname, prefix + f'{index+k:0{index_width}}')

		rho = open_and_reshape(basename + extension, n1, n2)
	
		plt.imsave(basename+'.png', rho, cmap=cmap_name)

	print("done")

	ffmpeg_cmd = f'ffmpeg -framerate 30 -i {dirname}/{prefix}%0{index_width}d.png -f mp4 -an -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p -r 30 {movie_name}'
	os.system(ffmpeg_cmd)




# %%
create_heatmap_movie('/Users/fun/Dropbox/work/recherche/ot/mattwonjunflavien/gf/wgfBFMcodes/data/rho-0000.dat', 80, 512, 512)
# %%
