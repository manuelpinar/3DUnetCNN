# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 08:55:53 2020

@author: Manuel Pinar-Molina
"""

import os
import sys
import re
import nrrd
import nibabel as nib
import numpy as np
import argparse
from natsort import natsorted
import shutil
from seg_extend import extend

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)


'''
Call:
python nrrd_to_nifty.py --path_in ..data\datos_son_espases\Casos --path_out ..data\datos_son_espases\Casos_nifty
'''

parser = argparse.ArgumentParser()
parser.add_argument('--path_in', default = os.path.join(ROOT_DIR, "data\datos_son_espases\Casos"))
parser.add_argument('--path_out', default = os.path.join(ROOT_DIR, "data\datos_son_espases\Casos_nifty"))



parsed_args = parser.parse_args(sys.argv[1:])

path_in = parsed_args.path_in
path_out = parsed_args.path_out

if not os.path.exists(path_out):
    os.mkdir(path_out)

for folder in natsorted(os.listdir(path_in)):

    path_casos = os.path.join(path_in, folder)

    
    readdata, header = nrrd.read(os.path.join(path_casos, "data.nrrd"))
    readseg, header_seg = nrrd.read(os.path.join(path_casos, "seg.nrrd"))
     
    #Extend the segmented image to the same size like data_image, using seg_extend.py
    segmentation_extend = extend(readdata, readseg)
    segmentation_extend = segmentation_extend/255
    
    path_nifty = os.path.join(path_out, folder)
    if not os.path.exists(path_nifty):
        os.mkdir(path_nifty)

    
    data_nii, seg_nii = nib.Nifti1Image(readdata, affine=np.eye(4, 4)), nib.Nifti1Image(segmentation_extend, affine=np.eye(4, 4))
       
    nib.save(data_nii, os.path.join(path_out, "data.nii"))
    nib.save(seg_nii, os.path.join(path_out, "seg.nii"))

    data_source, seg_source = os.path.join(path_out, "data.nii"), os.path.join(path_out, "seg.nii")
       
    shutil.move(data_source, path_nifty)
    shutil.move(seg_source, path_nifty)
        
    