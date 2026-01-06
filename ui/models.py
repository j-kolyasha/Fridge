def create_filter(field: str, value: str|int) -> dict:
    filter = {
        "field": field,
        "value": value
    }

    return filter
