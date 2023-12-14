def assertError(condition: bool, error: Exception) -> None:
    if not condition:
        raise error