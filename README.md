# CS 499 Grazioso Salvare Dashboard Enhancements

This repository contains a sanitized ePortfolio version of my CS-340 Grazioso Salvare Dashboard artifact for CS 499.

## Artifact

The original project used Python and MongoDB to display animal shelter data and support rescue-animal selection.

## Enhancements

This repository includes enhancements in three areas:

- Software design and engineering
- Algorithms and data structures
- Databases

## Enhancement One: Software Design and Engineering

Enhancement One refactored the original dashboard project into a more maintainable layered structure.

The enhanced version separates responsibilities into clearer components:

- `app.py`: application entry point
- `animal_shelter.py`: MongoDB database access layer
- `config.py`: environment-based configuration
- `rescue_filter_service.py`: rescue criteria, filtering logic, and ranking support
- `dashboard_controller.py`: coordination layer
- `database_query_service.py`: safer database query construction and validation
- `sample_animals.py`: sample records for review mode

## Security Note

This public repository does not include real database credentials. Configuration values should be supplied through environment variables. The `.env.example` file shows the expected configuration format.

## Review Mode

The enhanced project includes review-mode output that can be run without a live MongoDB database.

```bash
cd enhanced
python app.py
```

