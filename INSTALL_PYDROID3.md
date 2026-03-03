# Cara Install E.L.E.N.A AI di Pydroid3 (Android)

## 📱 Langkah Instalasi

### 1. Install Module `requests`

Buka Pydroid3, lalu:

**Pilihan A - Via Menu Pydroid3:**
1. Buka menu (☰) di Pydroid3
2. Pilih **"Pip"** atau **"Terminal"**
3. Ketik: `pip install requests`
4. Tunggu sampai selesai

**Pilihan B - Via Terminal:**
```bash
pip install requests
```

### 2. Download File

Download 3 file dari repository:
- `elena.py`
- `README.md` 
- `.gitignore`

### 3. Jalankan Program

```bash
python elena.py
```

### 4. Masukkan API Key

Saat pertama kali dijalankan:
1. Buka browser: https://openrouter.ai/keys
2. Daftar/Login
3. Copy API key (format: `sk-or-v1-...`)
4. Paste di Pydroid3

---

## ⚠️ Troubleshooting

### Error: ModuleNotFoundError: No module named 'requests'

**Solusi:**
```bash
pip install requests
```

Atau gunakan menu Pydroid3:
- Menu → Pip → ketik `requests` → Install

### Error: API key invalid

**Solusi:**
- Pastikan copy API key dengan benar (tidak ada spasi)
- Cek di https://openrouter.ai/keys
- Hapus file `key.txt` lalu jalankan ulang

### Error: Connection failed

**Solusi:**
- Pastikan internet aktif
- Coba gunakan WiFi jika mobile data lambat
- Restart aplikasi Pydroid3

---

## 🎯 Quick Start (Pydroid3)

```bash
# 1. Install requests
pip install requests

# 2. Jalankan
python elena.py

# 3. Masukkan API key saat diminta

# 4. Mulai chat!
E.L.E.N.A :> Hello!
```

---

## 📝 Catatan Penting

- **API Key gratis** tersedia di OpenRouter
- File `key.txt` akan dibuat otomatis (jangan dihapus)
- Koneksi internet diperlukan untuk setiap chat
- Ctrl+C untuk keluar

---

Developer: Suryadi
Repository: https://github.com/suryadiarsyil-ops/elena-ai
