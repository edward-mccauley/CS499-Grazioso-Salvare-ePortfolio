"""
Application entry point for the enhanced CS-340 Grazioso Salvare Dashboard.

This file demonstrates the layered design:
- AnimalShelter handles database access.
- RescueFilterService handles rescue filter criteria logic.
- DashboardController coordinates the database and filtering logic.
"""

from animal_shelter import AnimalShelter
from rescue_filter_service import RescueFilterService
from dashboard_controller import DashboardController
from sample_animals import SAMPLE_ANIMALS
from database_query_service import DatabaseQueryService

def create_controller():
    """Create and return the dashboard controller instance."""
    shelter_database = AnimalShelter()
    filter_service = RescueFilterService()
    return DashboardController(shelter_database, filter_service)

def show_database_review_mode():
    """Display safe database query construction without requiring MongoDB."""
    query_service = DatabaseQueryService()

    requested_filters = {
        "breed": {"$in": ["Labrador Retriever Mix", "Newfoundland"]},
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
        "unsafe_field": "This field should be ignored",
    }

    requested_projection = [
        "name",
        "breed",
        "sex_upon_outcome",
        "age_upon_outcome_in_weeks",
        "private_field",
    ]

    print()
    print("Database review mode:")
    print("Safe query:")
    print(query_service.build_safe_query(requested_filters))

    print("Safe projection:")
    print(query_service.build_projection(requested_projection))

    print("Safe limit:")
    print(query_service.validate_limit(500))
    
def main():
    """Run a simple review of the enhanced application structure."""
    controller = create_controller()

    print("Enhanced CS-340 Grazioso Salvare Dashboard")
    print("Available rescue options:")

    for option in controller.get_rescue_options():
        print(f"- {option}")

    selected_rescue_type = "Water Rescue"
    ranked_animals = controller.get_ranked_animals_for_rescue_type(
        selected_rescue_type,
        SAMPLE_ANIMALS,
    )

    print()
    print(f"Ranked sample results for {selected_rescue_type}:")

    for animal in ranked_animals:
        print(
            f"- {animal.get('name')}: "
            f"score={animal.get('match_score')}, "
            f"matched_traits={animal.get('matched_traits')}"
        )

    show_database_review_mode()

if __name__ == "__main__":
    main()
