## Business Problem
This is the development of final project for the course mlops-zoomcamp from [DataTalksClub](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project).
The project provides the online service for the prediction of customers intention to buy a car. The dataset has been downloaded from kaggle. 
The aim of the project is to make a production service with experiment tracking, pipeline automation, observability and we are not focussed towards accuracy of the model.
## Dataset
The dataset is available from [kaggle House Rent Prediction Dataset
](https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset).

**Dataset Glossary (Column-Wise):**
- BHK: Number of Bedrooms, Hall, Kitchen.
- Rent: Rent of the Houses/Apartments/Flats.
- Size: Size of the Houses/Apartments/Flats in Square Feet.
- Floor: Houses/Apartments/Flats situated in which Floor and Total Number of Floors (Example: Ground out of 2, 3 out of 5, etc.)
- Area Type: Size of the Houses/Apartments/Flats calculated on either Super Area or Carpet Area or Build Area.
- Area Locality: Locality of the Houses/Apartments/Flats.
- City: City where the Houses/Apartments/Flats are Located.
- Furnishing Status: Furnishing Status of the Houses/Apartments/Flats, either it is Furnished or Semi-Furnished or Unfurnished.
- Tenant Preferred: Type of Tenant Preferred by the Owner or Agent.
- Bathroom: Number of Bathrooms.
- Point of Contact: Whom should you contact for more information regarding the Houses/Apartments/Flats.

## Trained Model

- It has been released as github release and available in https://github.com/amitkml/mlops-zoomcamp-learning/releases/tag/v0.1.0-alpha-home-rent

## High Level Solution
The project is implemented on Ubuntu 22.04 on Amazon AWS. The described steps for reproducbility are based on specific AWS configuration. This repository has 2 folders: src and data. The folder data contains the whole dataset for the given service. In the folder src the main source code is provided with various configuration files for docker and existing databases.

## References
- https://www.codeac.io/documentation/pylint-configuration.html

