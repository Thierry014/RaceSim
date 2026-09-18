"""Pure-Python cycling prediction engine.

This package MUST NOT import Django (no models, no settings, no ORM). It works
purely on the dataclasses defined in ``domain``. The mapping from Django models
to these dataclasses lives in ``uci.services``.
"""

from .domain import RiderStats, KeyPoint, Prediction
from .engine import PredictEngine

__all__ = ["RiderStats", "KeyPoint", "Prediction", "PredictEngine" ]