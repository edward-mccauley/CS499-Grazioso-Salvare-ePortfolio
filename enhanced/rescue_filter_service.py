"""
Rescue filter service for the enhanced CS-340 Grazioso Salvare Dashboard.

This module separates rescue criteria from the dashboard interface and adds
algorithmic matching and ranking. The ranking system uses dictionaries, lists,
conditional logic, scoring, and sorting to identify the strongest rescue-animal
candidates.
"""


class RescueFilterService:
    """Builds rescue queries and ranks animals based on rescue criteria."""

    RESET = "Reset"
    WATER_RESCUE = "Water Rescue"
    MOUNTAIN_RESCUE = "Mountain or Wilderness Rescue"
    DISASTER_RESCUE = "Disaster or Individual Tracking"

    def __init__(self):
        """Initialize supported rescue profiles and scoring rules."""
        self.rescue_profiles = {
            self.WATER_RESCUE: {
                "preferred_breeds": [
                    "Labrador Retriever Mix",
                    "Chesapeake Bay Retriever",
                    "Newfoundland",
                ],
                "preferred_sex": "Intact Female",
                "age_range_weeks": (26, 156),
                "minimum_score": 70,
                "weights": {
                    "breed": 40,
                    "sex": 30,
                    "age": 30,
                },
            },
            self.MOUNTAIN_RESCUE: {
                "preferred_breeds": [
                    "German Shepherd",
                    "Alaskan Malamute",
                    "Old English Sheepdog",
                    "Siberian Husky",
                    "Rottweiler",
                ],
                "preferred_sex": "Intact Male",
                "age_range_weeks": (26, 156),
                "minimum_score": 70,
                "weights": {
                    "breed": 40,
                    "sex": 30,
                    "age": 30,
                },
            },
            self.DISASTER_RESCUE: {
                "preferred_breeds": [
                    "Doberman Pinscher",
                    "German Shepherd",
                    "Golden Retriever",
                    "Bloodhound",
                    "Rottweiler",
                ],
                "preferred_sex": "Intact Male",
                "age_range_weeks": (20, 300),
                "minimum_score": 70,
                "weights": {
                    "breed": 40,
                    "sex": 30,
                    "age": 30,
                },
            },
        }

    def get_supported_rescue_types(self):
        """Return a list of rescue type options for the dashboard."""
        return [self.RESET] + list(self.rescue_profiles.keys())

    def build_query(self, rescue_type):
        """
        Build a MongoDB query for the selected rescue type.

        This method is kept for database compatibility. The ranking methods
        provide the deeper Milestone Three algorithmic enhancement.

        Args:
            rescue_type (str): Rescue category selected by the user.

        Returns:
            dict: MongoDB query criteria.
        """
        if rescue_type == self.RESET or rescue_type is None:
            return {}

        profile = self.rescue_profiles.get(rescue_type)

        if profile is None:
            return {}

        min_age, max_age = profile["age_range_weeks"]

        return {
            "breed": {"$in": profile["preferred_breeds"]},
            "sex_upon_outcome": profile["preferred_sex"],
            "age_upon_outcome_in_weeks": {"$gte": min_age, "$lte": max_age},
        }

    def score_animal(self, animal, rescue_type):
        """
        Score one animal record against the selected rescue criteria.

        Args:
            animal (dict): Animal record from the shelter data.
            rescue_type (str): Selected rescue category.

        Returns:
            dict: Scored animal result with match score and matched traits.
        """
        profile = self.rescue_profiles.get(rescue_type)

        if profile is None or not isinstance(animal, dict):
            return {
                "animal": animal,
                "match_score": 0,
                "matched_traits": [],
            }

        score = 0
        matched_traits = []

        breed = animal.get("breed", "")
        sex = animal.get("sex_upon_outcome", "")
        age = animal.get("age_upon_outcome_in_weeks")

        weights = profile["weights"]

        if self._breed_matches(breed, profile["preferred_breeds"]):
            score += weights["breed"]
            matched_traits.append("breed")

        if sex == profile["preferred_sex"]:
            score += weights["sex"]
            matched_traits.append("sex")

        if self._age_matches(age, profile["age_range_weeks"]):
            score += weights["age"]
            matched_traits.append("age")

        return {
            "animal": animal,
            "match_score": score,
            "matched_traits": matched_traits,
        }

    def rank_animals(self, animals, rescue_type):
        """
        Rank animal records from strongest match to weakest match.

        Args:
            animals (list): Animal records to evaluate.
            rescue_type (str): Selected rescue category.

        Returns:
            list: Ranked animal records with match scores.
        """
        if not isinstance(animals, list):
            return []

        if rescue_type == self.RESET or rescue_type is None:
            return [
                {
                    **animal,
                    "match_score": 0,
                    "matched_traits": [],
                }
                for animal in animals
                if isinstance(animal, dict)
            ]

        profile = self.rescue_profiles.get(rescue_type)

        if profile is None:
            return []

        ranked_animals = []

        for animal in animals:
            scored_result = self.score_animal(animal, rescue_type)

            if scored_result["match_score"] >= profile["minimum_score"]:
                ranked_animals.append(
                    {
                        **scored_result["animal"],
                        "match_score": scored_result["match_score"],
                        "matched_traits": scored_result["matched_traits"],
                    }
                )

        return sorted(
            ranked_animals,
            key=lambda animal: (
                -animal["match_score"],
                str(animal.get("name", "")),
            ),
        )

    def _breed_matches(self, breed, preferred_breeds):
        """Return True when the animal breed matches a preferred breed."""
        normalized_breed = self._normalize_text(breed)

        for preferred_breed in preferred_breeds:
            normalized_preferred = self._normalize_text(preferred_breed)

            if normalized_breed == normalized_preferred:
                return True

            if normalized_preferred.replace(" mix", "") in normalized_breed:
                return True

        return False

    def _age_matches(self, age, age_range):
        """Return True when the animal age is inside the preferred range."""
        try:
            age_value = float(age)
        except (TypeError, ValueError):
            return False

        min_age, max_age = age_range
        return min_age <= age_value <= max_age

    def _normalize_text(self, value):
        """Normalize text values for safer comparison."""
        return str(value).strip().lower()