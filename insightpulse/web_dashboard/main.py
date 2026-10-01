import sqlite3
from fastapi import FastAPI, Query, HTTPException, Form
from fastapi.responses import HTMLResponse
from processing.cleaner import clean_and_store_data

app = FastAPI(title="InsightPulse Studio", version="3.1")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gnosis | AI-Powered Data Analytics</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body class="bg-slate-50 text-slate-800 font-sans antialiased min-h-screen pb-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
            
            <!-- Header Section -->
            <div class="bg-gradient-to-r from-blue-700 to-indigo-800 text-white p-8 rounded-3xl shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div class="space-y-2">
                    <div class="inline-flex items-center gap-2 bg-blue-600/50 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold tracking-wide text-blue-100 uppercase border border-blue-400/30">
                        <span>⚡ Enterprise Data Pipeline</span>
                    </div>
                    <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight">Gnosis</h1>
                    <p class="text-blue-100 text-sm max-w-xl">Platform ekstraksi data web otomatis, pembersihan data berbasis Pandas, dan analitik tren Indonesia cerdas.</p>
                </div>
                <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 text-right hidden sm:block">
                    <div class="text-xs text-blue-200">Status Sistem</div>
                    <div class="text-sm font-bold flex items-center gap-1.5 justify-end mt-0.5">
                        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>Aktif & Terhubung</span>
                    </div>
                </div>
            </div>

            <!-- Scraper Control Card -->
            <div class="bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-slate-100 space-y-5">
                <div>
                    <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span>🔍</span> Masukkan Target URL / Tren Indonesia
                    </h2>
                    <p class="text-slate-500 text-sm mt-0.5">Ketik URL portal berita/tren apa pun untuk membandingkan data dan melihat grafik secara dinamis.</p>
                </div>

                <!-- Input & Button Group -->
                <div class="flex flex-col md:flex-row gap-3 items-center">
                    <div class="relative w-full md:flex-1">
                        <input type="text" id="targetUrl" 
                               placeholder="Contoh: https://www.cnnindonesia.com/teknologi" 
                               class="w-full px-4 py-3.5 pl-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-600 focus:bg-white text-sm transition shadow-inner">
                    </div>
                    <button onclick="triggerCustomScraper()" id="btnScrape" 
                            class="w-full md:w-auto bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-semibold px-8 py-3.5 rounded-2xl shadow-lg shadow-blue-500/25 transition duration-200 flex items-center justify-center gap-2 text-sm whitespace-nowrap">
                        <span>🚀 Tarik Data & Analisis</span>
                    </button>
                </div>

                <!-- Quick Suggestion Pills -->
                <div class="flex flex-wrap items-center gap-2 pt-2">
                    <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider mr-1">Rekomendasi Cepat:</span>
                    <button onclick="setPresetUrl('https://www.cnnindonesia.com/teknologi')" class="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 text-slate-600 px-3 py-1.5 rounded-xl border border-slate-200 transition">CNN Teknologi</button>
                    <button onclick="setPresetUrl('https://www.cnbcindonesia.com/market')" class="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 text-slate-600 px-3 py-1.5 rounded-xl border border-slate-200 transition">CNBC Market</button>
                    <button onclick="setPresetUrl('https://finance.detik.com/')" class="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 text-slate-600 px-3 py-1.5 rounded-xl border border-slate-200 transition">Detik Finance</button>
                    <button onclick="setPresetUrl('https://tekno.kompas.com/')" class="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 text-slate-600 px-3 py-1.5 rounded-xl border border-slate-200 transition">Kompas Tekno</button>
                </div>
            </div>

            <!-- Status Alert Box -->
            <div id="statusAlert" class="hidden p-4 rounded-2xl text-sm font-medium transition-all duration-300"></div>

            <!-- Grid Layout: Chart & AI Insights -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Chart Card -->
                <div class="bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                                <span>📊</span> Statistik Perbandingan Sumber
                            </h2>
                            <span class="text-xs text-slate-400 bg-slate-100 px-2.5 py-1 rounded-lg">Real-time Comparison</span>
                        </div>
                        <p class="text-slate-500 text-xs mb-4">Grafik batang membandingkan jumlah artikel antar domain web yang Anda tarik.</p>
                    </div>
                    <div class="relative h-72 w-full">
                        <canvas id="authorChart"></canvas>
                    </div>
                </div>

                <!-- AI Insights Card (NOW FULLY DYNAMIC) -->
                <div class="bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col justify-between">
                    <div>
                        <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2 mb-1">
                            <span>🤖</span> Analisis Wawasan AI Indonesia
                        </h2>
                        <p class="text-slate-500 text-xs mb-4">Ringkasan analitik otomatis yang merespons data database secara langsung.</p>
                        
                        <div class="bg-gradient-to-br from-slate-50 to-blue-50/50 p-5 rounded-2xl border border-slate-200/80 text-slate-700 text-sm leading-relaxed space-y-3">
                            <p id="aiInsightText">Memuat wawasan AI...</p>
                        </div>
                    </div>
                    <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                        <span>Engine: Smart Database Analytics</span>
                        <span class="text-blue-600 font-medium">Dynamic Mode</span>
                    </div>
                </div>
            </div>

            <!-- Data Table Card -->
            <div class="bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-slate-100 space-y-4">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                    <div>
                        <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                            <span>📋</span> Repositori Data Terbaru
                        </h2>
                        <p class="text-slate-500 text-sm">Data dari berbagai situs berkumpul secara terstruktur di sini.</p>
                    </div>
                    <button onclick="loadData()" class="text-xs font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 px-3.5 py-2 rounded-xl transition flex items-center gap-1.5">
                        <span>🔄 Muat Ulang Tabel</span>
                    </button>
                </div>

                <div class="overflow-x-auto rounded-2xl border border-slate-100">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50/70 text-slate-500 text-xs uppercase tracking-wider border-b border-slate-100">
                                <th class="p-4 font-semibold">ID</th>
                                <th class="p-4 font-semibold">Judul / Konten Artikel (Text)</th>
                                <th class="p-4 font-semibold">Sumber Domain</th>
                            </tr>
                        </thead>
                        <tbody id="dataTableBody" class="divide-y divide-slate-100 text-sm text-slate-700">
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

        <!-- Script untuk Interaksi Dinamis -->
        <script>
            function setPresetUrl(url) {
                document.getElementById('targetUrl').value = url;
            }

            async function loadData() {
                try {
                    // 1. Muat data tabel
                    const resTable = await fetch('/api/quotes?limit=8&offset=0');
                    const result = await resTable.json();
                    
                    const tbody = document.getElementById('dataTableBody');
                    tbody.innerHTML = '';
                    
                    if (result.data.length === 0) {
                        tbody.innerHTML = `<tr><td colspan="3" class="p-6 text-center text-slate-400">Belum ada data di database. Silakan jalankan scraper di atas.</td></tr>`;
                        return;
                    }

                    result.data.forEach(item => {
                        tbody.innerHTML += `
                            <tr class="hover:bg-slate-50/80 transition duration-150">
                                <td class="p-4 font-mono text-xs text-slate-400">#${item.id}</td>
                                <td class="p-4 font-medium text-slate-800 leading-relaxed">${item.text}</td>
                                <td class="p-4">
                                    <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-100">
                                        ${item.author}
                                    </span>
                                </td>
                            </tr>
                        `;
                    });

                    // 2. Muat data chart statistik perbandingan
                    const resChart = await fetch('/api/chart-stats');
                    const chartData = await resChart.json();
                    renderChart(chartData.labels, chartData.counts);

                    // 3. Muat analisis AI dinamis
                    const resAi = await fetch('/api/ai-insight');
                    const aiData = await resAi.json();
                    document.getElementById('aiInsightText').innerHTML = aiData.insight;

                } catch (err) {
                    console.error("Gagal memuat data:", err);
                }
            }

            let myChart = null;
            function renderChart(labels, dataCounts) {
                const ctx = document.getElementById('authorChart').getContext('2d');
                if (myChart) myChart.destroy();

                myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Jumlah Artikel',
                            data: dataCounts,
                            backgroundColor: '#2563eb',
                            hoverBackgroundColor: '#1d4ed8',
                            borderRadius: 10,
                            barThickness: 'flex',
                            maxBarThickness: 40
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { 
                                beginAtZero: true, 
                                ticks: { stepSize: 1, precision: 0 },
                                grid: { color: '#f1f5f9' }
                            },
                            x: {
                                grid: { display: false }
                            }
                        }
                    }
                });
            }

            async function triggerCustomScraper() {
                const urlInput = document.getElementById('targetUrl').value;
                const btn = document.getElementById('btnScrape');
                const alertBox = document.getElementById('statusAlert');
                
                btn.disabled = true;
                btn.innerHTML = `<svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> <span>Memproses...</span>`;
                
                alertBox.className = "p-4 rounded-2xl text-sm font-medium bg-blue-50 text-blue-700 border border-blue-200 block shadow-sm";
                alertBox.innerHTML = "⏳ <strong>Sedang Berjalan:</strong> Menarik data, membersihkan teks dengan Pandas, dan memperbarui grafik analitik...";

                try {
                    const response = await fetch('/api/run-scraper', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: new URLSearchParams({ url: urlInput })
                    });
                    
                    const data = await response.json();
                    
                    alertBox.className = "p-4 rounded-2xl text-sm font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 block shadow-sm";
                    alertBox.innerHTML = `✅ <strong>Berhasil!</strong> ${data.message} (${data.total_added} data baru ditambahkan).`;
                    
                    // Segarkan seluruh dashboard seketika
                    loadData();
                } catch (err) {
                    alertBox.className = "p-4 rounded-2xl text-sm font-medium bg-rose-50 text-rose-700 border border-rose-200 block shadow-sm";
                    alertBox.innerHTML = "❌ <strong>Gagal:</strong> Terjadi kesalahan saat menarik data.";
                } finally {
                    btn.disabled = false;
                    btn.innerHTML = "<span>🚀 Tarik Data & Analisis</span>";
                }
            }

            loadData();
        </script>
    </body>
    </html>
    """

@app.post("/api/run-scraper")
def api_run_scraper(url: str = Form(None)):
    try:
        target = url if url and url.strip() != "" else None
        added_count = clean_and_store_data(target)
        return {
            "status": "success", 
            "message": "Pipeline data berhasil diselesaikan!",
            "total_added": added_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quotes")
def get_quotes(limit: int = 8, offset: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, author FROM quotes ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM quotes")
    total = cursor.fetchone()[0]
    conn.close()
    
    quotes_list = [{"id": r["id"], "text": r["text"], "author": r["author"]} for r in rows]
    return {"total_data_in_database": total, "data": quotes_list}

@app.get("/api/chart-stats")
def get_chart_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author, COUNT(*) as count FROM quotes GROUP BY author ORDER BY count DESC LIMIT 6")
    rows = cursor.fetchall()
    conn.close()
    
    labels = [r["author"] for r in rows]
    counts = [r["count"] for r in rows]
    
    return {"labels": labels, "counts": counts}

@app.get("/api/ai-insight")
def get_ai_insight():
    """Endpoint baru untuk menghasilkan Analisis Wawasan AI secara dinamis."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM quotes")
    total_data = cursor.fetchone()[0]
    
    cursor.execute("SELECT author, COUNT(*) as cnt FROM quotes GROUP BY author ORDER BY cnt DESC LIMIT 3")
    top_sources = cursor.fetchall()
    conn.close()
    
    if total_data == 0:
        return {"insight": "Belum ada data di database. Silakan jalankan tombol 'Tarik Data & Analisis' di atas."}
    
    sources_summary = ", ".join([f"<strong>{row['author']}</strong> ({row['cnt']} data)" for row in top_sources])
    
    insight_html = (
        f"💡 <strong>Analisis Tren AI Indonesia:</strong> Dari total <strong>{total_data}</strong> data artikel/tren yang tersimpan di sistem, "
        f"kontribusi sumber terbesar saat ini berasal dari: {sources_summary}. "
        f"Distribusi ini menunjukkan variasi informasi lintas portal yang sangat baik untuk perbandingan tren digital."
    )
    return {"insight": insight_html}