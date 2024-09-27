from enum import IntEnum
from enum import unique


class BaseIntEnum(IntEnum):
    """
    Base class for integer enumerations with utility methods.

    Methods:
    --------
    choices() -> tuple:
        Returns (value, name) pairs for all members.
    
    has_key(key: str) -> bool:
        Checks if a key exists in member names.

    has_value(value: int) -> bool:
        Checks if a value exists in members.

    get_name() -> str:
        Returns the name of the current member.

    get_value() -> int:
        Returns the value of the current member.
    """

    @classmethod
    def choices(cls):
        """Return (value, name) pairs for all members."""
        return tuple((key.value, key.name) for key in cls)

    @classmethod
    def has_key(cls, key):
        """Check if a key exists in member names."""
        return (key in cls._member_names_)

    @classmethod
    def has_value(cls, value):
        """Check if a value exists in members."""
        return (value in cls._value2member_map_)

    def get_name(self):
        """Return the name of the current member."""
        return self.name

    def get_value(self):
        """Return the value of the current member."""
        return self.value


@unique
class UserTypes(BaseIntEnum):
    """
    Enumeration for user types.

    Members:
    --------
    ADMIN (1): Admin user type.
    RECRUITER 
	"""
    ADMIN = 1
    RECRUITER = 2
    JOB_SEEKER = 3