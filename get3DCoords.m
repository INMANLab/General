function get3DCoords(pID, savepath)
% get3DCoords takes a patient ID (pID) as input and the path for where 
% to save the data (savepath) to export the following:
%
%   XYZ_MNI:    coordinates of electrode contacts in MNI space
%   XYZ:        coordinates of electrode contacts in patient space
%   vertices:   vertices for 3D model of patient brain
%   faces:      faces for 3D model of patient brain
%
% e.g., get3DCoords('UIC202302', 'G:\My Drive\Data\UIC202302\')
% Justin Campbell (03/21/23)
%%

% Load preprocessed files (LeGUI pipeline)
ptPath = strcat('Z:\', pID, '\Imaging\Registered\');
load(strcat(ptPath, 'Electrodes.mat')); % load electrode info
load(strcat(ptPath, 'Surfaces.mat')); % load 3d model info

% Extract coordinates
XYZ_MNI     = ElecXYZMNIProjRaw;
XYZ         = ElecXYZProjRaw;
vertices    = BrainSurfRaw.vertices;
faces       = BrainSurfRaw.faces;

% Remove microelectrodes
XYZ(MicroElecRaw,:) = NaN;
XYZ = rmmissing(XYZ);
XYZ_MNI(MicroElecRaw,:) = NaN;
XYZ_MNI = rmmissing(XYZ_MNI);

% Export
writematrix(XYZ_MNI, fullfile(savepath, strcat(pID, '_XYZ_MNI.csv')));
writematrix(XYZ, fullfile(savepath, strcat(pID, '_XYZ.csv')));
writematrix(vertices, fullfile(savepath, strcat(pID, '_vertices.csv')));
writematrix(faces, fullfile(savepath, strcat(pID, '_faces.csv')));

% Display
fprintf('Files saved to %s \n', savepath);

end