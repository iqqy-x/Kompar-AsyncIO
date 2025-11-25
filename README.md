# 🌦️ AsyncIO Weather Data Collector

Mengambil data kondisi cuaca seluruh kecamatan di sebuah provinsi menggunakan HTTP asynchronous (AsyncIO + aiohttp).

Proyek ini mengolah dataset kecamatan, membersihkannya, lalu mengambil data cuaca secara paralel berdasarkan koordinat (latitude & longitude) menggunakan WeatherAPI.

Hasil akhir berupa file Excel yang berisi:
- **Last Update** (time)
- **Suhu** (°C)
- **Kelembapan** (%)
- **Kondisi Cuaca** (Sunny, Cloudy, Rainy, dll)
- **Kecepatan Angin** (m/s)
- **Arah Angin** (°)
- **Sinar UV**

AsyncIO memungkinkan ratusan request API berjalan secara paralel, membuat proses pengambilan data jauh lebih cepat.

---

## 📁 Project Structure

```
project_asyncio/
│
├── data/
│   ├── cleaned/
│   │   └── kecamatan_cleaned.xlsx
│   ├── output/
│   │   └── hasil_cuaca.xlsx
│   └── raw/
│       └── diskominfo-od_16357_kode_wilayah_kecamatan.csv
│
├── .env
├── datacleaning.ipynb
└── main.py
```

---

## ⚙️ Instalasi & Persiapan

### 1. Clone Repository
```bash
git https://github.com/iqqy-x/Kompar-Asynio.git
```

### 2. Setup API Key

Buat file `.env` di root project:

```env
API_KEY=your_weatherapi_key
```

Dapatkan API key dari: [https://www.weatherapi.com/](https://www.weatherapi.com/)

---

## 🧹 Data Cleaning

Proses pembersihan dataset dilakukan dalam:
- `datacleaning.ipynb`

Output-nya adalah:
- `data/cleaned/kecamatan_cleaned.xlsx`

**Kolom yang dipakai:**
- `nama_kota`
- `nama_kecamatan`
- `latitude`
- `longitude`

---

## ⚡ AsyncIO Weather Fetching

Program utama menggunakan `aiohttp` + `asyncio` untuk menjalankan ratusan request API secara paralel.

### Alur Utama:
1. Baca file `kecamatan_cleaned.xlsx`
2. Buat coroutine untuk tiap kecamatan
3. Jalankan semua coroutine dengan `asyncio.gather()`
4. Gabungkan hasil ke DataFrame
5. Simpan ke `hasil_cuaca.xlsx`

---

## ▶️ Menjalankan Program

```bash
python main.py
```

**Output terminal:**
```
Mengambil data cuaca: 100%|██████████████████████| 627/627
File disimpan di data/output/hasil_cuaca.xlsx
Waktu eksekusi: 5.42 detik
```

---

## 📄 Contoh Output (hasil_cuaca.xlsx)

| nama_kota    | nama_kecamatan | latitude  | longitude | last_update      | suhu | kelembapan | kondisi | angin_ms | arah_angin | uv   |
|--------------|----------------|-----------|-----------|------------------|------|------------|---------|----------|------------|------|
| KAB. BOGOR   | CIBINONG       | -6.47891  | 106.845   | 2025-11-25 11:45 | 33   | 49         | Sunny   | 1.19     | 289        | 13.3 |
| KAB. BOGOR   | GUNUNG PUTRI   | -6.46461  | 106.8916  | 2025-11-25 11:45 | 33   | 49         | Sunny   | 1.30     | 298        | 13.3 |

---

## 🧠 Mengapa AsyncIO?

**Keuntungan menggunakan AsyncIO:**
- Non-blocking I/O → tidak menunggu API satu per satu
- Jauh lebih cepat dibanding synchronous
- Lebih ringan dari multithreading
- Cocok untuk ratusan request HTTP
- Memanfaatkan event loop untuk concurrency efisien