"""
Dashboard controller for the enhanced CS-340 Grazioso Salvare Dashboard.

The controller coordinates between the dashboard interface, rescue filter
service, and database access layer.
"""


class DashboardController:
    """Coordinates dashboard requests, filtering logic, and database access."""

    def __init__(self, shelter_database, filter_service):
        """
        Initialize the dashboard controller.

        Args:
            shelter_database: Database access object.
            filter_service: RescueFilterService object.
        """
        self.shelter_database = shelter_database
        self.filter_service = filter_service

    def get_rescue_options(self):
        """Return rescue type options for the dashboard interface."""
        return self.filter_service.get_supported_rescue_types()

    def get_animals_for_rescue_type(self, rescue_type):
        """
        Retrieve animal records for the selected rescue type.

        Args:
            rescue_type (str): Rescue category selected by the user.

        Returns:
            list: Matching animal records.
        """
        query = self.filter_service.build_query(rescue_type)
        return self.shelter_database.read(query)

    def get_ranked_animals_for_rescue_type(self, rescue_type, animals=None):
        """
        Retrieve and rank animal records for the selected rescue type.

        Args:
            rescue_type (str): Rescue category selected by the user.
            animals (list): Optional list of animal records for review/testing.

        Returns:
            list: Ranked animal records with match scores.
        """
        if animals is None:
            animals = self.shelter_database.read_animals(limit=50)

        return self.filter_service.rank_animals(animals, rescue_type)

        
