from django.core.validators import BaseValidator
from .helpers import calculate_age

class AgeValidator(BaseValidator):
    message = ("Age must be at least %(limit_value)d.")
    code = "min_age"

    def compare(self, a, b):
        return calculate_age(a) < b