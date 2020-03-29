import numpy as np
from PIL import Image

filename = 'rabbitPic'

img = Image.open( filename + '.png' )
data = np.array( img, dtype='uint8' )
np.save( filename + '.npy', data)

