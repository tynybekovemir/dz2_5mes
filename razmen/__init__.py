# core/__init__.py
from __future__ import absolute_import, unicode_literals

# Это обязательно, чтобы Celery работал с текущим проектом Django.
from .celery import app as celery_app

__all__ = ('celery_app',)
