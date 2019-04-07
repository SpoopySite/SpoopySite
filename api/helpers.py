import logging

import validators.url

log = logging.getLogger(__name__)


async def validate_url(url: str):
    a = validators.url(url)
    if not isinstance(a, validators.ValidationFailure):
        return True
    return False
