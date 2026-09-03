from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordPolicy:
    min_length: int = 12
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special: bool = True
