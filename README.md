# Grayscale Image Converter (Streamlit)

Program ini adalah aplikasi web sederhana berbasis Streamlit untuk mengubah gambar berwarna menjadi grayscale dengan beberapa metode yang berbeda.

## Deskripsi

Aplikasi menyediakan:
- Upload file gambar (PNG, JPG, JPEG, BMP, WEBP)
- Dropdown untuk memilih metode grayscale
- Preview gambar asli dan hasil metode terpilih
- Tombol download hasil metode yang dipilih
- Loading bar saat proses konversi gambar

## Metode Grayscale

Aplikasi menggunakan metode yang sama seperti referensi di `colorToGray.py`:

1. Averaging
   - Rumus: `(R + G + B) / 3`
2. Luminosity (Weighting)
   - Rumus: `0.299R + 0.587G + 0.114B`
3. Desaturation
   - Rumus: `(max(R, G, B) + min(R, G, B)) / 2`
4. Single Channel (Red)
   - Rumus: `R`
5. Decomposition (Max)
   - Rumus: `max(R, G, B)`
6. Decomposition (Min)
   - Rumus: `min(R, G, B)`

## Struktur File

- `app.py`: Aplikasi utama Streamlit
- `colorToGray.py`: Referensi fungsi grayscale versi console

## Cara Menjalankan

Anda bisa menggunakan salah satu cara berikut.

### Opsi 1: Buka Versi Online

1. Buka link berikut di browser:

   https://color2gray.streamlit.app

### Opsi 2: Jalankan Secara Lokal

1. Buat virtual environment (opsional tapi direkomendasikan)

   Windows PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependensi

   ```powershell
   pip install streamlit pillow
   ```

3. Jalankan aplikasi

   ```powershell
   streamlit run app.py
   ```

4. Buka browser di alamat yang ditampilkan Streamlit (biasanya `http://localhost:8501`).
