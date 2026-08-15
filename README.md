# CS 499 Grazioso Salvare Dashboard Enhancements

This repository contains a sanitized ePortfolio version of my Grazioso Salvare Dashboard artifact for CS 499 Computer Science Capstone.

The original project used Python and MongoDB to display animal shelter data and support rescue-animal selection through a dashboard application. The enhanced version improves the artifact in software design and engineering, algorithms and data structures, and databases.

## ePortfolio

The full ePortfolio is published through GitHub Pages:

[View My CS 499 ePortfolio](https://edward-mccauley.github.io)

## Repository Structure

```text
original/
  ProjectTwoDashboard.ipynb
  CRUD_Python_Module_redacted.py

enhanced/
  app.py
  animal_shelter.py
  config.py
  dashboard_controller.py
  database_query_service.py
  rescue_filter_service.py
  sample_animals.py
  requirements.txt
  README.md

.env.example
.gitignore
README.md
```

## Enhancement One: Software Design and Engineering

Enhancement One refactored the original dashboard into a more maintainable layered structure. The enhanced version separates responsibilities into clearer components:

* `app.py`: application entry point
* `animal_shelter.py`: MongoDB database access layer
* `config.py`: environment-based configuration
* `rescue_filter_service.py`: rescue criteria and filtering logic
* `dashboard_controller.py`: coordination layer

This enhancement demonstrates modular design, separation of concerns, class-based organization, configuration management, documentation, and maintainability.

## Enhancement Two: Algorithms and Data Structures

Enhancement Two improves the rescue-animal selection process by adding matching, scoring, and ranking logic.

The enhanced version uses:

* Dictionaries to organize rescue criteria
* Lists to process animal records
* Conditional logic to evaluate matches
* Scoring rules to assign candidate scores
* Sorting to rank stronger rescue candidates first

This enhancement changes the selection process from basic filtering into a more useful decision-support feature.

## Enhancement Three: Databases

Enhancement Three improves the MongoDB database access layer by adding safer query construction and validation.

The enhanced version includes:

* A dedicated `database_query_service.py` module
* Allowed filter fields
* Allowed update fields
* Allowed MongoDB operators
* Projection support
* Result limit validation
* Safer update handling
* Controlled database error handling
* Environment-based configuration

This enhancement supports safer and more maintainable database interaction.

## Security and Configuration

This public repository does not include real database credentials.

Database configuration values should be supplied through environment variables. The `.env.example` file documents the expected configuration format:

```text
AAC_DB_HOST=localhost
AAC_DB_PORT=27017
AAC_DB_NAME=aac
AAC_DB_COLLECTION=animals
AAC_DB_USERNAME=your_username_here
AAC_DB_PASSWORD=your_password_here
```

The enhanced source code uses environment-based configuration instead of hard-coded credentials.

## Requirements

The enhanced artifact uses Python and the dependencies listed in `enhanced/requirements.txt`.

A live MongoDB database is not required to run the included review-mode demonstration.

## Running the Enhanced Artifact

The enhanced project includes review-mode output that can be run without a live MongoDB database.

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r enhanced/requirements.txt
cd enhanced
python app.py
```

Expected review-mode output includes:

* Available rescue options
* Ranked sample results for Water Rescue
* Safe database query example
* Safe projection example
* Safe result limit example

## Notes for Reviewers

The `original/` folder contains the original dashboard notebook and a redacted version of the original CRUD module for comparison. The `enhanced/` folder contains the refactored and improved version of the artifact.

This repository is intended to support the CS 499 ePortfolio and demonstrate growth in software design, algorithms and data structures, and database development.
