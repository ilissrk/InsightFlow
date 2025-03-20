from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
from collections import defaultdict

class InsightGenerator:
    def __init__(self):
        self.patterns: Dict[str, Dict] = {}
        self.thresholds: Dict[str, float] = {}
        self.insight_cache: Dict[str, List[Dict]] = {}
        self.metrics_history: Dict[str, List[float]] = defaultdict(list)

    async def generate_insights(self, data: Dict, context: Optional[Dict] = None) -> List[Dict]:
        """Generate insights from data"""
        try:
            insights = []
            
            # Pattern-based insights
            pattern_insights = await self._detect_patterns(data)
            insights.extend(pattern_insights)
            
            # Anomaly detection
            anomalies = await self._detect_anomalies(data)
            insights.extend(anomalies)
            
            # Trend analysis
            trends = await self._analyze_trends(data)
            insights.extend(trends)
            
            # Context-based insights
            if context:
                context_insights = await self._generate_context_insights(data, context)
                insights.extend(context_insights)
            
            return insights
        except Exception as e:
            raise Exception(f"Insight generation error: {str(e)}")

    async def _detect_patterns(self, data: Dict) -> List[Dict]:
        """Detect patterns in data"""
        try:
            detected_patterns = []
            for pattern_name, pattern in self.patterns.items():
                if self._match_pattern(data, pattern):
                    detected_patterns.append({
                        "type": "pattern",
                        "name": pattern_name,
                        "confidence": self._calculate_confidence(data, pattern),
                        "timestamp": datetime.utcnow().isoformat()
                    })
            return detected_patterns
        except Exception as e:
            raise Exception(f"Pattern detection error: {str(e)}")

    async def _detect_anomalies(self, data: Dict) -> List[Dict]:
        """Detect anomalies in data"""
        try:
            anomalies = []
            for metric, values in self.metrics_history.items():
                if metric in data:
                    current_value = data[metric]
                    if self._is_anomaly(current_value, values):
                        anomalies.append({
                            "type": "anomaly",
                            "metric": metric,
                            "value": current_value,
                            "threshold": self.thresholds.get(metric, 0),
                            "timestamp": datetime.utcnow().isoformat()
                        })
                    # Update history
                    values.append(current_value)
                    if len(values) > 1000:  # Keep last 1000 values
                        values.pop(0)
            return anomalies
        except Exception as e:
            raise Exception(f"Anomaly detection error: {str(e)}")

    async def _analyze_trends(self, data: Dict) -> List[Dict]:
        """Analyze trends in data"""
        try:
            trends = []
            for metric, values in self.metrics_history.items():
                if metric in data:
                    trend = self._calculate_trend(values)
                    if trend:
                        trends.append({
                            "type": "trend",
                            "metric": metric,
                            "direction": trend["direction"],
                            "magnitude": trend["magnitude"],
                            "timestamp": datetime.utcnow().isoformat()
                        })
            return trends
        except Exception as e:
            raise Exception(f"Trend analysis error: {str(e)}")

    async def _generate_context_insights(self, data: Dict, context: Dict) -> List[Dict]:
        """Generate context-based insights"""
        try:
            # Implement context-based insight generation
            return []
        except Exception as e:
            raise Exception(f"Context insight error: {str(e)}")

    def _match_pattern(self, data: Dict, pattern: Dict) -> bool:
        """Match data against a pattern"""
        # Implement pattern matching logic
        return False

    def _calculate_confidence(self, data: Dict, pattern: Dict) -> float:
        """Calculate confidence score for a pattern match"""
        # Implement confidence calculation logic
        return 0.0

    def _is_anomaly(self, value: float, history: List[float]) -> bool:
        """Check if a value is anomalous"""
        if not history:
            return False
        mean = sum(history) / len(history)
        std_dev = (sum((x - mean) ** 2 for x in history) / len(history)) ** 0.5
        return abs(value - mean) > (std_dev * 3)  # 3 sigma rule

    def _calculate_trend(self, values: List[float]) -> Optional[Dict]:
        """Calculate trend direction and magnitude"""
        if len(values) < 2:
            return None
            
        slope = (values[-1] - values[0]) / len(values)
        magnitude = abs(slope)
        
        if magnitude < 0.01:  # Threshold for significant trend
            return None
            
        return {
            "direction": "up" if slope > 0 else "down",
            "magnitude": magnitude
        }

    def register_pattern(self, name: str, pattern: Dict) -> None:
        """Register a new pattern"""
        self.patterns[name] = pattern

    def set_threshold(self, metric: str, threshold: float) -> None:
        """Set threshold for a metric"""
        self.thresholds[metric] = threshold