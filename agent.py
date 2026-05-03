#!/usr/bin/env python3
"""businesslog-agent — Business metrics and logging intelligence"""
import json, time
from typing import List, Dict

class BusinessLogAgent:
    def __init__(self, plato_url="http://147.224.38.131:8847"):
        self.plato_url = plato_url
        self.metrics: List[Dict] = []
    
    def log_metric(self, category: str, name: str, value: float, unit: str, notes: str=""):
        m = {"category": category, "name": name, "value": value, "unit": unit, "notes": notes, "time": time.time()}
        self.metrics.append(m)
        self._submit(f"{category} metric: {name}", f"{value} {unit}. {notes}")
        return m
    
    def get_dashboard(self) -> Dict:
        if not self.metrics: return {"error": "No metrics"}
        cats = {}
        for m in self.metrics:
            c = m["category"]
            if c not in cats: cats[c] = []
            cats[c].append(m)
        return {"total_metrics": len(self.metrics), "categories": list(cats.keys()), "latest": self.metrics[-1]}
    
    def get_trend(self, name: str) -> List:
        return [m for m in self.metrics if m["name"] == name]
    
    def _submit(self, q: str, a: str):
        try:
            import urllib.request
            urllib.request.urlopen(urllib.request.Request(f"{self.plato_url}/submit", data=json.dumps({"question": q, "answer": a, "agent": "businesslog-agent", "room": "businesslog"}).encode(), headers={"Content-Type": "application/json"}), timeout=5)
        except: pass

def demo():
    a = BusinessLogAgent()
    a.log_metric("revenue", "daily", 15000, "USD", "Q2 target on track")
    a.log_metric("users", "active", 4230, "count", "+12% vs last week")
    a.log_metric("revenue", "daily", 16200, "USD", "Promotion started")
    print(a.get_dashboard())
    print(a.get_trend("daily"))

if __name__ == "__main__": demo()
