def validate_not_divisible_by_seven(value):
    if (value is not None):
        if value % 7 == 0:
            raise ValidationError(
                "%(value)s is divisible by seven",
                params={"value": value},
                )


def validate_even(value):
    if (value is not None):
        if value % 2 != 0:
            raise ValidationError(
                "%(value)s is not an even number",
                params={"value": value},
                )



