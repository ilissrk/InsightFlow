import pytest
import pandas as pd
import numpy as np
from app.analytics.engine import AnalyticsEngine

@pytest.fixture
def analytics_engine():
    return AnalyticsEngine()

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'value': [1, 2, 3, 4, 5, 100],  # Last value is an anomaly
        'timestamp': pd.date_range(start='2024-01-01', periods=6, freq='H')
    })

async def test_analyze(analytics_engine, sample_data):
    metrics = ['count', 'average', 'sum']
    results = await analytics_engine.analyze(sample_data['value'], metrics)
    
    assert results['count'] == 6
    assert results['average'] == pytest.approx(19.17, rel=1e-2)
    assert results['sum'] == 115

async def test_detect_anomalies(analytics_engine, sample_data):
    anomalies = await analytics_engine.detect_anomalies(sample_data, 'value')
    assert len(anomalies) == 1
    assert anomalies.iloc[0]['value'] == 100

async def test_generate_insights(analytics_engine, sample_data):
    insights = await analytics_engine.generate_insights(sample_data['value'])
    assert len(insights) > 0
    assert 'type' in insights[0]
    assert 'description' in insights[0]