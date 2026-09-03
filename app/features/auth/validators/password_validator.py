from app.features.auth.exceptions.authentication_exceptions import PasswordPolicyError
from app.features.auth.security.password_policy import PasswordPolicy


class PasswordValidator:
    def __init__(self, policy: PasswordPolicy):
        self._policy = policy

    def validate(self, password: str) -> None:
        if len(password) < self._policy.min_length:
            raise PasswordPolicyError(f"Password must be at least {self._policy.min_length} characters long.")

        if len(password) > self._policy.max_length:
            raise PasswordPolicyError(f"Password must not exceed {self._policy.max_length} characters.")

        if self._policy.require_uppercase and not any(
            char.isupper() for char in password
        ):
            raise PasswordPolicyError("Password must contain an uppercase letter.")

        if self._policy.require_lowercase and not any(
            char.islower() for char in password
        ):
            raise PasswordPolicyError("Password must contain a lowercase letter.")

        if self._policy.require_digit and not any(
            char.isdigit() for char in password
        ):
            raise PasswordPolicyError("Password must contain a digit.")

        if self._policy.require_special and not any(
            not char.isalnum() for char in password
        ):
            raise PasswordPolicyError("Password must contain a special character.")