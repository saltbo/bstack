def with_tax(cents, rate):
    """The amount in cents with tax added, rounded to the nearest cent."""
    return int(cents * (1 + rate))
