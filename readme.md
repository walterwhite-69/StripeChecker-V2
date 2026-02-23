# 💳 StripeChecker-V2 

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/walterwhite-69/StripeChecker-V2?style=for-the-badge&color=gold)
![GitHub Forks](https://img.shields.io/github/forks/walterwhite-69/StripeChecker-V2?style=for-the-badge&color=blue)
![Python](https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python)
![Developer](https://img.shields.io/badge/Developer-Walter-red?style=for-the-badge)

**Tired of scrolling through endless Telegram channels looking for a "free" checker?**  
*Oh wait, most of them are "paid" now? Or they log your hits? Or they're just plain broken?*  
Welcome to the club. We made this because we were tired of the same old BS.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Safety](#-safety)

</div>

---

## 🚀 Features

- **Blazing Fast Concurrency**: Multi-threaded engine using `ThreadPoolExecutor`. Check cards faster than a Telegram scammer blocks you.
- **Premium Rich UI**: A professional terminal interface with a clean layout and color-coded results. No messy scrolling walls of text.
- **Dynamic Telemetry**: Automatically generates random `muid`, `guid`, and `sid` to bypass Stripe's "unsupported surface" restrictions.
- **Smart Proxy Rotation**: Supports `ip:port` and `ip:port:user:pass`. Rotates on every check to keep you under the radar.
- **Mass Processing**: Just point it to your combolist and let it handle the rest.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/walterwhite-69/StripeChecker-V2

# Enter the directory
cd StripeChecker-V2

# Install requirements
pip install requests Faker rich
```

## 📖 Usage

1. **Combos**: Put your cards in a file (Format: `number|mm|yy|cvv`).
2. **Proxies**: (Optional) Put your proxies in a file (Format: `ip:port` or `ip:port:user:pass`).
3. **Run**:
```bash
python checker.py
```
4. **Configure**: Enter file paths and thread count (Recommended: 10-50 for stability).

## 🛡️ Safety & Disclaimer

> [!WARNING]
> This tool is for **educational and research purposes only**. The developer assumes no responsibility for any misuse of this software. Don't be that guy.

---

**Author** - [Walter](https://github.com/walterwhite-69)  
**Main Repository** - [StripeChecker-V2](https://github.com/walterwhite-69/StripeChecker-V2)

*If this helped you, definitely star the repo. Or keep paying for those Telegram bots, your choice.* 😉
