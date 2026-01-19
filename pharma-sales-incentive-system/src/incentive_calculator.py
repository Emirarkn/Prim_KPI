"""
Pharma Sales Incentive System - Prim Hesaplama Modülü
Ağırlıklı KPI bazlı prim hesaplama motoru
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KPIWeight:
    """KPI ağırlık tanımı"""
    name: str
    weight: float
    min_threshold: float = 0.85
    max_threshold: float = 1.65


@dataclass 
class ProductGroupWeight:
    """Ürün grubu ağırlık tanımı"""
    group_name: str
    products: List[str]
    weight: float


@dataclass
class STScore:
    """ST skoru"""
    st_name: str
    bm_name: str
    region: str
    kpi_scores: Dict[str, float] = field(default_factory=dict)
    product_scores: Dict[str, float] = field(default_factory=dict)
    total_score: float = 0.0
    eligible_for_bonus: bool = False


class IncentiveCalculator:
    """Prim hesaplama sınıfı"""
    
    def __init__(self):
        # Varsayılan KPI ağırlıkları
        self.kpi_weights = {
            'sales_volume': KPIWeight('Satış Hacmi', 60.0),
            'distribution': KPIWeight('Dağılım', 15.0),
            'route_compliance': KPIWeight('Rota Uyumu', 15.0),
            'order_success': KPIWeight('Sipariş Başarısı', 10.0),
        }
        
        # Varsayılan ürün grubu ağırlıkları
        self.product_weights: Dict[str, ProductGroupWeight] = {}
        
        # Prim eşiği
        self.bonus_threshold = 85.0
        
        # Min/Max eşikler
        self.min_threshold = 0.85
        self.max_threshold = 1.65
    
    def load_scorecard(self, scorecard_df: pd.DataFrame):
        """Scorecard'dan ürün ağırlıklarını yükle"""
        try:
            # Scorecard yapısını analiz et
            for idx, row in scorecard_df.iterrows():
                if pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]):
                    group_name = str(row.iloc[0]).strip()
                    weight = float(row.iloc[1]) if pd.notna(row.iloc[1]) else 0
                    
                    if weight > 0:
                        self.product_weights[group_name] = ProductGroupWeight(
                            group_name=group_name,
                            products=[],
                            weight=weight
                        )
            
            logger.info(f"{len(self.product_weights)} ürün grubu yüklendi")
            
        except Exception as e:
            logger.error(f"Scorecard yüklenirken hata: {e}")
    
    def calculate_achievement_rate(self, actual: float, target: float) -> float:
        """Gerçekleşme oranını hesapla"""
        if target <= 0:
            return 0.0
        return actual / target
    
    def calculate_score(self, rate: float, weight: float) -> float:
        """Oran ve ağırlıktan puan hesapla"""
        if rate < self.min_threshold:
            return 0.0
        elif rate > self.max_threshold:
            return weight * self.max_threshold
        else:
            return weight * rate
    
    def calculate_st_sales_score(
        self,
        target_df: pd.DataFrame,
        actual_df: pd.DataFrame,
        st_name: str,
        months: List[int]
    ) -> Dict[str, Dict[str, float]]:
        """ST satış skorunu hesapla"""
        scores = {}
        
        # ST'nin hedeflerini filtrele
        st_targets = target_df[
            (target_df['Mumessil'] == st_name) & 
            (target_df['Ay'].isin(months))
        ]
        
        # Ürün grubu bazında hesapla
        for product in st_targets['Urun'].unique():
            target_sum = st_targets[st_targets['Urun'] == product]['Hedef'].sum()
            
            # Gerçekleşen değeri bul
            actual_sum = 0
            if actual_df is not None and len(actual_df) > 0:
                # Brick bazlı eşleştirme gerekebilir
                st_bricks = st_targets[st_targets['Urun'] == product]['Brick'].unique()
                actual_filtered = actual_df[
                    (actual_df['Urun'] == product) &
                    (actual_df['Brick'].isin(st_bricks))
                ]
                if 'Adet' in actual_filtered.columns:
                    actual_sum = actual_filtered['Adet'].sum()
                elif 'Anamal KUTU' in actual_filtered.columns:
                    actual_sum = actual_filtered['Anamal KUTU'].sum()
            
            rate = self.calculate_achievement_rate(actual_sum, target_sum)
            
            # Ürün ağırlığını bul
            weight = self.product_weights.get(product, ProductGroupWeight(product, [], 10)).weight
            score = self.calculate_score(rate, weight)
            
            scores[product] = {
                'target': target_sum,
                'actual': actual_sum,
                'rate': rate,
                'weight': weight,
                'score': score,
            }
        
        return scores
    
    def calculate_route_compliance(
        self,
        visit_df: pd.DataFrame,
        st_name: str,
        months: List[int]
    ) -> Dict[str, float]:
        """Rota uyum skorunu hesapla"""
        if visit_df is None or len(visit_df) == 0:
            return {'planned': 0, 'actual': 0, 'rate': 0, 'score': 0}
        
        # ST ziyaretlerini filtrele
        st_visits = visit_df[visit_df['ST'] == st_name]
        
        if 'Tarih' in st_visits.columns:
            st_visits = st_visits[st_visits['Tarih'].dt.month.isin(months)]
        
        planned = len(st_visits)
        actual = len(st_visits[st_visits.get('Gerceklesti', True) == True])
        
        rate = actual / planned if planned > 0 else 0
        weight = self.kpi_weights['route_compliance'].weight
        score = self.calculate_score(rate, weight)
        
        return {
            'planned': planned,
            'actual': actual,
            'rate': rate,
            'score': score,
        }
    
    def calculate_order_success(
        self,
        order_df: pd.DataFrame,
        st_name: str,
        months: List[int]
    ) -> Dict[str, float]:
        """Sipariş başarı skorunu hesapla"""
        if order_df is None or len(order_df) == 0:
            return {'target': 0, 'actual': 0, 'rate': 0, 'score': 0}
        
        # Basit hesaplama
        target_orders = 100  # Varsayılan hedef
        actual_orders = len(order_df)
        
        rate = actual_orders / target_orders if target_orders > 0 else 0
        weight = self.kpi_weights['order_success'].weight
        score = self.calculate_score(rate, weight)
        
        return {
            'target': target_orders,
            'actual': actual_orders,
            'rate': rate,
            'score': score,
        }
    
    def calculate_st_total_score(
        self,
        target_df: pd.DataFrame,
        actual_df: pd.DataFrame,
        visit_df: pd.DataFrame,
        order_df: pd.DataFrame,
        st_name: str,
        bm_name: str,
        region: str,
        months: List[int]
    ) -> STScore:
        """ST toplam skorunu hesapla"""
        
        st_score = STScore(
            st_name=st_name,
            bm_name=bm_name,
            region=region,
        )
        
        # Satış skorları
        sales_scores = self.calculate_st_sales_score(
            target_df, actual_df, st_name, months
        )
        st_score.product_scores = sales_scores
        
        # KPI skorları
        sales_total = sum(s['score'] for s in sales_scores.values())
        st_score.kpi_scores['sales_volume'] = sales_total
        
        route = self.calculate_route_compliance(visit_df, st_name, months)
        st_score.kpi_scores['route_compliance'] = route['score']
        
        order = self.calculate_order_success(order_df, st_name, months)
        st_score.kpi_scores['order_success'] = order['score']
        
        # Toplam skor
        st_score.total_score = sum(st_score.kpi_scores.values())
        
        # Prim hakkı
        st_score.eligible_for_bonus = st_score.total_score >= self.bonus_threshold
        
        return st_score
    
    def calculate_all_st_scores(
        self,
        target_df: pd.DataFrame,
        actual_df: pd.DataFrame,
        visit_df: pd.DataFrame,
        order_df: pd.DataFrame,
        st_bm_mapping: Dict[str, str],
        st_region_mapping: Dict[str, str],
        quarter: int
    ) -> List[STScore]:
        """Tüm ST skorlarını hesapla"""
        
        quarter_months = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
        }
        
        months = quarter_months.get(quarter, [])
        scores = []
        
        # Tüm ST'leri al
        all_st = target_df['Mumessil'].dropna().unique()
        
        for st_name in all_st:
            bm_name = st_bm_mapping.get(st_name, "Bilinmiyor")
            region = st_region_mapping.get(st_name, "Bilinmiyor")
            
            st_score = self.calculate_st_total_score(
                target_df, actual_df, visit_df, order_df,
                st_name, bm_name, region, months
            )
            scores.append(st_score)
        
        return scores
    
    def calculate_bm_score(self, st_scores: List[STScore], bm_name: str) -> Dict[str, Any]:
        """BM skorunu hesapla (ST ortalaması)"""
        bm_st_scores = [s for s in st_scores if s.bm_name == bm_name]
        
        if not bm_st_scores:
            return {'bm_name': bm_name, 'avg_score': 0, 'st_count': 0}
        
        avg_score = sum(s.total_score for s in bm_st_scores) / len(bm_st_scores)
        eligible_count = sum(1 for s in bm_st_scores if s.eligible_for_bonus)
        
        return {
            'bm_name': bm_name,
            'avg_score': avg_score,
            'st_count': len(bm_st_scores),
            'eligible_count': eligible_count,
            'eligible_rate': eligible_count / len(bm_st_scores) * 100,
        }
    
    def get_top_performers(self, st_scores: List[STScore], n: int = 5) -> List[STScore]:
        """En yüksek skorlu ST'leri getir"""
        return sorted(st_scores, key=lambda x: x.total_score, reverse=True)[:n]
    
    def get_bottom_performers(self, st_scores: List[STScore], n: int = 5) -> List[STScore]:
        """En düşük skorlu ST'leri getir"""
        return sorted(st_scores, key=lambda x: x.total_score)[:n]
    
    def get_summary_statistics(self, st_scores: List[STScore]) -> Dict[str, Any]:
        """Özet istatistikleri getir"""
        if not st_scores:
            return {}
        
        scores = [s.total_score for s in st_scores]
        eligible = [s for s in st_scores if s.eligible_for_bonus]
        
        return {
            'total_st': len(st_scores),
            'eligible_count': len(eligible),
            'eligible_rate': len(eligible) / len(st_scores) * 100,
            'avg_score': np.mean(scores),
            'median_score': np.median(scores),
            'min_score': min(scores),
            'max_score': max(scores),
            'std_score': np.std(scores),
        }
