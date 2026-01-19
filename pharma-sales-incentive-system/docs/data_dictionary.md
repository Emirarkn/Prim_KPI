# 📚 Veri Sözlüğü (Data Dictionary)

Bu belge, sistemde kullanılan veri yapılarını ve alanları tanımlar.

---

## 📊 Ana Veri Dosyaları

### 1. Target (Hedef) Dosyası

| Alan | Tip | Açıklama | Örnek |
|------|-----|----------|-------|
| `Ay` | Integer | Hedef ayı (1-12) | 1, 2, 3 |
| `BM` | String | Bölge Müdürü kodu/adı | BM_001 |
| `Mumessil` | String | Satış Temsilcisi kodu/adı | ST_001 |
| `Brick` | String | Coğrafi bölge kodu | BRICK_001 |
| `Urun` | String | Ürün grubu adı | URUN_GRUBU_A |
| `Hedef` | Integer | Hedef satış adedi | 1000 |

### 2. Sell-Out (Satış) Dosyası

| Alan | Tip | Açıklama | Örnek |
|------|-----|----------|-------|
| `Tarih` | DateTime | Satış tarihi | 2025-01-15 |
| `Brick` | String | Satış yapılan brick | BRICK_001 |
| `GLN` | String | Eczane/Müşteri kodu | GLN_0001 |
| `Urun` | String | Satılan ürün grubu | URUN_GRUBU_A |
| `Adet` | Integer | Satış adedi | 50 |

### 3. Ziyaret Dosyası

| Alan | Tip | Açıklama | Örnek |
|------|-----|----------|-------|
| `Tarih` | DateTime | Ziyaret tarihi | 2025-01-15 |
| `ST` | String | Ziyareti yapan ST | ST_001 |
| `Musteri` | String | Ziyaret edilen müşteri | MUSTERI_0001 |
| `Aktivite` | String | Aktivite tipi | Ziyaret, Sipariş |
| `Gerceklesti` | Boolean | Gerçekleşme durumu | True/False |

### 4. Scorecard Dosyası

| Alan | Tip | Açıklama | Örnek |
|------|-----|----------|-------|
| `Urun_Grubu` | String | Ürün grubu adı | URUN_GRUBU_A |
| `Agirlik` | Float | KPI ağırlığı (%) | 15 |
| `Min_Esik` | Float | Minimum eşik oranı | 0.85 |
| `Max_Esik` | Float | Maximum eşik oranı | 1.65 |

---

## 🏢 Organizasyon Yapısı

### Hiyerarşi

```
Şirket
└── Bölge (4 adet)
    └── Bölge Müdürü (BM)
        └── Satış Temsilcisi (ST) (4-6 adet)
            └── Brick (çok sayıda)
                └── Müşteri/Eczane (GLN)
```

### ST-BM İlişkisi

| Alan | Tip | Açıklama |
|------|-----|----------|
| `Mumessil` | String | ST kodu |
| `BM` | String | Bağlı olduğu BM |
| `Bolge` | String | Bölge adı |

### Brick-ST İlişkisi

| Alan | Tip | Açıklama |
|------|-----|----------|
| `Brick` | String | Brick kodu |
| `Mumessil` | String | Sorumlu ST |

---

## 📈 KPI Metrikleri

### Satış Hacmi (Weight: 60%)

```
Oran = Gerçekleşen Satış / Hedef Satış

Puan = 
  - 0        (eğer Oran < 0.85)
  - Ağırlık × 1.65  (eğer Oran > 1.65)
  - Ağırlık × Oran  (diğer durumlarda)
```

### Rota Uyumu (Weight: 15%)

```
Oran = Gerçekleşen Ziyaret / Planlanan Ziyaret
```

### Sipariş Başarısı (Weight: 10%)

```
Oran = Sipariş Alınan Müşteri / Hedef Müşteri
```

### Dağılım (Weight: 15%)

```
Oran = Satış Yapılan Ürün Çeşidi / Hedef Ürün Çeşidi
```

---

## 📅 Dönem Tanımları

| Dönem | Aylar | Açıklama |
|-------|-------|----------|
| Q1 | 1, 2, 3 | Ocak - Mart |
| Q2 | 4, 5, 6 | Nisan - Haziran |
| Q3 | 7, 8, 9 | Temmuz - Eylül |
| Q4 | 10, 11, 12 | Ekim - Aralık |

---

## 🎯 Prim Eşikleri

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| `bonus_threshold` | 85 | Minimum toplam skor |
| `min_threshold` | 0.85 | Minimum gerçekleşme oranı |
| `max_threshold` | 1.65 | Maximum puan alınabilecek oran |

---

## 📝 Veri Kalitesi Kuralları

### Zorunlu Alanlar
- `Ay`: Boş olamaz, 1-12 arası olmalı
- `Hedef`: Pozitif sayı olmalı
- `Tarih`: Geçerli tarih formatında olmalı

### Referans Bütünlüğü
- Her `Mumessil` bir `BM`'e bağlı olmalı
- Her `Brick` bir `Mumessil`'e atanmış olmalı
- `Urun` değerleri Scorecard'da tanımlı olmalı

### Veri Tipleri
- Sayısal alanlar: Integer veya Float
- Tarih alanları: YYYY-MM-DD formatı
- Kod alanları: Büyük harf, alt çizgi ile
