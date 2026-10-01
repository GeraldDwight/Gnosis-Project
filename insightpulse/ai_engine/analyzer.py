import sqlite3
import os
from openai import OpenAI

def analyze_data_with_ai():
    print("Membaca data dari database lokal...")
    
    # Membaca beberapa data dari SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, author FROM quotes LIMIT 5")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("Tidak ada data di database untuk dianalisis.")
        return

    # Menyusun data agar mudah dibaca oleh AI
    data_text = "\n".join([f"- \"{row[0]}\" oleh {row[1]}" for row in rows])
    
    print("Menghubungkan ke AI Engine...")
    
    # Pengecekan API Key OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("\n[Mode Simulasi AI Aktif]:")
        print("Catatan: Anda belum memasukkan API Key OpenAI di environment variable.")
        print("Berikut adalah simulasi hasil analisis AI berdasarkan data yang diambil:")
        print("--------------------------------------------------")
        print("💡 **Insight Analisis Tren:**")
        print("Data kutipan menunjukkan dominasi tema tentang ketekunan, motivasi diri, dan perjuangan hidup. Hal ini sangat relevan untuk konten pengembangan diri (*self-improvement*) di platform digital.")
        print("--------------------------------------------------")
        return

    # Jika API key tersedia, jalankan pemanggilan OpenAI yang sebenarnya
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Anda adalah seorang data analyst dan business insights expert."},
                {"role": "user", "content": f"Analisis data kutipan berikut dan berikan ringkasan tren atau wawasan singkat:\n{data_text}"}
            ]
        )
        insight = response.choices[0].message.content
        print("\n--- HASIL ANALISIS AI ---")
        print(insight)
    except Exception as e:
        print(f"Gagal memanggil API: {e}")

if __name__ == "__main__":
    analyze_data_with_ai()