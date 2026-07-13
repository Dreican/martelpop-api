from sqlalchemy.exc import IntegrityError

from app.shared.database.constraints import USERS_EMAIL_UNIQUE


class Helper:

    @staticmethod
    def is_constraint_violation(
        error: IntegrityError,
        constraint_name: str,
    ) -> bool:
        diag = getattr(error.orig, "diag", None)

        if diag is None:
            return False

        return diag.constraint_name == constraint_name

    @staticmethod
    def is_email_unique_violation(error: IntegrityError) -> bool:
        return Helper.is_constraint_violation(error, USERS_EMAIL_UNIQUE)