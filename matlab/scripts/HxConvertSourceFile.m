%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (c) Copyright 2014 Hexoskin
% Permission to use, copy, modify, and distribute this software for any 
% purpose with or without fee is hereby granted, provided that the above 
% copyright notice and this permission notice appear in all copies. The 
% software is provided "as is" and the author disclaims all warranties with
% regard to this software including all implied warranties of
% merchantability and fitness. In no event shall the author be liable for
% any special, direct, indirect, or consequential damages or any damages
% whatsoever resulting from loss of use, data or profits, whether in an 
% action of contract, negligence or other tortious action, arising out of
% or in connection with the use or performance of this software.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% ConvertSourceFile    deprecated
% This function demonstrates and implements the decoding of binary data
% as downloaded grom the my.hexoskin.com dashboard. Datas are downloaded in
% binary (wav of hxd) format from the dashboard. The code converts them to
% a more "human-friendly" format, then saves it as a CSV in the same
% folder.


function HxConvertSourceFile(path)
% convertSourceFile(path) converts all raw wav or hxd contained in a folder
% to a more "human-friendly" format and saves it as a CSV in the same
% folder
%
%   path is the path to the folder where the wav and hxd are stored
if exist(path, 'dir')
    files = dir(path);
    for i = 1:length(files)
        if ~exist(fullfile(path,files(i).name ),'dir') && isempty(strfind(files(i).name,'CHAR'))  
            data = loadData(path, files(i).name);
            if length(data)
                disp(strcat('Converting file',files(i).name))
                saveCSV(data, path, files(i).name)
            end
        end
    end
else
   disp('Path does not exist.') 
end

function data = loadData(path, filename)
% data = loadData(path, filename) converts a particular file from wav or
% hxd to an array variable
%
%   data is the output array
%   path is the file to the path
%   filename is the name of the file

data = [];
if strcmpi(filename(end-2:end), 'wav')
    data = loadWave(path, filename);
elseif  strcmpi(filename(end-2:end), 'hxd')
    data = loadAsync(path, filename);
end


function data = loadWave(path, filename)
% data = loadWave(path, filename) load a wav (synchronous) file. The value
% are returned for each second. The time t=0 correspond to the beginning of
% the record.
%
%   data is the array output of the decoded data
%   path is the file to the path
%   filename is the name of the file

filename = fullfile(path, filename);
if exist('OCTAVE_VERSION', 'builtin')
    [y, Fs, nbits, opts] = wavread(filename);
else
    [y, Fs, nbits, opts] = wavread(filename, 'native');
end
if any(Fs == [ 256, 128,64])
    offset = -1;
else
    % This is for signal with frequency smaller or equal th one Hz
    offset = 0 ;
    Fs = 1/Fs;
end
y = double(y);
% Special case for acceleration data interpretation
if ~isempty(strfind(filename, 'ACC'))
    y(y < 0) = y(y < 0) + 2^16;
end
scale=getScale(filename);

if length(y) > 1
    data =y * [1, 1];
    for i1 = 1:length(y)
        data(i1, 1) = (i1 + offset)  / Fs ;
        data(i1, 2) =  data(i1, 2) *scale;
    end
else
    data = [];
end



function data = loadAsync(path, filename)
% data = loadAsync(path, filename) load an hxd (asynchronous) file. The
% value are returned in second. The time t=0 correspond to the beginning of
% the record.
%
%   data is the array output of the decoded data
%   path is the file to the path
%   filename is the name of the file

filename = fullfile(path, filename);
fid = fopen(filename);
data = [];
scale=getScale(filename);
[temp, count]= fread(fid, 2, 'int64');
f=1;
while count == 2
    data(f,1) = temp(1)/256;
    data(f,2) = temp(2)*scale;
    [temp, count]= fread(fid, 2, 'int64');
    f = f + 1;
end
fclose(fid);


function saveCSV(data, path, filename)
% saveTXT(path, filename, data) receives some data and saves it in CSV
% format. The first column contains the timestamps, and the second column
% contains values, if applicable.
%
%   data is the array output of the decoded data
%   path is the file to the path
%   filename is the name of the file

fileout = strrep(strrep(filename, 'hxd', 'csv'), 'wav', 'csv');
filename = fullfile(path, fileout);
dlmwrite(filename, data, 'delimiter', ',','precision', '%10.8f')


function scale=getScale(filename)
% scale=getScale(datatype) is used to get the scaling factor to use with
% the decoded data. It is necessary because the raw data stored on the
% database sometimes needs to be factored to be represented in a standard
% unit.
%
%   scale is the multiplicative factor to use with the datatype
%   filename is the name of the file, indicating which datatype is used

if ~isempty(strmatch(filename, { 'RR_interval.hxd', 'NN_interval.hxd', 'activity.wav', 'acceleration_X.wav', 'acceleration_Y.wav', 'acceleration_Z.wav'}))
    scale = 1/256;
elseif ~isempty(strmatch(filename, {'step.hxd', 'heartrate.wav','breathingrate.wav', 'inspiration.hxd','expiration.hxd','step.wav', 'cadence.wav', 'sleep_position.hxd', 'ECG_I.wav','ECG_II.wav','ECG_III.wav' }))
    scale = 1;
    
elseif ~isempty(strmatch(filename, { 'minute_ventilation.wav', 'tidal_volume.wav'}))
    scale = 13.28;
    
elseif ~isempty(strmatch(filename, { 'ANN.wav', 'SDNN.wav'}))
    scale = 1/256/16;
elseif ~isempty(strmatch(filename, { 'NN_over_RR.wav', 'HRV_LF_normalized.wav'}))
    scale = 1/10;
else
    scale = 1;
end

%% Example functions
% The functions below are not used above, they are presented here as
% examples of how to integrate hexoskin data with other programs.

function saveKubiosRR(path, rr)
% example to save the rr interval in a file format that is compatible
% with kubios rr ASCII file format
% Note it may be necessary to use the Kubios "custom ascii file import command",
% otherwise the rr file can be treated as a ECG file
%
%   path is the name of the path where to save the created file
%   rr is the rr intervals array, as decoded by the loadData function

filename = fullfile(path,'nn_kubios.txt');
dlmwrite(filename, rr,'delimiter', ' ')


function saveKubiosECG(path, ECG)
% example to save the ECG  in a file format that is compatible with kubios
% EKG ASCII file format
%
%   path is the name of the path where to save the created file
%   ECG is the ECG array, as decoded by the loadData function

filename = fullfile(path,'ECG_kubios.txt');
dlmwrite(filename, ECG, 'delimiter', ' ')


HxConvertSourceFile('/home/webert3/smoking_viz_data/participant_1/hexoskin/10-19-2018_13:31')
