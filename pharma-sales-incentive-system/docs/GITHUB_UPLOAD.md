# 🚀 GitHub'a Yükleme Rehberi

## Ön Hazırlık

### 1. GitHub Hesabı
- GitHub hesabınız yoksa [github.com](https://github.com) adresinden oluşturun
- SSH key oluşturun (önerilir): `ssh-keygen -t ed25519`

### 2. Git Kurulumu Kontrolü
```bash
git --version
# Çıktı: git version 2.x.x
```

---

## 📦 Yeni Repository Oluşturma

### Adım 1: GitHub'da Repository Oluştur

1. GitHub'a giriş yapın
2. Sağ üstteki "+" → "New repository"
3. Ayarlar:
   - **Repository name:** `pharma-sales-incentive-system`
   - **Description:** `İlaç sektörü için saha satış yönetimi ve prim hesaplama sistemi`
   - **Visibility:** ⚠️ **Private** (hassas veriler için)
   - **Initialize:** BOŞ bırakın (README, .gitignore eklemeyin)
4. "Create repository" tıklayın

### Adım 2: Yerel Repository Başlat

```bash
# Proje dizinine gidin
cd pharma-sales-incentive-system

# Git başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Pharma Sales Incentive System v1.0.0"

# Ana branch'i main yap
git branch -M main

# Remote ekle (kendi kullanıcı adınızı yazın)
git remote add origin git@github.com:KULLANICI_ADI/pharma-sales-incentive-system.git

# Push
git push -u origin main
```

---

## 🔒 Güvenlik Kontrolü (ÖNEMLİ!)

### Push Öncesi Kontrol Listesi

```bash
# 1. Hassas dosya kontrolü
git status

# 2. .gitignore çalışıyor mu?
cat .gitignore | head -50

# 3. Hangi dosyalar commit edilecek?
git diff --cached --name-only

# 4. Excel dosyası var mı? (OLMAMALI!)
git diff --cached --name-only | grep -E "\.xlsx$"
# Boş çıktı olmalı!

# 5. Eğer Excel dosyası varsa, kaldır:
git reset HEAD dosya_adi.xlsx
```

### .gitignore Doğrulama

```bash
# Bu dosyaların IGNORE edildiğini kontrol edin:
git check-ignore -v Target25.xlsx
git check-ignore -v BrickST.xlsx
git check-ignore -v STBM.xlsx
# Çıktı: .gitignore:XX:pattern    dosya_adi.xlsx
```

---

## 📁 Dosya Yapısı Kontrolü

GitHub'a yüklenmesi gereken dosyalar:

```
✅ YÜKLENMELİ:
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config/
│   ├── kpi_weights.json
│   ├── product_groups.json
│   └── regions.json
├── data/
│   └── sample/          ✅ Sadece örnek veriler
│       ├── Sample_Target.xlsx
│       ├── Sample_SellOut.xlsx
│       └── ...
├── docs/
│   ├── SECURITY.md
│   ├── data_dictionary.md
│   └── user_guide.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── data_loader.py
│   ├── incentive_calculator.py
│   └── report_generator.py
└── tests/
    └── test_calculator.py

❌ YÜKLENMEMELİ:
├── Target25.xlsx
├── BrickST.xlsx
├── STBM.xlsx
├── bölgestbrickgln.xlsx
├── Hedeflenen_*.xlsx
├── Scorecard.xlsx
├── Kriter.xlsx
└── *_Sell_out*.xlsx
```

---

## 🔄 Sonraki Güncellemeler

### Değişiklik Yapıldığında

```bash
# Değişiklikleri görüntüle
git status
git diff

# Değişiklikleri ekle
git add -A

# Commit
git commit -m "Açıklayıcı mesaj"

# Push
git push
```

### Branch Stratejisi (Önerilir)

```bash
# Yeni özellik için branch
git checkout -b feature/yeni-ozellik

# Geliştirme yap...
git add -A
git commit -m "Yeni özellik eklendi"

# Main'e merge
git checkout main
git merge feature/yeni-ozellik
git push
```

---

## 🏷️ Versiyon Etiketleme

```bash
# Versiyon etiketi ekle
git tag -a v1.0.0 -m "İlk kararlı sürüm"

# Etiketi push et
git push origin v1.0.0
```

---

## ⚠️ Sorun Giderme

### Yanlışlıkla Hassas Dosya Yüklediyseniz

```bash
# 1. Dosyayı git geçmişinden sil
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch HASSAS_DOSYA.xlsx" \
  --prune-empty --tag-name-filter cat -- --all

# 2. Remote'u güncelle
git push origin --force --all

# 3. GitHub'da "Settings" > "Secrets" kontrol et
```

### Push Reddedilirse

```bash
# Önce pull yap
git pull origin main --rebase

# Sonra push
git push
```

---

## 📞 Yardım

- GitHub Docs: https://docs.github.com
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf
