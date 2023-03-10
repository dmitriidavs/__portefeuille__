__all__ = ['validators',
           'validate_env_vars', 'validate_asset_name', 'validate_asset_quantity']

from pydantic import ValidationError

from .validators import EnvVars


def validate_env_vars(env_vars: dict) -> dict:
    try:
        env_vars = EnvVars.parse_obj(env_vars)
        return env_vars.dict()
    except ValidationError as err:
        raise TypeError(err.json())


async def validate_asset_name(ticker: str) -> bool:
    """Check if ticker symbol is valid"""

    # TODO: add caching
    # TODO: add real validation xD
    if ticker == 'err':     # test
        return False
    else:
        return True


async def validate_asset_quantity(quan: str) -> bool:
    """Check if asset quantity can be converted to float"""

    try:
        float(quan)
        return True
    except ValueError:
        return False
