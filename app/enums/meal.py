from enum import Enum


class MealType(str, Enum):
    STANDARD = "standard"
    VEGAN = "vegan"
    LOW_SALT = "lowSalt"
    LACTO_OVO = "lactoOvo"
