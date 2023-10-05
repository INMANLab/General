def plotPtBrain(xyz, dPrime = None, faces = None, vertices = None, roi_smoothing = 8, elec_size = 16, show_brain = True):
    """plotPtBrain() uses the visbrain package (visbrain.org) to generate a 3D model of a specific patient's brain w/ electrode contacts superimposed. Electrode locations (MNI XYZ coordinates) are defined in each patient's CSMap.mat file.

    Inputs:
        xyz (pd.DataFrame): X,Y,Z coordinates of electrodes (use MNI space if >1 patient).
        dPrime (pd.DataFrame, optional): dPrime values from behavioral testing; used to color electrodes.
        faces (pd.DataFrame, optional): faces for 3D model of patient brain.
        vertices (pd.DataFrame, optional): vertices for 3D model of patient brain.
        elec_size (float, optional): Marker size for electrode contact(s).
        roi_smoothing (int, optional): Amount of smoothing to apply to ROI voxels.
        
    Justin M. Campbell (justin.campbell@hsc.utah.edu)
    03/21/23
    """
        
    # Import libraries
    from visbrain.objects import BrainObj, ColorbarObj, SceneObj, SourceObj, RoiObj
    
    # Scene object
    scene_obj = SceneObj(bgcolor='white', size=(1000, 1000))
    
    # Brain object(s)
    if show_brain == True:
        brain_obj = BrainObj('white', faces = faces, vertices = vertices, translucent = True)
        scene_obj.add_to_subplot(brain_obj, row=0, col=0, use_this_cam=True)
    
    # ROI object(s)
    roiAMY = RoiObj('aal')
    roiHC = RoiObj('aal')
    roiAMY.select_roi(roiAMY.where_is('amygdala'), translucent = True, smooth = roi_smoothing, roi_to_color={41: 'blue', 42: 'blue'})
    roiHC.select_roi(roiHC.where_is('hippocampus'), translucent = True, smooth = roi_smoothing, roi_to_color={37: 'green', 38: 'green'})
    scene_obj.add_to_subplot(roiAMY, row=0, col=0)
    scene_obj.add_to_subplot(roiHC, row=0, col=0)
    
    # Source object(s)
    iEEG_obj = SourceObj('iEEG', xyz, color = (['#000000'] * len(xyz)), radius_min = elec_size) # All black
    scene_obj.add_to_subplot(iEEG_obj)

    # Preview
    scene_obj.preview()

### IMPLEMENTATION
import pandas as pd
datapath = '/Users/justincampbell/Library/CloudStorage/GoogleDrive-u0815766@gcloud.utah.edu/My Drive/Research Projects/BLAES/Data/3DBrains/'
pID = 'UIC202302'
xyz = pd.read_csv((datapath + pID + '_XYZ.csv')).to_numpy()
faces = pd.read_csv((datapath + pID + '_faces.csv'))
vertices = pd.read_csv((datapath + pID + '_vertices.csv'))

if __name__ == "__main__":
    plotPtBrain(xyz, faces = faces, vertices = vertices) # patient brain
