# Battery-Pack-Diagnostics-for-Electric-Vehicles

Derive curves for cell and vehicle level differential voltage analysis (DVA) and incremental capacity analyis (ICA) in python.

## Associated Article
Please also check the associated article available online published in the Journal of eTransportation (Elsevier):

[Battery pack diagnostics for electric vehicles: Transfer of differential voltage and incremental capacity analysis from cell to vehicle level](https://www.sciencedirect.com/science/article/pii/S2590116824000468)
 
## Features
* Calculation of DVA and ICA from timeseries data
* Availabilty of cell and vehicle data
* Filtering methods
* Visualization tools (pOCV, DVA, ICA & bode diagrams)
* Notebooks for displaying data in Latex format

## Project Structure
    ├── data           <- must be created by user, download files from mediatum (link below)
    │   ├── figures    <- Generated figures are saved in this folder
    │   │
    │   ├── font    <- fonts for the figures (STIX)
    │   │
    │   ├── Tesla    <- cell and vehicle data
    │   │
    │   └── VW       <- cell, halfcell and vehicle data (+raw vehicle data)
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the category, and a short description 
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to load and prepare data for further processing
    │   │   
    │   ├── filtering       <- Filtering methods to reduce the noise in DVA/ICA
    │   │
    |   ├── utils       <- Utils for calculating bode plots
    │   │
    │   ├── visualization  <- Scripts to create visualizations
    │   │    
    │   └── voltage_capacity_analysis <- Scripts to extract the DVA/ICA from timeseries data
    │
    ├── .gitignore
    │
    ├── LICENSE
    │
    ├── README.md
    │	
    └── requirements.txt

## Requirements

The following requirements are to be met:
* python 3.11.9


## Installation

1. clone repo into directory
```console
git clone https://github.com/TUMFTM/Battery-Pack-Diagnostics-for-Electric-Vehicles.git
```  
2. install libraries via the requirements.txt
```console
pip install -r requirements.txt
```  
3. download data from mediaTUM and place into data folder:
```url
https://mediatum.ub.tum.de/1737452
```

## Contributing and Support

For contributing to the code please contact:  

[Philip Bilfinger](mailto:philip.bilfinger@tum.de)<br/>
**[Institute of Automotive Technology](https://www.mos.ed.tum.de/en/ftm/home/)**<br/>
**[Technical University of Munich, Germany](https://www.tum.de/en/)**

## Versioning

V0.1 

## Authors

Philip Bilfigner

## License
 
We are very happy if you choose this code for your projects and provide all updates under GNU LESSER GENERAL PUBLIC LICENSE Version 3 (29 June 2007). Please refer to the license file for any further questions about incorporating these scripts into your projects.
We are looking forward to hearing your feedback and kindly ask you to share bugfixes, improvements and updates on the files provided.

## BibTex entry

@article{Bilfinger2024, <br />
  title = {Battery pack diagnostics for electric vehicles: Transfer of differential voltage and incremental capacity analysis from cell to vehicle level},<br />
  ISSN = {2590-1168},<br />
  url = {http://dx.doi.org/10.1016/j.etran.2024.100356 },<br />
  DOI = {10.1016/j.etran.2024.100356},<br />
  journal = {eTransportation},<br />
  publisher = {Elsevier BV},<br />
  author = {Bilfinger,  Philip and Rosner,  Philipp and Schreiber,  Markus and Kr\"{o}ger,  Thomas and Gamra,  Kareem Abo and Ank,  Manuel and Wassiliadis,  Nikolaos and Dietermann,  Brian and Lienkamp,  Markus},<br />
  year = {2024}<br />
}
