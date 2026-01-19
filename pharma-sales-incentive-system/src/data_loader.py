"""
Pharma Sales Incentive System - Veri Yükleme Modülü
Excel dosyalarından veri okuma ve işleme
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LoadResult:
    """Veri yükleme sonucu"""
    success: bool
    data: Optional[pd.DataFrame]
    message: str
    row_count: int = 0


class DataLoader:
    """Excel veri yükleme sınıfı"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.loaded_data: Dict[str, pd.DataFrame] = {}
        
        # Beklenen kolon yapıları
        self.expected_columns = {
            'target': ['Ay', 'BM', 'Mumessil', 'Brick', 'Urun', 'Hedef'],
            'sellout': ['Tarih', 'Brick', 'GLN', 'Urun', 'Adet'],
            'visit': ['Tarih', 'ST', 'Musteri', 'Aktivite'],
            'order': ['Tarih', 'Brick', 'GLN', 'Siparis'],
        }
    
    def load_target_file(self, file_path: str) -> LoadResult:
        """Hedef dosyasını yükle (Target25.xlsx)"""
        try:
            df = pd.read_excel(file_path, skiprows=2)
            
            # Kolon isimlerini standartlaştır
            df.columns = ['Ay', 'BM', 'Mumessil', 'Brick', 'Urun', 'Prod', 
                         'Hedef', 'Col7', 'Col8'][:len(df.columns)]
            
            # Başlık satırlarını filtrele
            df = df[df['Ay'] != 'Ay']
            
            # Veri tiplerini düzelt
            df['Ay'] = pd.to_numeric(df['Ay'], errors='coerce')
            df['Hedef'] = pd.to_numeric(df['Hedef'], errors='coerce')
            
            # NaN değerleri temizle
            df = df.dropna(subset=['Ay', 'Hedef'])
            
            self.loaded_data['target'] = df
            
            return LoadResult(
                success=True,
                data=df,
                message=f"Hedef dosyası başarıyla yüklendi",
                row_count=len(df)
            )
            
        except Exception as e:
            logger.error(f"Hedef dosyası yüklenirken hata: {e}")
            return LoadResult(
                success=False,
                data=None,
                message=f"Hata: {str(e)}"
            )
    
    def load_sellout_file(self, file_path: str) -> LoadResult:
        """Satış verisi dosyasını yükle"""
        try:
            df = pd.read_excel(file_path)
            
            # Tarih kolonunu dönüştür
            if 'Tarih' in df.columns:
                df['Tarih'] = pd.to_datetime(df['Tarih'])
                df['Ay'] = df['Tarih'].dt.month
                df['Yil'] = df['Tarih'].dt.year
            
            self.loaded_data['sellout'] = df
            
            return LoadResult(
                success=True,
                data=df,
                message=f"Satış verisi başarıyla yüklendi",
                row_count=len(df)
            )
            
        except Exception as e:
            logger.error(f"Satış dosyası yüklenirken hata: {e}")
            return LoadResult(
                success=False,
                data=None,
                message=f"Hata: {str(e)}"
            )
    
    def load_visit_file(self, file_path: str) -> LoadResult:
        """Ziyaret verisi dosyasını yükle"""
        try:
            df = pd.read_excel(file_path)
            
            if 'Tarih' in df.columns:
                df['Tarih'] = pd.to_datetime(df['Tarih'])
            
            self.loaded_data['visit'] = df
            
            return LoadResult(
                success=True,
                data=df,
                message=f"Ziyaret verisi başarıyla yüklendi",
                row_count=len(df)
            )
            
        except Exception as e:
            logger.error(f"Ziyaret dosyası yüklenirken hata: {e}")
            return LoadResult(
                success=False,
                data=None,
                message=f"Hata: {str(e)}"
            )
    
    def load_order_file(self, file_path: str) -> LoadResult:
        """Sipariş verisi dosyasını yükle"""
        try:
            df = pd.read_excel(file_path)
            
            if 'Tarih' in df.columns:
                df['Tarih'] = pd.to_datetime(df['Tarih'])
            
            self.loaded_data['order'] = df
            
            return LoadResult(
                success=True,
                data=df,
                message=f"Sipariş verisi başarıyla yüklendi",
                row_count=len(df)
            )
            
        except Exception as e:
            logger.error(f"Sipariş dosyası yüklenirken hata: {e}")
            return LoadResult(
                success=False,
                data=None,
                message=f"Hata: {str(e)}"
            )
    
    def load_master_files(self, master_dir: str) -> Dict[str, LoadResult]:
        """Master dosyaları yükle"""
        results = {}
        master_path = Path(master_dir)
        
        master_files = {
            'scorecard': 'Scorecard.xlsx',
            'brick_st': 'BrickST.xlsx',
            'st_bm': 'STBM.xlsx',
            'kriter': 'Kriter.xlsx',
            'urun_gr': 'Ürün_Gr.xlsx',
        }
        
        for key, filename in master_files.items():
            file_path = master_path / filename
            if file_path.exists():
                try:
                    df = pd.read_excel(str(file_path))
                    self.loaded_data[key] = df
                    results[key] = LoadResult(
                        success=True,
                        data=df,
                        message=f"{filename} yüklendi",
                        row_count=len(df)
                    )
                except Exception as e:
                    results[key] = LoadResult(
                        success=False,
                        data=None,
                        message=f"Hata: {str(e)}"
                    )
            else:
                results[key] = LoadResult(
                    success=False,
                    data=None,
                    message=f"Dosya bulunamadı: {filename}"
                )
        
        return results
    
    def get_unique_values(self, data_key: str, column: str) -> List[Any]:
        """Belirli bir kolonun benzersiz değerlerini getir"""
        if data_key in self.loaded_data:
            df = self.loaded_data[data_key]
            if column in df.columns:
                return df[column].dropna().unique().tolist()
        return []
    
    def get_st_list(self) -> List[str]:
        """ST listesini getir"""
        if 'target' in self.loaded_data:
            return sorted(self.loaded_data['target']['Mumessil'].dropna().unique().tolist())
        return []
    
    def get_bm_list(self) -> List[str]:
        """BM listesini getir"""
        if 'target' in self.loaded_data:
            return sorted(self.loaded_data['target']['BM'].dropna().unique().tolist())
        return []
    
    def get_product_list(self) -> List[str]:
        """Ürün listesini getir"""
        if 'target' in self.loaded_data:
            return sorted(self.loaded_data['target']['Urun'].dropna().unique().tolist())
        return []
    
    def filter_by_quarter(self, year: int, quarter: int) -> Dict[str, pd.DataFrame]:
        """Verileri çeyreğe göre filtrele"""
        quarter_months = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
        }
        
        months = quarter_months.get(quarter, [])
        filtered = {}
        
        for key, df in self.loaded_data.items():
            if 'Ay' in df.columns:
                filtered[key] = df[df['Ay'].isin(months)]
            elif 'Tarih' in df.columns:
                df_copy = df.copy()
                df_copy['Ay'] = df_copy['Tarih'].dt.month
                filtered[key] = df_copy[df_copy['Ay'].isin(months)]
            else:
                filtered[key] = df
        
        return filtered
    
    def validate_data(self) -> Dict[str, List[str]]:
        """Yüklenen verileri doğrula"""
        issues = {}
        
        # Hedef verisi kontrolleri
        if 'target' in self.loaded_data:
            target_issues = []
            df = self.loaded_data['target']
            
            if df['Hedef'].isna().sum() > 0:
                target_issues.append(f"{df['Hedef'].isna().sum()} satırda hedef değeri eksik")
            
            if df['Mumessil'].isna().sum() > 0:
                target_issues.append(f"{df['Mumessil'].isna().sum()} satırda mümessil bilgisi eksik")
            
            if target_issues:
                issues['target'] = target_issues
        
        # Satış verisi kontrolleri
        if 'sellout' in self.loaded_data:
            sellout_issues = []
            df = self.loaded_data['sellout']
            
            if 'Adet' in df.columns and df['Adet'].isna().sum() > 0:
                sellout_issues.append(f"{df['Adet'].isna().sum()} satırda adet değeri eksik")
            
            if sellout_issues:
                issues['sellout'] = sellout_issues
        
        return issues
    
    def get_summary(self) -> Dict[str, Any]:
        """Yüklenen verilerin özetini getir"""
        summary = {
            'loaded_files': list(self.loaded_data.keys()),
            'total_rows': sum(len(df) for df in self.loaded_data.values()),
        }
        
        if 'target' in self.loaded_data:
            df = self.loaded_data['target']
            summary['st_count'] = df['Mumessil'].nunique()
            summary['bm_count'] = df['BM'].nunique()
            summary['product_count'] = df['Urun'].nunique()
            summary['months'] = sorted(df['Ay'].dropna().unique().tolist())
        
        return summary
