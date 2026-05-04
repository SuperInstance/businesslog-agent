"""
PLATO BusinessLog Agent for businesslog.ai
=========================================
Business metrics, KPIs, revenue tracking, milestone logging.
Uses fleet_agent base class.
"""

import time
from typing import Optional, Dict, Any
from dataclasses import dataclass

from fleet_agent import BaseAgent


@dataclass
class BusinessMetric:
    """A business metric tile."""
    metric_name: str
    value: float
    unit: str  # "revenue" | "users" | "conversions" | "hours"
    period: str  # "daily" | "weekly" | "monthly" | "quarterly"


@dataclass
class Milestone:
    """A business milestone."""
    title: str
    description: str
    achieved: bool
    target_date: Optional[str] = None


class BusinessLogAgent(BaseAgent):
    """
    Business metrics agent.
    
    Logs KPIs, revenue, milestones to PLATO.
    Uses fleet_math for trend analysis.
    """
    
    BUSINESSLOG_ROOM = "businesslog-ai"
    
    def __init__(self, business_id: str = "default"):
        super().__init__(agent_name=f"business-{business_id}")
        self.business_id = business_id
        self.room = self.BUSINESSLOG_ROOM
    
    def log_kpi(self, metric_name: str, value: float, 
                unit: str, period: str = "daily") -> dict:
        """Log a KPI metric."""
        tile = {
            "domain": self.room,
            "agent": self.agent_name,
            "type": "kpi",
            "question": f"What is the {metric_name} ({period})?",
            "answer": f"{value} {unit}",
            "content": {
                "metric_name": metric_name,
                "value": value,
                "unit": unit,
                "period": period,
            }
        }
        return self.post_tile(tile)
    
    def log_revenue(self, amount: float, source: str, 
                   recurring: bool = False) -> dict:
        """Log revenue."""
        tile = {
            "domain": self.room,
            "agent": self.agent_name,
            "type": "revenue",
            "question": f"How much revenue from {source}?",
            "answer": f"${amount} ({'recurring' if recurring else 'one-time'})",
            "content": {
                "amount": amount,
                "source": source,
                "recurring": recurring,
            }
        }
        return self.post_tile(tile)
    
    def log_milestone(self, title: str, description: str,
                    achieved: bool = True) -> dict:
        """Log a business milestone."""
        tile = {
            "domain": self.room,
            "agent": self.agent_name,
            "type": "milestone",
            "question": f"What milestone: {title}?",
            "answer": description,
            "content": {
                "title": title,
                "description": description,
                "achieved": achieved,
            }
        }
        return self.post_tile(tile)
    
    def get_metrics(self, limit: int = 20) -> list:
        """Get recent business metrics from PLATO."""
        response = self.get_tiles(limit=limit)
        return response.get("tiles", [])
    
    def get_revenue_trend(self) -> dict:
        """Analyze revenue trend using fleet_math."""
        from fleet_agent import EmergenceDetector
        
        tiles = self.get_metrics(limit=100)
        
        coords = []
        scores = []
        
        for tile in tiles:
            content = tile.get("content", {})
            amount = content.get("amount", 0)
            if amount > 0:
                # Use timestamp as pseudo-coordinate
                ts = content.get("timestamp", 0)
                coords.append((float(ts % 1000) / 1000.0, amount / 10000.0))
                scores.append(amount)
        
        if len(coords) < 3:
            return {"trend": "insufficient_data"}
        
        detector = EmergenceDetector()
        patterns = detector.detect(coords, scores)
        
        return {"trend": patterns}
