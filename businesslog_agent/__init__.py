"""
PLATO BusinessLog Agent — Business Metrics for businesslog.ai
=============================================================
Logs KPIs, revenue, milestones to PLATO. Uses fleet_agent base.
"""

from .businesslog_agent import BusinessLogAgent

__all__ = ["BusinessLogAgent"]
__version__ = "0.2.0"
