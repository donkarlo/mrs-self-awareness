Folders:

DATA: put here the Vocabulary and data for testing;

OUTPUT: folder where to output results or intermediate values. 
The code does not save anything for now.

Codes:

The main code for testing on MJPF is in Apply_MJPF.

Before making it run, set the parameters in Config. Config defines 
MJPF parameters such as number of particles and skewvalue; and the
name of folders where to read and where to save. Name of Vocabulary
file is also defined. Names of the testing files are instead in the 
main.

The other code files are:
- BuildVocabulary.py to load Vocabulary parameters;
- DistanceCalculations.py to calculate Bhattacharya and Kullback Leibler 
  distances;
- KF.py has Kalman Filter prediction and update;
- LoadData.py to load data from MATLAB files;
- DefineColors.py if colors are needed for plotting;