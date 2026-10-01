# Gnosis

> Platform analitik data berbasis web modern untuk ekstraksi berita/tren otomatis, pemrosesan data, visualisasi grafik interaktif, dan wawasan AI *real-time*.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal?style=flat-square&logo=fastapi)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=flat-square&logo=tailwind-css)
![Chart.js](https://img.shields.io/badge/Chart.js-4.0-ff6384?style=flat-square&logo=chart.js)

---

## 🚀 Gambaran Umum (Overview)
**Gnosis** adalah aplikasi *End-to-End Data Pipeline* yang dirancang untuk menarik data teks/artikel secara otomatis dari berbagai portal web berita di Indonesia (Teknologi, Keuangan, Olahraga, hingga Tren Nasional), membersihkannya, menyimpannya ke dalam basis data relasional, serta menyajikannya dalam bentuk dashboard interaktif yang elegan.

---

## ✨ Fitur Utama
* **Custom Web Scraper & Anti-Block Mechanism:** Dilengkapi *User-Agent spoofing* dan sistem *fallback* cerdas untuk memastikan proses penarikan data tetap berjalan lancar tanpa terganggu proteksi keamanan situs web.
* **Database Relasional Terstruktur:** Menyimpan riwayat data artikel secara aman menggunakan SQLite dengan arsitektur REST API FastAPI.
* **Statistik Perbandingan Multi-Sumber:** Grafik batang interaktif (`Chart.js`) yang mengelompokkan jumlah data berdasarkan domain sumber secara *real-time*.
* **Dynamic AI Insights Engine:** Kotak wawasan analitik yang membaca kondisi database secara langsung untuk merangkum tren informasi yang paling mendominasi.
* **Desain UI/UX Modern:** Dibangun menggunakan Tailwind CSS dengan antarmuka yang bersih, responsif, dan ramah pengguna.

---

## 🛠️ Teknologi yang Digunakan
* **Backend:** Python, FastAPI, Uvicorn, SQLite
* **Data Processing & Scraping:** BeautifulSoup4, Requests, Pandas
* **Frontend:** HTML5, Tailwind CSS (CDN), JavaScript (ES6), Chart.js

---

## ⚙️ Cara Instalasi & Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek secara lokal di komputer Anda:

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/username/insightpulse-studio.git](https://github.com/username/insightpulse-studio.git)
   cd insightpulse-studio