"""Constants and Enums for Petlibro."""

from enum import IntEnum, StrEnum

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, UnitOfMass, UnitOfVolume

type _Unit = Unit

DOMAIN = "petlibro"

# Configuration keys
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_API_TOKEN = "api_token"
CONF_REGION = "region"

# Supported platforms
PLATFORMS = ["sensor", "switch", "button", "binary_sensor", "number", "select", "text", "update"]  # Add any other platforms as needed

# Update interval for device data in seconds
UPDATE_INTERVAL_SECONDS = 60  # You can adjust this value based on your needs


class Gender(IntEnum):
    """Gender/sex options."""

    # API value, MDI Icon, Symbol, Emoji
    NONE = 0, "mdi:gender-male-female", "\u26a5", ""
    MALE = 1, "mdi:gender-male", "\u2642", "\u2642\ufe0f"
    FEMALE = 2, "mdi:gender-female", "\u2640", "\u2640\ufe0f"

    def __new__(cls, value: int, icon: str, symbol: str, emoji: str):
        "Ensures IntEnum functionality while allowing symbols."
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._icon = icon  # noqa: SLF001
        obj._symbol = symbol  # noqa: SLF001
        obj._emoji = emoji  # noqa: SLF001
        return obj

    @property
    def lower(self) -> str:
        """Returns unit name in lower case."""
        return self.name.lower()

    @property
    def icon(self) -> str:
        """MDI icon for gender (eg. mdi:gender-male)."""
        return self._icon

    @property
    def symbol(self) -> str:
        """Symbol for gender (eg. \u26a5, \u2642, \u2640)."""
        return self._symbol

    @property
    def emoji(self) -> str:
        """Emoji for gender (eg. \u2642\ufe0f, \u2640\ufe0f)."""
        return self._emoji


class APIKey(StrEnum):
    """Common API JSON keys."""

    # Common
    ID = "id"
    NAME = "name"
    WEIGHT = "weight"

    # Member
    EMAIL = "email"
    NICKNAME = "nickname"
    GENDER = "gender"
    FEED_UNIT = "feedUnitType"
    WATER_UNIT = "waterUnitType"
    WEIGHT_UNIT = "weightUnitType"

    # Pet
    BIRTHDAY = "birthday"
    TYPE = "type"
    SEX = "gender"
    BREED_NAME = "breedName"
    BREED_ID = "breedId"
    PET_ID = "petId"


class Unit(IntEnum):
    """Weight, feed, and water units with symbols and conversion."""

    CUPS = 1, "cup", 1/12,
    OUNCES = 2, UnitOfMass.OUNCES, 0.35,
    GRAMS = 3, UnitOfMass.GRAMS, 10,
    MILLILITERS = 4, UnitOfVolume.MILLILITERS, 20,

    KILOGRAMS = 5, UnitOfMass.KILOGRAMS, 1,
    POUNDS = 6, UnitOfMass.POUNDS, 2.20459,

    WATER_OUNCES = 2, UnitOfVolume.FLUID_OUNCES, 0.035195,
    WATER_MILLILITERS = 4, UnitOfVolume.MILLILITERS, 1,

    def __new__(cls, value: int, symbol: str, factor: float):
        "Ensures IntEnum functionality while allowing extra attributes."
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._symbol = symbol  # noqa: SLF001
        obj._factor = factor  # noqa: SLF001
        return obj

    @property
    def lower(self) -> str:
        """Returns unit name in lower case."""
        return self.name.lower()

    @property
    def symbol(self) -> str:
        """Returns unit symbol."""
        return self._symbol

    @property
    def factor(self) -> float:
        """Returns unit conversion factor."""
        return self._factor

    @classmethod
    def round(self, value: float, unit: _Unit):
        return round(value, ROUNDING_RULES.get(unit, 0))

    @classmethod
    def convert_feed(
        self, value: float, from_unit: _Unit | None, to_unit: _Unit | None, rounded: bool = False
    ):
        """Convert PetLibro feed units. Use **None** for portion unit (1/12th of a cup)."""
        if value and from_unit != to_unit:
            if not {from_unit, to_unit}.issubset(VALID_UNIT_TYPES[APIKey.FEED_UNIT]):
                raise ValueError(f"Incompatible conversion: {from_unit} -> {to_unit}")

            from_factor = from_unit.factor if from_unit else 1
            to_factor = to_unit.factor if to_unit else 1

            api_value = value / from_factor
            new_value = api_value * to_factor
        else:
            new_value = value

        if not to_unit:
            return round(new_value)
        if rounded:
            return Unit.round(new_value, to_unit)
        return new_value
    

DEFAULT_WEIGHT = Unit.POUNDS
DEFAULT_FEED = Unit.CUPS
DEFAULT_WATER = Unit.WATER_OUNCES
VALID_UNIT_TYPES: dict[str, set[Unit]] = {
    APIKey.WEIGHT_UNIT: {Unit.POUNDS, Unit.KILOGRAMS, None},
    APIKey.FEED_UNIT: {Unit.CUPS, Unit.OUNCES, Unit.GRAMS, Unit.MILLILITERS, None},
    APIKey.WATER_UNIT: {Unit.OUNCES, Unit.MILLILITERS, Unit.WATER_OUNCES, Unit.WATER_MILLILITERS, None},
}
ROUNDING_RULES = {
    Unit.CUPS: 3, Unit.OUNCES: 2, Unit.POUNDS: 2, Unit.WATER_OUNCES: 2, Unit.KILOGRAMS: 2
}
