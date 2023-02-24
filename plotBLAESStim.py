def plotBLAESStim(xyz, dPrime = None, roi_smoothing = 8, elec_size = 20, show_brain = True):
    """plotBLAESStim() uses the visbrain package (visbrain.org) to generate a 3D model of an brain w/ electrode contacts superimposed. Electrode locations (MNI XYZ coordinates) are defined in each patient's CSMap.mat file.

    Inputs:
        xyz (pd.DataFrame): X,Y,Z coordinates of electrodes (use MNI space if >1 patient).
        dPrime (pd.DataFrame, optional): dPrime values from behavioral testing; used to color electrodes.
        elec_size (float, optional): Marker size for electrode contact(s).
        roi_smoothing (int, optional): Amount of smoothing to apply to ROI voxels.
        
    Justin M. Campbell (justin.campbell@hsc.utah.edu)
    02/14/23
    """
        
    # Import libraries
    from visbrain.objects import BrainObj, ColorbarObj, SceneObj, SourceObj, RoiObj
    
    # Scene object
    scene_obj = SceneObj(bgcolor='white', size=(1000, 1000))
    
    # Brain object(s)
    if show_brain == True:
        brain_obj = BrainObj('B3', translucent = True)
        scene_obj.add_to_subplot(brain_obj, row=0, col=0, use_this_cam=True)
    
    # ROI object(s)
    roiAMY = RoiObj('aal')
    roiHC = RoiObj('aal')
    roiAMY.select_roi(roiAMY.where_is('amygdala'), translucent = True, smooth = roi_smoothing, roi_to_color={41: 'blue', 42: 'blue'})
    roiHC.select_roi(roiHC.where_is('hippocampus'), translucent = True, smooth = roi_smoothing, roi_to_color={37: 'green', 38: 'green'})
    scene_obj.add_to_subplot(roiAMY, row=0, col=0)
    scene_obj.add_to_subplot(roiHC, row=0, col=0)
    
    # Source object(s)
    if dPrime is not None:
        iEEG_obj = SourceObj('iEEG', xyz, radius_min = elec_size, edge_color = 'black', edge_width = 0.5)
        iEEG_obj.color_sources(data = dPrime, cmap = 'coolwarm')
        # Colorbar object
        CBAR_STATE = dict(cbtxtsz=15, txtsz=10, txtcolor = 'black', width=.1, cbtxtsh=3., rect=(-.3, -2., 1., 4.), clim = (dPrime.min(),dPrime.max()))
        cbar_obj = ColorbarObj(iEEG_obj, cblabel="d' Difference", **CBAR_STATE)
        scene_obj.add_to_subplot(cbar_obj, row=0, col=1, width_max=200)
    else:
        iEEG_obj = SourceObj('iEEG', xyz, color = (['#000000'] * len(xyz)), radius_min = elec_size) # All black
    scene_obj.add_to_subplot(iEEG_obj)

    # Preview
    scene_obj.preview()

### IMPLEMENTATION
import pandas as pd
datapath = '/Users/justincampbell/Library/CloudStorage/GoogleDrive-u0815766@gcloud.utah.edu/My Drive/Misc./BLAESCoords 021523.csv'       
BLAESCoords = pd.read_csv(datapath)
BLAESCoords = BLAESCoords.dropna()
xyz = BLAESCoords[['X', 'Y', 'Z']].to_numpy()
dPrime = BLAESCoords['dPrimeDiff_Item'].to_numpy()
if __name__ == "__main__":
    plotBLAESStim(xyz, dPrime)