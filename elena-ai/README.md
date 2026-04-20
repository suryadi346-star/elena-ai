# elena-ai

<h1 align="center">E.L.E.N.A AI</h1>

```
    ███████╗██╗     ███████╗███╗   ██╗ █████╗
    ██╔════╝██║     ██╔════╝████╗  ██║██╔══██╗
    █████╗  ██║     █████╗  ██╔██╗ ██║███████║
    ██╔══╝  ██║     ██╔══╝  ██║╚██╗██║██╔══██║
    ███████╗███████╗███████╗██║ ╚████║██║  ██║
    ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
```

**Ethical Learning & Network Assistant v2.0**

E.L.E.N.A adalah chatbot AI berbasis terminal yang menggunakan DeepSeek Chat melalui OpenRouter API. Cocok untuk Termux, Pydroid3, dan environment Python lainnya.

## 🚀 Features

- 💬 Conversational AI dengan memori percakapan
- 🔄 Streaming response real-time
- 📝 Auto-summarization untuk percakapan panjang
- 🎨 Colorful ASCII art banner
- ⚙️ Adjustable temperature settings
- 🔐 Secure API key management
- 📱 Mobile-friendly (Termux & Pydroid3)

## 📋 Requirements

- Python 3.7+
- `requests` library

## 🔧 Installation

### For Termux (Android)

```bash
# Update & install Python
pkg update && pkg upgrade
pkg install python git

# Clone repository
git clone https://github.com/suryadi346-star/elena-ai
cd elena-ai

# Install dependencies
pip install requests

# Run
python elena.py
```

### For Pydroid3 (Android)

1. Buka Pydroid3
2. Menu → Pip → Install `requests`
3. Download `elena.py` dari repository
4. Run script

### For PC/Linux

```bash
# Clone repository
git clone https://github.com/suryadi346-star/elena-ai
cd elena-ai

# Install dependencies
pip install requests

# Run
python elena.py
```

## 🔑 API Key Setup

1. Dapatkan API key dari [OpenRouter](https://openrouter.ai/keys)
2. Jalankan program:
```bash
python elena.py
```
3. Masukkan API key saat diminta
4. API key akan disimpan di `key.txt` (jangan commit file ini!)

## 💻 Usage

### Commands

- `/help` - Menampilkan daftar command
- `/reset` - Reset percakapan
- `/temp` - Menampilkan temperature saat ini
- `/temp <value>` - Set temperature (0.0 - 1.5)
- `exit` atau `quit` - Keluar dari program

### Example

```
E.L.E.N.A :> Hello!

E.L.E.N.A:
Hey! How can I help you today?

--------------------------------------------------

E.L.E.N.A :> What is Python?

E.L.E.N.A:
Python is a high-level programming language...
```

## ⚙️ Configuration

- **Model**: DeepSeek Chat
- **API**: OpenRouter
- **Temperature**: 0.7 (default, adjustable)
- **Max Tokens**: 4096
- **Max History**: 150 messages or 200k characters

## 📁 File Structure

```
elena-ai/
├── elena.py              # Main program
├── key.txt              # API key storage (auto-generated)
├── README.md            # This file
├── INSTALL_PYDROID3.md  # Pydroid3 installation guide
└── .gitignore           # Git ignore rules
```

## 🔒 Security

⚠️ **IMPORTANT**: 
- API key disimpan di `key.txt` 
- **JANGAN** commit `key.txt` ke repository!
- File `.gitignore` sudah mengabaikan `key.txt`

## 🐛 Troubleshooting

### Error: ModuleNotFoundError: No module named 'requests'
```bash
pip install requests
```

### Error: API key invalid
1. Pastikan copy API key dengan benar
2. Cek di https://openrouter.ai/keys
3. Hapus `key.txt` dan jalankan ulang

### Error: Connection failed
1. Pastikan internet aktif
2. Coba gunakan WiFi
3. Restart aplikasi

## 📱 Platform Support

- ✅ Termux (Android)
- ✅ Pydroid3 (Android)
- ✅ Linux
- ✅ macOS
- ✅ Windows (WSL/Git Bash)
- ✅ Windows Terminal

## 👨‍💻 Developer

**Suryadi**

- GitHub: [@suryadi346-star](https://github.com/suryadi346-star/elena-ai)
- Repository: [elena-ai](https://github.com/suryadi346-star/elena-ai)

## 📜 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

E.L.E.N.A AI adalah tool eksperimental untuk pembelajaran. Gunakan dengan bijak dan bertanggung jawab.

---

<h1 align="center">Made with ❤️ by Suryadi</h1>

<div align="center">
  
[⬆ Kembali ke atas](#️-elena-ai)

</div>

