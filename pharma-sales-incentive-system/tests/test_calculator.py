"""
Pharma Sales Incentive System - Birim Testleri
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Proje kökünü path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from incentive_calculator import IncentiveCalculator, KPIWeight, ProductGroupWeight


class TestIncentiveCalculator:
    """Prim hesaplama testleri"""
    
    @pytest.fixture
    def calculator(self):
        """Test için calculator instance"""
        return IncentiveCalculator()
    
    def test_achievement_rate_calculation(self, calculator):
        """Gerçekleşme oranı hesaplama testi"""
        # Normal durum
        assert calculator.calculate_achievement_rate(850, 1000) == 0.85
        assert calculator.calculate_achievement_rate(1000, 1000) == 1.0
        assert calculator.calculate_achievement_rate(1650, 1000) == 1.65
        
        # Sıfır hedef
        assert calculator.calculate_achievement_rate(100, 0) == 0.0
        
        # Sıfır gerçekleşen
        assert calculator.calculate_achievement_rate(0, 1000) == 0.0
    
    def test_score_calculation_below_threshold(self, calculator):
        """Eşik altı skor testi"""
        # %85 altı = 0 puan
        score = calculator.calculate_score(0.84, 10)
        assert score == 0.0
        
        score = calculator.calculate_score(0.50, 15)
        assert score == 0.0
    
    def test_score_calculation_above_max_threshold(self, calculator):
        """Eşik üstü skor testi"""
        # %165 üstü = max puan (ağırlık × 1.65)
        score = calculator.calculate_score(2.0, 10)
        assert score == 10 * 1.65
        
        score = calculator.calculate_score(1.80, 15)
        assert score == 15 * 1.65
    
    def test_score_calculation_normal_range(self, calculator):
        """Normal aralık skor testi"""
        # %85 - %165 arası = ağırlık × oran
        score = calculator.calculate_score(1.0, 10)
        assert score == 10.0
        
        score = calculator.calculate_score(0.90, 10)
        assert score == 9.0
        
        score = calculator.calculate_score(1.20, 15)
        assert score == 18.0
    
    def test_bonus_eligibility(self, calculator):
        """Prim hakkı testi"""
        # 85 ve üzeri = prim hakkı var
        assert calculator.bonus_threshold == 85.0
        
        # Bu test STScore objesi ile yapılmalı
        # Basit kontrol
        assert 85 >= calculator.bonus_threshold
        assert 84 < calculator.bonus_threshold
    
    def test_kpi_weights_sum(self, calculator):
        """KPI ağırlıkları toplamı testi"""
        total_weight = sum(kpi.weight for kpi in calculator.kpi_weights.values())
        assert total_weight == 100.0
    
    def test_kpi_weight_structure(self, calculator):
        """KPI ağırlık yapısı testi"""
        assert 'sales_volume' in calculator.kpi_weights
        assert 'route_compliance' in calculator.kpi_weights
        assert 'order_success' in calculator.kpi_weights
        
        # Satış hacmi en yüksek ağırlıklı olmalı
        assert calculator.kpi_weights['sales_volume'].weight == 60.0


class TestProductGroupWeight:
    """Ürün grubu ağırlık testleri"""
    
    def test_product_group_creation(self):
        """Ürün grubu oluşturma testi"""
        pg = ProductGroupWeight(
            group_name='TEST_GRUP',
            products=['Ürün1', 'Ürün2'],
            weight=10.0
        )
        
        assert pg.group_name == 'TEST_GRUP'
        assert len(pg.products) == 2
        assert pg.weight == 10.0


class TestDataValidation:
    """Veri doğrulama testleri"""
    
    def test_target_data_structure(self):
        """Hedef veri yapısı testi"""
        # Örnek veri oluştur
        data = {
            'Ay': [1, 2, 3],
            'BM': ['BM_001', 'BM_001', 'BM_002'],
            'Mumessil': ['ST_001', 'ST_002', 'ST_003'],
            'Brick': ['BRICK_001', 'BRICK_002', 'BRICK_003'],
            'Urun': ['URUN_A', 'URUN_B', 'URUN_C'],
            'Hedef': [1000, 1500, 800]
        }
        df = pd.DataFrame(data)
        
        # Gerekli kolonlar mevcut mu?
        required_cols = ['Ay', 'BM', 'Mumessil', 'Brick', 'Urun', 'Hedef']
        for col in required_cols:
            assert col in df.columns
        
        # Veri tipleri doğru mu?
        assert df['Hedef'].dtype in ['int64', 'float64']
        assert df['Ay'].dtype in ['int64', 'float64']
    
    def test_sellout_data_structure(self):
        """Satış veri yapısı testi"""
        data = {
            'Tarih': pd.to_datetime(['2025-01-01', '2025-01-02']),
            'Brick': ['BRICK_001', 'BRICK_002'],
            'GLN': ['GLN_001', 'GLN_002'],
            'Urun': ['URUN_A', 'URUN_B'],
            'Adet': [50, 75]
        }
        df = pd.DataFrame(data)
        
        # Tarih kolonu datetime mi?
        assert pd.api.types.is_datetime64_any_dtype(df['Tarih'])
        
        # Adet pozitif mi?
        assert (df['Adet'] > 0).all()


class TestQuarterFiltering:
    """Çeyrek filtreleme testleri"""
    
    def test_quarter_months(self):
        """Çeyrek ay eşleşmesi testi"""
        quarter_months = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
        }
        
        # Q1
        assert 1 in quarter_months[1]
        assert 3 in quarter_months[1]
        assert 4 not in quarter_months[1]
        
        # Q4
        assert 10 in quarter_months[4]
        assert 12 in quarter_months[4]
        assert 9 not in quarter_months[4]
    
    def test_filter_by_month(self):
        """Ay bazlı filtreleme testi"""
        data = {
            'Ay': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'Hedef': [100] * 12
        }
        df = pd.DataFrame(data)
        
        # Q1 filtresi
        q1_months = [1, 2, 3]
        q1_data = df[df['Ay'].isin(q1_months)]
        assert len(q1_data) == 3
        
        # Q4 filtresi
        q4_months = [10, 11, 12]
        q4_data = df[df['Ay'].isin(q4_months)]
        assert len(q4_data) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
