# Automated analysis of _drosophila melanogaster_ wing imaginal disc intensity measurements
This Project is a collaboration with Shinya Matsuda. The aim of this 
project is to facilitate the analysis and comparison of intensity 
measurements of wing discs. Two scripts were generated for this project.
- [wing_disc-alignment.py](../blob/master/wing_disc-alignment.py)
- [wingdisc_comparision.py](../blob/master/wingdisc_comparison_v5.py)

## Automated alignment of wing imaginal disc intensity measurements
The script [wing_disc-alignment.py](../blob/master/wing_disc-alignment.py)
takes one or multiple excel file(s) like [wingdiscs.xlsx](../blob/master/wingdiscs.xlsx)
as input. One excel files corresponds to one experimental condition (e.g. WT).
Each sheet of this Excel file corresponds to one analysed wing imaginal disc, containing
the x-value, the intensity value and the x-correction value. The x-correction value
will be used to normalize the x-values. Once the data is preprocessed it will be merged 
and aligned in two databases. In database one __<name>\_no\_min_sub.xlsx__ the raw data loaded.
In the second database __<name>\_min\_sub__, the intensity is normalized by substraction of the minimum
intensity value. (This normalization does not change the relative Intensity differences 
therefore the Intensity profile is not changed.) For both datasets/databases the average, the standard 
deviation and the number of values in each row are calculated. Further the database is 
exported as excel file and a comparison plot is generated.

NEW FEATURE: You can pick as many experiments as you want at once, it will process them one after the other !!!

In order to facilitate the analysis for the User, standalone executables
for Windows and macOS were generated. This allows any (macOS or windows) 
user to operate the programs without prior installation of Python.


## Automated merge and comparison of multiple datasets
The results generated with [wing_disc-alignment.py](../blob/master/wing_disc-alignment.py) can further be analysed with 
[wingdisc_comparision.py](../blob/master/wingdisc_comparison_v5.py).
This script will normalize the data according to the operator’s choices and combine the different experimental 
conditions in one excel file. It allows to select a control (e.g. wild type expression pattern) with (unlimited) mutant 
conditions. Based on Shinya Matsuda’s needs, the following options were integrated: The operator can choose between three
options to normalize the datasets:
- __(option: "y")__ substract the minimum of the control from the Intensity values of each condition,
- __(option "n")__ the minimum value of each condition is used for normalization  
- __(option "no_min")__ no normalization is performed. 

The data is processed depending on the previous choice and the results are combined in an excel file.
Additionally, a Summary Plot is generated automatically for quick control and analysis.

In order to facilitate the analysis for the User, standalone executables for Windows and macOS were generated.
This allows any (macOS or windows) user to operate the programs without prior installation of Python.

If you would like me to automate your (tedious ;) analysis or you have 
questions, don't hesistate to contact me!!

