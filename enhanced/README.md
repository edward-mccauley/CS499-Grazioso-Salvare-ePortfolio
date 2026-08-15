# Enhanced CS-340 Grazioso Salvare Dashboard

## Artifact Description

This project is an enhanced version of my CS-340 Grazioso Salvare Dashboard. The original artifact was created for CS-340: Advanced Programming Concepts. The dashboard uses Python and MongoDB to display animal shelter data and support rescue-animal selection.

For CS 499 Milestone Two, this enhancement focuses on Category One: Software Design and Engineering.

## Original Design

The original artifact included two main files:

- `ProjectTwoDashboard.ipynb`
- `CRUD_Python_Module.py`

The dashboard notebook handled several responsibilities, including dashboard layout, user interaction, filtering behavior, display updates, and calls to the database module. The CRUD module handled the MongoDB connection and basic create, read, update, and delete operations.

This structure worked for the original course project, but it could be improved from a software engineering perspective because several responsibilities were closely connected.

## Enhancement One: Software Design and Engineering

For this milestone, I enhanced the software design by separating the application into clearer components. The goal was not to rebuild the entire project from scratch, but to refactor the original artifact into a more maintainable, layered structure.

The enhanced structure includes:

- `app.py`: Application entry point
- `animal_shelter.py`: MongoDB database access layer
- `config.py`: Database configuration values
- `rescue_filter_service.py`: Rescue criteria and query-building logic
- `dashboard_controller.py`: Coordination layer between the dashboard, filters, and database
- `requirements.txt`: Python package requirements

## Enhanced Design Structure

The enhanced project separates responsibilities more clearly:

```text
app.py
    Starts the enhanced application structure.

dashboard_controller.py
    Coordinates between the dashboard, rescue filter service, and database layer.

rescue_filter_service.py
    Stores rescue criteria and builds MongoDB query filters.

animal_shelter.py
    Handles MongoDB database access and CRUD operations.

config.py
    Stores database configuration values and supports environment variables.

```

## Enhancement Two: Algorithms and Data Structures

For CS 499 Milestone Three, I enhanced the artifact by adding a rescue-animal matching and ranking algorithm.

The original dashboard used basic filtering to return records that matched selected rescue criteria. The enhanced version improves this by assigning a match score to each animal record and sorting the strongest candidates first.

The algorithm uses:

- dictionaries to store rescue profiles and scoring weights
- lists to store animal records and ranked results
- conditional logic to compare animal traits against rescue criteria
- helper methods to normalize text and validate age values
- scoring to measure match strength
- sorting to display strongest matches first

The enhanced algorithm evaluates each animal using breed, sex, and age criteria. Each matching trait adds points to the animal's match score. Animals that meet the minimum score are included in the ranked result list.

This enhancement supports Course Outcome 3 because it demonstrates algorithmic design, data structure selection, scoring logic, sorting, validation, and trade-off reasoning.

## Algorithm Review Mode

Because the original MongoDB environment may not always be running locally, the enhanced project includes `sample_animals.py`. These sample records use the same field names as the original CS-340 `aac.animals` MongoDB collection.

To review the algorithm without MongoDB:

```bash
cd enhanced
python app.py

```
## Enhancement Three: Databases

For CS 499 Milestone Four, I enhanced the database portion of the artifact by improving how the application builds, validates, and controls MongoDB database operations.

The original artifact used a CRUD module to connect to MongoDB and retrieve animal records. The enhanced version adds a database query service that validates requested fields, builds safer MongoDB query objects, creates projections, caps result limits, and prepares safer update values.

The database enhancement includes:

- `database_query_service.py` for database validation and query construction
- allowed filter fields to reduce unsafe or unexpected query behavior
- allowed update fields to control which fields can be changed
- allowed projection fields to limit returned data
- result limits to prevent overly large database reads
- safer update and delete handling
- controlled error handling in the database access class

This enhancement supports Course Outcome 4 by demonstrating practical database and software engineering techniques. It also supports Course Outcome 5 by applying a security mindset to database access, validation, and data exposure control.

## Database Review Mode

The enhanced project can demonstrate the database validation logic without requiring MongoDB to be running locally.

To review the database enhancement:

```bash
cd enhanced
python app.py

```
