"""
PLATO BusinessLog Agent — Business Metrics for businesslog.ai

Business metrics, KPIs, revenue tracking, milestone logging.
Every business event logged to PLATO as a functional tile.
"""

import time
import requests
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

DEFAULT_PLATO_URL = "http://localhost:8847"
ROOM = "businesslog-ai"


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


class BusinessLogAgent:
    """
    Business metrics agent.
    
    Logs KPIs, revenue, milestones to PLATO.
    Tracks business growth over time through vessel accumulation.
    """
    
    def __init__(self, business_id: str = "default", plato_url: str = DEFAULT_PLATO_URL):
        self.business_id = business_id
        self.plato_url = plato_url.rstrip("/")
        self.room = ROOM
    
    def _write(self, metric_type: str, data: Dict[str, Any]) -> bool:
        tile = {
            "question": f"business:{metric_type}",
            "answer": str(data),
            "confidence": 0.9,
            "metadata": {
                "business_id": self.business_id,
                "metric_type": metric_type,
                "timestamp": time.time(),
                **data
            }
        }
        try:
            resp = requests.post(f"{self.plato_url}/room/{self.room}", json=tile, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def log_kpi(self, metric_name: str, value: float, unit: str, period: str = "daily") -> bool:
        """Log a KPI metric."""
        return self._write("kpi", {
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "period": period,
        })
    
    def log_revenue(self, amount: float, source: str, recurring: bool = False) -> bool:
        """Log revenue."""
        return self._write("revenue", {
            "amount": amount,
            "source": source,
            "recurring": recurring,
        })
    
    def log_milestone(self, title: str, description: str, achieved: bool = True) -> bool:
        """Log a business milestone."""
        return self._write("milestone", {
            "title": title,
            "description": description,
            "achieved": achieved,
        })
    
    def ask(self, question: str) -> str:
        """Query business metrics from PLATO."""
        try:
            resp = requests.get(f"{self.plato_url}/room/{self.room}?limit=20", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                relevant = [t for t in tiles if any(w in str(t).lower() for w in question.lower().split()[:3])]
                if relevant:
                    return f"Found {len(relevant)} business records: {relevant[-1].get('answer', '')[:200]}"
        except:
            pass
        return "Business system unavailable."
