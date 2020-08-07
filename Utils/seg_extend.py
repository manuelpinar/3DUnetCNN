# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 5 08:55:53 2020

@author: Manuel Pinar-Molina
"""
import numpy as np

'''
Normalize the original data with values between 0-255
'''

def normalize(original):
    readdata_norm = np.array(original) + abs(np.min(original))
    readdata_norm = readdata_norm/ np.max(readdata_norm)
    readdata_norm = readdata_norm*255
    
    return readdata_norm

'''
Set all values < threshold at 0 
'''

def adapt_image(image, threshold=128):
    image_2 = np.copy(image)
    indexes = np.argwhere(image_2<threshold)
    image_2[indexes[:,0],indexes[:,1],indexes[:,2]]=0
    
    return image_2

'''
Take only 3 layers of image and the filter in order to calculate the convolution with less layers and less operations
'''

def layers(image,filt,p1):    
    tmp1 = int(p1/4)
    cortes = [tmp1, 2*tmp1, 3*tmp1]
    image2 = image[:,:,cortes]
    filtro2 = filt[:,:,cortes]
    return image2, filtro2

'''
This function extends the segmented image to the same size as original_data, 
also locates the position of the segmented image and regrows the image while maintaining the original position of the segmented image. 
To do this, it convolves the segmented image (used as a convolution filter) over the data image, subtracting one image from the other, 
this operation is saved in a matrix and then the minimum value is searched to know the position it was in.
'''
def extend(im, fil):

    im = normalize(im)
    im = adapt_image(im)
    
    fil = normalize(fil)
    
    f1, c1, p1 = np.shape(im)
    f2, c2, p2 = np.shape(fil)
    im2, fil2 = layers(im,fil,p1) 
    
    conv = np.zeros((1+f1-f2,1+c1-c2))
    for k in range(1+f1-f2):
        for j in range(1+c1-c2):
            conv[k,j] = np.sum(np.absolute(fil2-im2[k:k+f2,j:j+c2,:]))

    minimo = np.min(conv)
    f, c = np.where(conv==minimo)
    f = f[0]
    c = c[0]

 
    
    final_filter = np.zeros(np.shape(im))
    final_filter[f:f+f2,c:c+c2,:] = fil
    
    return final_filter
