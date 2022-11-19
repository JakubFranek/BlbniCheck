from typing import Optional


def validate_string(
    var: str,
    var_name: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
) -> str:
    if not isinstance(var_name, str):
        raise TypeError(
            f"var_name passed into validate_string() must be a string, is {type(var_name)} instead."
        )
    if not isinstance(var, str):
        raise TypeError(f"{var_name} must be a string, is {type(var)} instead.")
    else:
        length: int = len(var)
        if min_length is not None and length < min_length:
            raise ValueError(
                f"{var_name} length ({length}) must be at least {min_length} characters long."
            )
        if max_length is not None and length > max_length:
            raise ValueError(
                f"{var_name} length ({length}) can be at most {max_length} characters long."
            )

    return var
