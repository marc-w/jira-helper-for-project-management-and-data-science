"""library module"""
from lib.configuration import lazy_config

# import this
config = lazy_config


class Nothing:  # pylint: disable=R0903
    """
    Stub class to create a unique data type for identifying
    a failed get.

        The problem is that reading the API returns the
        same as default (None) for .get().

        Since the API can theoretically return any
        data type, this class iis used as a placeholder

        Allows the application to differentiate between a valid None from
        the daa and a failed .get()

    :return _type_: None
    """


# import this
nothing = Nothing()
