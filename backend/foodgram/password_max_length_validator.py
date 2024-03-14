from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _, ngettext

__under__ = _


class MaximumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, max_length=150):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    """Введённый пароль слишком длинный.
Он должен содержать не более %(max_length)d символов""",
                    """Введённый пароль слишком длинный.
Он должен содержать не более %(max_length)d символов""",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            """Введённый пароль слишком длинный.
Он должен содержать не более %(max_length)d символов""",
            """Введённый пароль слишком длинный.
Он должен содержать не более %(max_length)d символов""",
            self.max_length
        ) % {'max_length': self.max_length}
