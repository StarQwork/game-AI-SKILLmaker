# -*- coding: utf-8 -*-
"""
核心模块 - 业务逻辑层
"""

from .config import OUTPUT_DIR, DEFAULT_ROLES, MODEL_PRESETS
from .templates import ROLE_TEMPLATES, get_available_roles, get_default_roles
from .generator import generate_game_plan, generate_all, generate_single
from .api_client import call_api

__all__ = [
    'OUTPUT_DIR', 'DEFAULT_ROLES', 'MODEL_PRESETS',
    'ROLE_TEMPLATES', 'get_available_roles', 'get_default_roles',
    'generate_game_plan', 'generate_all', 'generate_single',
    'call_api'
]
