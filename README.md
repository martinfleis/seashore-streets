# Paper title HERE
Repository of data and code for paper NAME TBD.


Paper reference HERE

Date: 27/03/2020

Contact: martin@martinfleischmann.net

## Introduction
This repository contains python code in the form of Jupyter notebooks and geospatial data used in the above-mentioned research paper.

The official archived version of this repository can be found at XXX and should be referenced as XX. However, primarily refer to the original paper.

Geospatial data represent morphological structure of 30 seashore streets along the Portuguese coast. The data were analyzed using computational Jupyter notebooks to determine their morphometric profile, morphological classification and asses the risk of flooding due to the extreme weather events caused by climate change.

Building layers were manually digitized and, where available, enriched by OpenStreetMap data. Street network layer was extracted from OpenStreetMap. Other layers were generated using Jupyter notebooks.

### Data structure:

GeoPackages containing geospatial data are divided according to geographical locations.

Structure of repository:

```
./*.ipynb
    - Juptyter notebooks used for the analysis. Uses datasets in data folder.
./*.pdf, *.html, *.py
    - alternative formats mirroring the content of Jupyter notebooks
./environment.yml
    - conda environment specification to re-create reproducible Python environment
./LICENSE
    - license for software in the root folder
./data
    atlantic.gpkg
        name_blg    - Polygon layers
        name_str    - LineString layers
        name_case   - Polygon layers
        name_tess   - Polygon layers
        name_blocks - Polygon layers
        ...
     preatl.gpkg
        name_blg
        name_str
        name_case
        ...
     premed.gpkg
        name_blg
        name_str
        name_case
        ...
     med.gpkg
        name_blg
        name_str
        name_case
        ...
    summative_data.csv
        - CSV containing contextual (summative) morphometric profiles of each case study.
    summative_data_norm.csv
        - normalized version of summative_data.csv
    waterrelation_data.csv
        - CSV containing flood risk data for each case study.
    wind_relation.csv
        - CSV containing data of seashore street orientation regarding SW wind for each case study.
    LICENSE
        - license for data in the data folder

```

## Licensing
Software in this repository is license under [Creative Commons Zero v1.0 Universal](LICENSE). The geospatial datasets are licensed under [Open Database License](data/LICENSE).
