from core.models import LocationExtended


def format_location(location: LocationExtended) -> str:
    return f"""
{location}
""".strip()
