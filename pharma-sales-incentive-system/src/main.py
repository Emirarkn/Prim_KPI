"""
Pharma Sales Incentive System - Ana Uygulama
Flet tabanlı modern kullanıcı arayüzü
"""

import flet as ft
from pathlib import Path
import sys

# Proje kök dizinini path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
from src.incentive_calculator import IncentiveCalculator
from src.report_generator import ReportGenerator


class PharmaSalesApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.data_loader = DataLoader()
        self.calculator = IncentiveCalculator()
        self.report_gen = ReportGenerator()
        
        # State
        self.current_view = "dashboard"
        self.loaded_data = {}
        
        self.build_ui()
    
    def setup_page(self):
        """Sayfa ayarları"""
        self.page.title = "Pharma Sales Incentive System"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 800
        self.page.window.min_height = 600
    
    def build_ui(self):
        """Ana UI yapısını oluştur"""
        # Sol menü
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.UPLOAD_FILE_OUTLINED,
                    selected_icon=ft.Icons.UPLOAD_FILE,
                    label="Veri Yükle",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.Icons.ANALYTICS,
                    label="Performans",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PAYMENTS_OUTLINED,
                    selected_icon=ft.Icons.PAYMENTS,
                    label="Prim",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.DESCRIPTION_OUTLINED,
                    selected_icon=ft.Icons.DESCRIPTION,
                    label="Raporlar",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Ayarlar",
                ),
            ],
            on_change=self.nav_change,
        )
        
        # Ana içerik alanı
        self.content_area = ft.Container(
            content=self.build_dashboard(),
            expand=True,
            padding=20,
        )
        
        # Ana layout
        self.page.add(
            ft.Row(
                [
                    self.nav_rail,
                    ft.VerticalDivider(width=1),
                    self.content_area,
                ],
                expand=True,
            )
        )
    
    def nav_change(self, e):
        """Navigasyon değişikliği"""
        views = {
            0: self.build_dashboard,
            1: self.build_data_import,
            2: self.build_performance,
            3: self.build_incentive,
            4: self.build_reports,
            5: self.build_settings,
        }
        
        self.content_area.content = views.get(e.control.selected_index, self.build_dashboard)()
        self.page.update()
    
    def build_dashboard(self):
        """Dashboard görünümü"""
        return ft.Column(
            [
                ft.Text("📊 Dashboard", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row(
                    [
                        self._create_stat_card("Toplam ST", "24", ft.Colors.BLUE),
                        self._create_stat_card("Aktif Bölge", "4", ft.Colors.GREEN),
                        self._create_stat_card("Bölge Müdürü", "6", ft.Colors.ORANGE),
                        self._create_stat_card("Brick", "500+", ft.Colors.PURPLE),
                    ],
                    wrap=True,
                ),
                ft.Container(height=20),
                ft.Text("📈 Çeyreklik Özet", size=20, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Text(
                        "Veri yükledikten sonra performans özeti burada görünecek.",
                        color=ft.Colors.GREY_600,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def _create_stat_card(self, title: str, value: str, color: str):
        """İstatistik kartı oluştur"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=14, color=ft.Colors.GREY_600),
                    ft.Text(value, size=32, weight=ft.FontWeight.BOLD, color=color),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=150,
            height=100,
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def build_data_import(self):
        """Veri yükleme görünümü"""
        def pick_file(file_type: str):
            def handler(e):
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"{file_type} dosyası seçildi"),
                    action="Tamam",
                )
                self.page.snack_bar.open = True
                self.page.update()
            return handler
        
        return ft.Column(
            [
                ft.Text("📥 Veri Yükle", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Gerekli Dosyalar", size=18, weight=ft.FontWeight.W_500),
                ft.Container(height=10),
                self._create_upload_row("Hedef Dosyası", "Target25.xlsx", pick_file("Hedef")),
                self._create_upload_row("Satış Verisi", "Sell_Out.xlsx", pick_file("Satış")),
                self._create_upload_row("Ziyaret Detay", "Ziyaret_Detay.xlsx", pick_file("Ziyaret")),
                self._create_upload_row("Sipariş Verisi", "Siparis.xlsx", pick_file("Sipariş")),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Tümünü İşle",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=lambda e: self._process_all_data(),
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def _create_upload_row(self, label: str, hint: str, on_click):
        """Dosya yükleme satırı"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.INSERT_DRIVE_FILE, color=ft.Colors.GREY_600),
                    ft.Column(
                        [
                            ft.Text(label, weight=ft.FontWeight.W_500),
                            ft.Text(hint, size=12, color=ft.Colors.GREY_500),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.ElevatedButton("Dosya Seç", on_click=on_click),
                ],
            ),
            padding=15,
            bgcolor=ft.Colors.GREY_50,
            border_radius=8,
            margin=ft.margin.only(bottom=10),
        )
    
    def _process_all_data(self):
        """Tüm verileri işle"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Veriler işleniyor..."),
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def build_performance(self):
        """Performans görünümü"""
        return ft.Column(
            [
                ft.Text("📊 Performans", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Tabs(
                    selected_index=0,
                    tabs=[
                        ft.Tab(text="ST Bazlı", icon=ft.Icons.PERSON),
                        ft.Tab(text="BM Bazlı", icon=ft.Icons.GROUP),
                        ft.Tab(text="Bölge Bazlı", icon=ft.Icons.MAP),
                        ft.Tab(text="Ürün Bazlı", icon=ft.Icons.INVENTORY),
                    ],
                ),
                ft.Container(
                    content=ft.Text(
                        "Performans verileri için önce veri yüklemeniz gerekiyor.",
                        color=ft.Colors.GREY_600,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                ),
            ],
        )
    
    def build_incentive(self):
        """Prim hesaplama görünümü"""
        return ft.Column(
            [
                ft.Text("💰 Prim Hesaplama", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Yıl",
                            options=[ft.dropdown.Option("2025")],
                            value="2025",
                            width=120,
                        ),
                        ft.Dropdown(
                            label="Çeyrek",
                            options=[
                                ft.dropdown.Option("Q1", "Q1 (Oca-Mar)"),
                                ft.dropdown.Option("Q2", "Q2 (Nis-Haz)"),
                                ft.dropdown.Option("Q3", "Q3 (Tem-Eyl)"),
                                ft.dropdown.Option("Q4", "Q4 (Eki-Ara)"),
                            ],
                            value="Q4",
                            width=180,
                        ),
                        ft.ElevatedButton(
                            "Hesapla",
                            icon=ft.Icons.CALCULATE,
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),
                ft.Container(height=20),
                ft.Text("KPI Ağırlıkları", size=18, weight=ft.FontWeight.W_500),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("KPI")),
                        ft.DataColumn(ft.Text("Ağırlık")),
                        ft.DataColumn(ft.Text("Min Eşik")),
                        ft.DataColumn(ft.Text("Max Eşik")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Satış Hacmi")),
                            ft.DataCell(ft.Text("%60")),
                            ft.DataCell(ft.Text("%85")),
                            ft.DataCell(ft.Text("%165")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Dağılım")),
                            ft.DataCell(ft.Text("%15")),
                            ft.DataCell(ft.Text("%85")),
                            ft.DataCell(ft.Text("%165")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Rota Uyumu")),
                            ft.DataCell(ft.Text("%15")),
                            ft.DataCell(ft.Text("%85")),
                            ft.DataCell(ft.Text("%165")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Sipariş Başarısı")),
                            ft.DataCell(ft.Text("%10")),
                            ft.DataCell(ft.Text("%85")),
                            ft.DataCell(ft.Text("%165")),
                        ]),
                    ],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def build_reports(self):
        """Raporlar görünümü"""
        return ft.Column(
            [
                ft.Text("📋 Raporlar", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.TABLE_CHART),
                    title=ft.Text("ST Performans Kartı"),
                    subtitle=ft.Text("Bireysel scorecard raporu"),
                    trailing=ft.IconButton(ft.Icons.DOWNLOAD),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.GROUPS),
                    title=ft.Text("BM Özet Raporu"),
                    subtitle=ft.Text("Bölge müdürü bazlı performans"),
                    trailing=ft.IconButton(ft.Icons.DOWNLOAD),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.INVENTORY_2),
                    title=ft.Text("Ürün Grubu Analizi"),
                    subtitle=ft.Text("Ürün bazlı hedef/gerçekleşme"),
                    trailing=ft.IconButton(ft.Icons.DOWNLOAD),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ROUTE),
                    title=ft.Text("Ziyaret Uyum Raporu"),
                    subtitle=ft.Text("Plan vs gerçekleşen ziyaretler"),
                    trailing=ft.IconButton(ft.Icons.DOWNLOAD),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PAYMENTS),
                    title=ft.Text("Çeyreklik Prim Raporu"),
                    subtitle=ft.Text("Prim hak kazanan ST listesi"),
                    trailing=ft.IconButton(ft.Icons.DOWNLOAD),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def build_settings(self):
        """Ayarlar görünümü"""
        return ft.Column(
            [
                ft.Text("⚙️ Ayarlar", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ExpansionPanelList(
                    expand_icon_color=ft.Colors.BLUE,
                    elevation=1,
                    controls=[
                        ft.ExpansionPanel(
                            header=ft.ListTile(title=ft.Text("ST Yönetimi")),
                            content=ft.Container(
                                content=ft.Text("ST ekleme, çıkarma ve düzenleme işlemleri"),
                                padding=10,
                            ),
                        ),
                        ft.ExpansionPanel(
                            header=ft.ListTile(title=ft.Text("Brick Yönetimi")),
                            content=ft.Container(
                                content=ft.Text("Brick-ST atama işlemleri"),
                                padding=10,
                            ),
                        ),
                        ft.ExpansionPanel(
                            header=ft.ListTile(title=ft.Text("Ürün Grupları")),
                            content=ft.Container(
                                content=ft.Text("Ürün grubu tanımları ve ağırlıkları"),
                                padding=10,
                            ),
                        ),
                        ft.ExpansionPanel(
                            header=ft.ListTile(title=ft.Text("KPI Ayarları")),
                            content=ft.Container(
                                content=ft.Text("KPI ağırlıkları ve eşik değerleri"),
                                padding=10,
                            ),
                        ),
                    ],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )


def main(page: ft.Page):
    """Uygulama giriş noktası"""
    PharmaSalesApp(page)


if __name__ == "__main__":
    ft.app(target=main)
