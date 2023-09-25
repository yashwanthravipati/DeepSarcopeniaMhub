"""
-------------------------------------------------
MHub - default run script for the 
       DeepSarcopenia pipeline
-------------------------------------------------

-------------------------------------------------
Author: Yash Ravipati
Email:  yravipati@bwh.harvard.edu
Date:   17.09.2023
-------------------------------------------------
"""

import sys
from mhubio.core import Config, DataType, FileType, CT, SEG
from mhubio.modules.importer.DicomImporter import DicomImporter
from mhubio.modules.convert.NrrdConverter import NrrdConverter
from mhubio.modules.convert.DsegConverter import DsegConverter
from mhubio.modules.organizer.DataOrganizer import DataOrganizer
#from mhubio.modules.runner.NNUnetRunner import NNUnetRunner
from models.DeepSarcopenia.utils.DeepSarcopeniaRunner import DeepSarcipeniaRunner

# clean-up
import shutil
shutil.rmtree("/app/data/sorted_data", ignore_errors=True)
shutil.rmtree("/app/data/preprocessed_data", ignore_errors=True)
shutil.rmtree("/app/tmp", ignore_errors=True)
shutil.rmtree("/app/data/output_data", ignore_errors=True)
shutil.rmtree("/app/models/DeepSarcopenia/output", ignore_errors=True)

# config
config = Config('/app/models/DeepSarcopenia/config/config.yml')
config.verbose = True  # TODO: define levels of verbosity and integrate consistently. 
config.debug = True

# import (ct:dicom)
DicomImporter(config).execute()

# convert (ct:dicom -> ct:nifti)
NrrdConverter(config).execute()


# execute model (ct:nifti + heart:nifti -> seg:nifti)
DeepSarcopeniaRunner(config).execute()

# convert (seg:nifti -> seg:dicomseg)
DsegConverter(config).execute()

# organize data into output folder
organizer = DataOrganizer(config)
organizer.set_file_permissions = sys.platform.startswith('linux')
#organizer.setTarget(DataType(FileType.DICOM, CT), "/app/data/output_data/[i:SeriesID]/dcm")
#organizer.setTarget(DataType(FileType.NIFTI, CT), "/app/data/output_data/[i:SeriesID]/image.nii.gz")
#organizer.setTarget(DataType(FileType.NIFTI, SEG), "/app/data/output_data/[i:SeriesID]/heart.nii.gz")
#organizer.setTarget(DataType(FileType.NRRD, SEG), "/app/data/output_data/[i:SeriesID]/[d:roi].nrrd")
organizer.setTarget(DataType(FileType.DICOMSEG, SEG), "/app/data/output_data/[i:sid]/DeepSarcopenia.dcm")
organizer.execute()