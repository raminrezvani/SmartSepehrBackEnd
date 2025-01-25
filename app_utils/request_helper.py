def get_list_from_parameter(value: str) -> list:
    return [str(d).strip() for d in value.split(',') if len(d) > 1]
