# **Project Overview**:
The project's primary goal is to automate the data input process for a company that installs solar panels. The company previously used an Excel sheet to manually input various data points, such as rooftop size, building electricity usage, etc., for each building that wanted to install solar panels. This project aims to fetch the necessary data automatically using various APIs, given an address, and populate the inputs in the Excel sheet.

---

## **File Structure and Descriptions**:

### 1. **HTML Files**:
These files are responsible for the web interface of the application.

- **index.html**: This file contains the main interface for the application. It provides a form where users can input an address, including street name, street number, city, and postal code. Upon submission, the application fetches the relevant data and displays it on the same page.

### 2. **Python Files**:

- **app.py**: This is the main Flask application file. It sets up the Flask app, database configurations, and routes. The primary route is the index route, which renders the `index.html` template and handles the form submission. When the form is submitted, the application fetches the necessary data using the `database_utils.py` module and displays the results.

- **database.py**: This file sets up the SQLAlchemy instance, which is used for database interactions throughout the application.

- **database_utils.py**: This module contains functions for interacting with the database and external APIs. The main function, `get_or_create_address`, takes in address details, checks if the address already exists in the database, and if not, fetches the necessary data from external APIs and stores it in the database.

- **forms.py**: This module defines the `AddressForm` class, which is a Flask-WTF form used to collect address details from the user in the `index.html` template.

- **models.py**: This module defines the database models using SQLAlchemy. The database structure is hierarchical, representing the postal system's structure. The models are:
  - **District**: Represents a postal district, the highest level in the postal hierarchy.
  - **Area**: Represents a postal area within a district.
  - **Route**: Represents a postal route within an area.
  - **PostOffice**: Represents a post office within a route.
  - **Address**: Represents an individual address within a post office's jurisdiction. This model also stores additional data fetched from external APIs, such as EGID and Sonnendach ID.

### 3. **Database Structure**:
The database is structured to represent the hierarchical nature of the postal system. This structure allows for efficient querying and storage of addresses and their associated data. The hierarchy is as follows: District → Area → Route → Post Office → Address. Each level in the hierarchy has a one-to-many relationship with the level below it. For example, a district can have multiple areas, and each area can have multiple routes.

The reason for this structure is to efficiently store and retrieve different IDs for every address and postal code. Given the various ways different APIs fetch information about addresses, having a structured database ensures that the application doesn't have to look up the building ID every time, which would be inefficient.

---

## **End Goal**:
The end goal of this project is to create a tool that automates the data input process for the company's Excel sheet. Given an address, the tool will fetch the necessary data from various APIs, populate the Excel sheet's inputs, and save the fetched data in a structured database for future reference. This tool aims to eliminate the manual process of searching for data on websites and manually inputting it into the Excel sheet.
