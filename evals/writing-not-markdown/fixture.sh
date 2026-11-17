#!/bin/bash
mkdir -p orderdesk
cat > orderdesk/store.py <<'PY'
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    id: int
    total: int


def revenue(orders):
    return sum(o.total for o in orders)
PY
