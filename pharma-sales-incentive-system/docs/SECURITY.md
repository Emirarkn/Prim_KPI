# 🔒 Güvenlik ve Gizlilik Rehberi

## ⚠️ ÖNEMLİ UYARI

Bu proje, ilaç sektörü satış yönetimi için tasarlanmıştır. Gerçek verilerle çalışırken aşağıdaki kurallara **kesinlikle** uyulmalıdır.

---

## 🚫 GitHub'a ASLA Yüklenmemesi Gereken Dosyalar

### Kişisel Bilgiler İçeren Dosyalar
| Dosya Tipi | Açıklama | Risk |
|------------|----------|------|
| `Target*.xlsx` | Çalışan isimleri, hedefler | YÜKSEK |
| `*BrickST*.xlsx` | ST atamaları, isimler | YÜKSEK |
| `*STBM*.xlsx` | Çalışan hiyerarşisi | YÜKSEK |
| `bölge*gln*.xlsx` | Müşteri bilgileri, GLN | KRİTİK |
| `Hedeflenen*.xlsx` | Müşteri listesi | KRİTİK |

### Ticari Sır İçeren Dosyalar
| Dosya Tipi | Açıklama | Risk |
|------------|----------|------|
| `Scorecard.xlsx` | Prim stratejisi | YÜKSEK |
| `Kriter.xlsx` | Değerlendirme kriterleri | YÜKSEK |
| `*_Sell_out*.xlsx` | Satış verileri | ORTA |
| `Ürün_Gr.xlsx` | Ürün fiyatlandırma | ORTA |

---

## ✅ Güvenli Kullanım Rehberi

### 1. Yerel Geliştirme

```bash
# Gerçek verileri proje dışında tutun
/home/kullanici/
├── pharma-sales-incentive-system/    # Git repo (güvenli)
└── pharma-data/                       # Gerçek veriler (Git dışında)
    ├── Target25.xlsx
    ├── SellOut_Q4.xlsx
    └── ...
```

### 2. .gitignore Kontrolü

Her commit öncesi kontrol edin:

```bash
# Hangi dosyalar commit edilecek?
git status

# Hassas dosya var mı?
git diff --cached --name-only | grep -E "\.xlsx$"
```

### 3. Yanlışlıkla Yükleme Durumunda

```bash
# Dosyayı git geçmişinden tamamen sil
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch HASSAS_DOSYA.xlsx" \
  --prune-empty --tag-name-filter cat -- --all

# Veya BFG Repo-Cleaner kullan
bfg --delete-files HASSAS_DOSYA.xlsx
```

---

## 📋 Veri Anonimleştirme Rehberi

Eğer örnek veri paylaşmanız gerekiyorsa:

### Kişi İsimleri
```
BERTAN KURU → ST_001
ATİLLA TOKATLIOĞLU → BM_001
```

### Müşteri Bilgileri
```
GLN: 8691234567890 → GLN_0001
Eczane: GÜNEŞ ECZANE → MUSTERI_0001
```

### Lokasyon Bilgileri
```
IST ATAKOY+YESILKOY → BRICK_001
İstanbul → BOLGE_1
```

---

## 🔐 Önerilen Güvenlik Önlemleri

### Repository Ayarları
- [ ] Repository'yi **Private** yapın
- [ ] Branch protection kuralları ekleyin
- [ ] Collaborator'ları sınırlı tutun

### Kod İncelemesi
- [ ] Her PR'da hassas veri kontrolü
- [ ] Otomatik secret scanning aktif
- [ ] Pre-commit hook'ları kullanın

### Erişim Kontrolü
- [ ] 2FA zorunlu
- [ ] SSH key kullanımı
- [ ] Token süreleri kısa tutun

---

## 📞 Güvenlik İhlali Durumunda

1. **Hemen** repository'yi private yapın
2. Hassas dosyaları git geçmişinden silin
3. Etkilenen kişileri/kurumları bilgilendirin
4. Şirket IT/güvenlik ekibine bildirin

---

## 📄 KVKK / GDPR Uyumluluğu

Bu sistem kişisel veri işlediğinden:

- Veri işleme amacı belgelenmeli
- Veri saklama süreleri belirlenmeli
- Silme/düzeltme talepleri karşılanabilmeli
- Veri aktarımı güvenli yapılmalı

---

**Son Güncelleme:** 2025
**Sorumlu:** Proje Yöneticisi
