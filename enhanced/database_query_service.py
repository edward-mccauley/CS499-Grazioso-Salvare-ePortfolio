"""
Database query service for the enhanced CS-340 Grazioso Salvare Dashboard.

This module supports the database enhancement by validating requested fields,
building safer MongoDB query objects, creating projections, limiting result
sizes, and preparing safer update values.
"""


class DatabaseQueryService:
    """Builds safer MongoDB query, projection, update, and limit values."""

    DEFAULT_LIMIT = 50
    MAX_LIMIT = 100

    ALLOWED_FILTER_FIELDS = {
        "animal_id",
        "animal_type",
        "breed",
        "name",
        "outcome_type",
        "sex_upon_outcome",
        "age_upon_outcome_in_weeks",
    }

    ALLOWED_UPDATE_FIELDS = {
        "animal_type",
        "breed",
        "name",
        "outcome_type",
        "sex_upon_outcome",
        "age_upon_outcome_in_weeks",
    }

    ALLOWED_PROJECTION_FIELDS = {
        "animal_id",
        "animal_type",
        "breed",
        "color",
        "name",
        "outcome_type",
        "sex_upon_outcome",
        "age_upon_outcome",
        "age_upon_outcome_in_weeks",
        "location_lat",
        "location_long",
    }

    DEFAULT_PROJECTION_FIELDS = [
        "animal_id",
        "name",
        "breed",
        "sex_upon_outcome",
        "age_upon_outcome_in_weeks",
        "outcome_type",
    ]

    ALLOWED_OPERATORS = {"$eq", "$in", "$gte", "$lte"}

    def build_safe_query(self, filters=None):
        """
        Build a safer MongoDB query from requested filter values.

        Args:
            filters (dict): Requested MongoDB filter criteria.

        Returns:
            dict: Validated MongoDB query.
        """
        if filters is None:
            return {}

        if not isinstance(filters, dict):
            return {}

        safe_query = {}

        for field, value in filters.items():
            if field not in self.ALLOWED_FILTER_FIELDS:
                continue

            safe_value = self._sanitize_query_value(value)

            if safe_value is not None:
                safe_query[field] = safe_value

        return safe_query

    def build_projection(self, fields=None):
        """
        Build a MongoDB projection using only allowed fields.

        Args:
            fields (list): Requested fields to return.

        Returns:
            dict: MongoDB projection.
        """
        if fields is None:
            fields = self.DEFAULT_PROJECTION_FIELDS

        if not isinstance(fields, list):
            fields = self.DEFAULT_PROJECTION_FIELDS

        allowed_fields = [
            field for field in fields
            if field in self.ALLOWED_PROJECTION_FIELDS
        ]

        if not allowed_fields:
            allowed_fields = self.DEFAULT_PROJECTION_FIELDS

        projection = {field: 1 for field in allowed_fields}
        projection["_id"] = 0

        return projection

    def build_safe_update(self, updates=None):
        """
        Build a safer update document using only allowed update fields.

        Args:
            updates (dict): Requested field updates.

        Returns:
            dict: Validated update values.
        """
        if updates is None or not isinstance(updates, dict):
            return {}

        safe_updates = {}

        for field, value in updates.items():
            if field not in self.ALLOWED_UPDATE_FIELDS:
                continue

            safe_value = self._sanitize_scalar(value)

            if safe_value is not None:
                safe_updates[field] = safe_value

        return safe_updates

    def validate_limit(self, limit=None):
        """
        Validate and cap the number of database records returned.

        Args:
            limit (int): Requested result limit.

        Returns:
            int: Safe result limit.
        """
        try:
            limit_value = int(limit)
        except (TypeError, ValueError):
            return self.DEFAULT_LIMIT

        if limit_value < 1:
            return self.DEFAULT_LIMIT

        return min(limit_value, self.MAX_LIMIT)

    def _sanitize_query_value(self, value):
        """Sanitize scalar values or limited MongoDB operator dictionaries."""
        if isinstance(value, dict):
            return self._sanitize_operator_dict(value)

        return self._sanitize_scalar(value)

    def _sanitize_operator_dict(self, operator_dict):
        """Allow only approved MongoDB operators and safe values."""
        safe_operator_dict = {}

        for operator, value in operator_dict.items():
            if operator not in self.ALLOWED_OPERATORS:
                continue

            if operator == "$in":
                safe_values = self._sanitize_list(value)

                if safe_values:
                    safe_operator_dict[operator] = safe_values
            else:
                safe_value = self._sanitize_scalar(value)

                if safe_value is not None:
                    safe_operator_dict[operator] = safe_value

        return safe_operator_dict if safe_operator_dict else None

    def _sanitize_list(self, values):
        """Sanitize list values used with MongoDB $in queries."""
        if not isinstance(values, list):
            return []

        safe_values = []

        for value in values[:25]:
            safe_value = self._sanitize_scalar(value)

            if safe_value is not None:
                safe_values.append(safe_value)

        return safe_values

    def _sanitize_scalar(self, value):
        """Sanitize simple values before using them in database operations."""
        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            cleaned_value = value.strip()

            if not cleaned_value:
                return None

            return cleaned_value[:100]

        return None