"""
-------------------------------------------------
MHub - run the DeepSarcopenia pipeline
-------------------------------------------------

-------------------------------------------------
Author: Yash Ravipati
Email:  yravipati@bwh.harvard.edu
-------------------------------------------------
"""

import os, subprocess, shutil
from mhubio.core import Instance, InstanceData, IO
from mhubio.modules.runner.ModelRunner import ModelRunner

@IO.Config('batchsize', int, 64, the='Number of slices to be processed simultaneously. A smaller batch size requires less memory but may be slower.')

class DeepSarcopeniaRunner(ModelRunner):
    
    #batchsize: int

    @IO.Instance()
    @IO.Input('image', 'nrrd:mod=ct',  the='input ct scan')
#    @IO.Output('roi1_lungs', 'roi1_lungs.nii.gz', 'nifti:mod=seg:model=LungMask:roi=RIGHT_LUNG,LEFT_LUNG', bundle='model', the='predicted segmentation of the lungs')
#    @IO.Output('roi2_lunglobes', 'roi2_lunglobes.nii.gz', 'nifti:mod=seg:model=LungMask:roi=LEFT_UPPER_LUNG_LOBE,LEFT_LOWER_LUNG_LOBE,RIGHT_UPPER_LUNG_LOBE,RIGHT_MIDDLE_LUNG_LOBE,RIGHT_LOWER_LUNG_LOBE', bundle='model', the='predicted segmentation of the lung lobes')

    def task(self, instance: Instance, image: InstanceData, roi1_lungs: InstanceData, roi2_lunglobes: InstanceData) -> None:
        

        # bash command for the C3 Slice Selction *
        bash_command  = ["DeepSarcoepnia"]
        bash_command += [image.abspath]         # path to the input_file
        bash_command += [csv.abspath]    # path to the output file
        bash_command += ["--modelname", "C3_Top_Selection_Model"] # specify lung segmentation model

        self.v("Running the C3 Selection.")
        self.v(">> run C3 Selection (): ", " ".join(bash_command))
       
        # bash command for the C3 Slice Selction *
        bash_command  = ["DeepSarcoepnia"]
        bash_command += [image.abspath]         # path to the input_file
        bash_command += [preprocess.abspath]    # path to the output file
        
        self.v("Running the C3 Preprocess.")
        self.v(">> run C3 Preprocess (): ", " ".join(bash_command))

      # bash_command += ["--modelname", "C3_Top_Selection_Model"] # specify lung segmentation model

      
        # bash command for the C3 segmentation *
        bash_command  = ["DeepSarcoepnia"]
        bash_command += [image.abspath]         # path to the input_file
        bash_command += [segmentation.abspath]    # path to the output file
        bash_command += ["--modelname", "C3_Top_Segmentation_Model"] # specify lung segmentation model

        self.v("Running the C3 segmentation.")
        self.v(">> run C3 Segmentation (): ", " ".join(bash_command))
        
        # run the lung segmentation model
        bash_return = subprocess.run(bash_command, check=True, text=True)


        # bash command for the lung lobes segmentation (fusion)
#        bash_command  = ["lungmask"]
#        bash_command += [image.abspath]                   # path to the input_file
#        bash_command += [roi2_lunglobes.abspath]          # path to the output file
#        bash_command += ["--modelname", "LTRCLobes_R231"] # specify lung lobes seg model

#        self.v("Running the lung lobes segmentation (with model fusion).")
#        self.v(">> run lungmask (LTRCLobes_R231): ", " ".join(bash_command))
        
        # run the lung lobes segmentation model
#        bash_return = subprocess.run(bash_command, check=True, text=True)