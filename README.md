# 💊 Pharma Sales Incentive Management System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flet](https://img.shields.io/badge/UI-Flet-purple.svg)](https://flet.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Türkiye'deki ilaç sektörü için geliştirilmiş kapsamlı saha satış yönetimi ve teşvik (prim) hesaplama sistemi.

## 🎯 Proje Amacı

Bu sistem, ilaç şirketlerinin saha satış temsilcilerinin (ÜTT/ST) performansını takip etmek, hedeflerle karşılaştırmak ve çeyreklik prim hesaplamalarını otomatikleştirmek için tasarlanmıştır.

## ✨ Özellikler

- 📊 **Performans Takibi**: ST ve BM bazlı performans görüntüleme
- 🎯 **Hedef Yönetimi**: Aylık ve çeyreklik hedef takibi
- 💰 **Prim Hesaplama**: Ağırlıklı KPI bazlı otomatik prim hesaplama
- 📈 **Raporlama**: Detaylı Excel rapor çıktıları
- 🗺️ **Bölge Yönetimi**: ? bölge, ? BM, ??+ ST organizasyonu
- 📁 **Veri İthalatı**: Excel dosyalarından otomatik veri yükleme

## 📋 KPI Yapısı

| KPI | Ağırlık | Açıklama |
|-----|---------|----------|
| Satış Hacmi | %60 | Ürün grubu bazlı satış performansı |
| Dağılım | %15 | Ürün çeşitliliği ve penetrasyon |
| Rota Uyumu | %15 | Planlanan vs gerçekleşen ziyaretler |
| Sipariş Başarısı | %10 | Sipariş dönüşüm oranı |

**Prim Eşiği**: Toplam skor ≥ %85

## 🏗️ Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                    FLET GUI (Modern UI)                      │
├─────────────────────────────────────────────────────────────┤
│  📥 Veri Yükle │ 📊 Performans │ 💰 Prim │ 📋 Raporlar     │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    İŞ KATMANI (Business Logic)               │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Veri Import  │ Hedef Mgmt   │ Prim Calc    │ Report Gen     │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    VERİ KATMANI (Data Layer)                 │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Excel Files  │ Master Data  │ Transaction  │ Config         │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

## 📁 Proje Yapısı

```
pharma-sales-incentive-system/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Flet uygulaması ana giriş
│   ├── data_loader.py          # Excel veri yükleme modülü
│   ├── incentive_calculator.py # Prim hesaplama motoru
│   ├── report_generator.py     # Rapor oluşturma modülü
│   └── ui/
│       ├── __init__.py
│       ├── dashboard.py        # Ana dashboard
│       ├── data_import.py      # Veri yükleme ekranı
│       ├── performance.py      # Performans görüntüleme
│       └── settings.py         # Ayarlar ekranı
├── data/
│   └── sample/                 # Örnek veri dosyaları
├── config/
│   ├── product_groups.json     # Ürün grubu tanımları
│   ├── regions.json            # Bölge yapılandırması
│   └── kpi_weights.json        # KPI ağırlıkları
├── docs/
│   ├── user_guide.md           # Kullanıcı kılavuzu
│   ├── data_dictionary.md      # Veri sözlüğü
│   └── calculation_logic.md    # Hesaplama mantığı
├── tests/
│   └── test_calculator.py      # Birim testleri
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Kurulum

### Gereksinimler



### Adımlar

```bash
# Repository'yi klonlayın
git clone https://github.com/YOUR_USERNAME/pharma-sales-incentive-system.git
cd pharma-sales-incentive-system

# Sanal ortam oluşturun (önerilir)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python src/main.py
```

## 📊 Veri Dosyaları

### Gerekli Girdi Dosyaları

| Dosya | Açıklama | Format |
|-------|----------|--------|
| `Target25.xlsx` | Aylık hedefler | Ay, BM, ST, Brick, Ürün, Hedef |
| `Sell_Out.xlsx` | Gerçekleşen satışlar | Tarih, Brick, GLN, Ürün, Adet |
| `Ziyaret_Detay.xlsx` | Ziyaret kayıtları | Tarih, ST, Müşteri, Aktivite |
| `Siparis.xlsx` | Sipariş bilgileri | Tarih, Brick, GLN, Sipariş |

### Master Dosyalar (Dahil)

| Dosya | Açıklama |
|-------|----------|
| `Scorecard.xlsx` | Ürün grupları ve ağırlıkları |
| `BrickST.xlsx` | Brick-ST atamaları |
| `STBM.xlsx` | ST-BM hiyerarşisi |
| `Kriter.xlsx` | Prim kriterleri |

## 💡 Kullanım

### 1. Veri Yükleme

```
Veri Yükle > Hedef Dosyası > [Target25.xlsx seç]
Veri Yükle > Satış Verisi > [Sell_Out dosyaları seç]
```

### 2. Performans Görüntüleme

```
Performans > ST Bazlı > [ST seç] > [Dönem seç]
Performans > BM Bazlı > [BM seç] > [Dönem seç]
```

### 3. Prim Hesaplama

```
Prim Hesaplama > Çeyrek Seç > [Q1/Q2/Q3/Q4] > Hesapla
```

### 4. Rapor Çıktısı

```
Raporlar > Excel Export > [Rapor tipi seç] > İndir
```

## 🔢 Prim Hesaplama Mantığı

```python
# Her ürün grubu için:
oran = gerceklesen / hedef

if oran < 0.85:
    puan = 0
elif oran > 1.65:
    puan = agirlik * 1.65
else:
    puan = agirlik * oran

toplam_puan = sum(tum_puanlar)

# Prim hakkı kontrolü
prim_hakki = toplam_puan >= 85
```

## 🗺️ Organizasyon Yapısı

```
Türkiye (4 Bölge)
├── MARMARA
│   ├── BM: Atilla Tokatlıoğlu
│   └── ST'ler: [6 kişi]
├── EGE
│   ├── BM: Cenker Turan
│   └── ST'ler: [6 kişi]
├── İÇ ANADOLU-KARADENİZ
│   ├── BM: Mehmet Taşpınar
│   └── ST'ler: [6 kişi]
└── DOĞU AKDENİZ
    ├── BM: Hasan Emir Bozlu
    └── ST'ler: [6 kişi]
```

## 🔧 Konfigürasyon

### KPI Ağırlıkları (`config/kpi_weights.json`)

```json
{
  "satis_hacmi": 60,
  "dagilim": 15,
  "rota_uyum": 15,
  "siparis_basarisi": 10
}
```

### Ürün Grupları (`config/product_groups.json`)

```json
{
  "--": {
    "urunler": ["---- 2MG", "-----4MG", "-----"],
    "agirlik": 10
  },
  "DIGER_ITRIYAT": {
    "urunler": ["******", "**********", "*********"],
    "agirlik": 5
  }
}
```

## 🧪 Test

```bash
# Tüm testleri çalıştır
pytest tests/

# Coverage ile çalıştır
pytest --cov=src tests/
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'i push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📞 İletişim

Sorularınız için issue açabilir veya doğrudan iletişime geçebilirsiniz.

---

**Not**: Bu sistem, Türkiye ilaç sektörü için özelleştirilmiş olup, Türkçe terminoloji ve yerel iş süreçlerini desteklemektedir.
