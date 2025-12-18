# Knight's Tour Visualizer  
**Penyelesaian Masalah Knight's Tour dengan Visualisasi Interaktif**

<img src="image.png" width="800" />


## Judul
Visualisasi Knight's Tour Problem menggunakan Warnsdorff's Algorithm dengan Mode Open Tour dan Closed Tour

---

## Deskripsi Masalah
Permasalahan *Knight's Tour* adalah masalah klasik dalam teori graf di mana seekor kuda catur harus mengunjungi setiap kotak pada papan catur tepat satu kali. Kuda bergerak dengan pola "L" - 2 kotak ke satu arah dan 1 kotak ke arah tegak lurus, atau sebaliknya.

Dalam konteks graf, setiap kotak pada papan catur merepresentasikan simpul (node), dan setiap gerakan kuda yang valid merepresentasikan sisi (edge). Masalah ini mencari **Hamiltonian Path** - jalur yang mengunjungi setiap simpul tepat satu kali.

Terdapat dua jenis solusi Knight's Tour:
1. **Open Tour**: Kuda mengakhiri perjalanan di sembarang kotak yang tidak terhubung dengan posisi awal
2. **Closed Tour**: Kuda mengakhiri perjalanan di kotak yang dapat menyerang posisi awal dalam satu gerakan (membentuk siklus Hamiltonian)

---

## Tujuan Program
Program ini dibuat untuk:
- Memvisualisasikan proses penyelesaian Knight's Tour pada papan catur 8×8
- Menunjukkan perbedaan antara Open Tour dan Closed Tour
- Menyediakan animasi step-by-step untuk memahami pergerakan kuda
- Mengimplementasikan Warnsdorff's Algorithm secara interaktif
- Menyediakan antarmuka GUI yang user-friendly

---

## Proses Penyelesaian
1. Pengguna memilih posisi awal kuda pada papan catur (baris 0-7, kolom 0-7)
2. Pengguna memilih mode tour yang diinginkan:
   - **Open Tour**: kuda mengakhiri di sembarang kotak
   - **Closed Tour**: kuda mengakhiri di attacking square dari posisi awal
3. Program menjalankan algoritma Warnsdorff untuk menemukan jalur optimal
4. Jalur perjalanan kuda divisualisasikan pada papan catur dengan:
   - Angka urutan kunjungan (1-64)
   - Garis panah biru menunjukkan jalur perjalanan
   - Marker START (hijau) dan END (merah)
5. Program menampilkan informasi lengkap: posisi awal, posisi akhir, jumlah kotak yang dikunjungi, dan tipe tour
6. Fitur animasi memungkinkan pengguna melihat perjalanan kuda secara bertahap

---

## Algoritma yang Digunakan

### 1. Warnsdorff's Algorithm (Heuristic Approach)
Algoritma ini menggunakan pendekatan heuristik untuk menemukan Knight's Tour dengan tingkat keberhasilan tinggi (~99% untuk Open Tour).

**Prinsip Kerja:**
```
Untuk setiap langkah:
1. Dari posisi current, identifikasi semua gerakan kuda yang valid
2. Untuk setiap gerakan, hitung accessibility:
   - Accessibility = jumlah gerakan valid dari posisi tersebut
3. Pilih gerakan dengan accessibility TERENDAH
4. Pindahkan kuda ke posisi tersebut
5. Ulangi hingga semua kotak dikunjungi
```

---

### 2. Open Tour
Pada mode Open Tour:
- Kuda dapat mengakhiri perjalanan di kotak mana saja
- Lebih mudah ditemukan (success rate ~99%)
- Tidak membentuk siklus Hamiltonian
- Cocok untuk pemahaman dasar Knight's Tour

**Kondisi Berhasil:**
```
Semua 64 kotak berhasil dikunjungi tepat satu kali
```

---

### 3. Closed Tour
Pada mode Closed Tour:
- Kuda harus mengakhiri di kotak yang dapat menyerang posisi awal
- Membentuk siklus Hamiltonian (Hamiltonian Cycle)
- Lebih sulit ditemukan
- Program akan mencoba hingga 100 percobaan

**Kondisi Berhasil:**
```
1. Semua 64 kotak dikunjungi tepat satu kali
2. Posisi akhir dapat menyerang posisi awal dalam satu gerakan kuda
   (jarak Manhattan = (2,1) atau (1,2))
```

**Verifikasi Closed Tour:**
Jika posisi awal adalah (x₁, y₁) dan posisi akhir adalah (x₂, y₂), maka:
```
|x₂ - x₁| = 2 dan |y₂ - y₁| = 1, atau
|x₂ - x₁| = 1 dan |y₂ - y₁| = 2
```

---


## Cara Menjalankan Program

```bash
python theKnightTour_visualizer.py
```

---

## Cara Menggunakan Program

### Input Posisi Awal
- Gunakan **Spinbox "Baris"** untuk memilih baris (0-7)
  - 0 = baris paling atas
  - 7 = baris paling bawah
- Gunakan **Spinbox "Kolom"** untuk memilih kolom (0-7)
  - 0 = kolom paling kiri
  - 7 = kolom paling kanan

### Pilih Mode Tour
**Mode Open Tour:**
- Klik radio button **"Open Tour"**
- Kuda akan mengakhiri perjalanan di sembarang kotak
- Success rate tinggi (~99%)
- Recommended untuk pemula

**Mode Closed Tour:**
- Klik radio button **"Closed Tour"**
- Kuda akan mengakhiri di attacking square dari posisi awal
- Lebih challenging
- Program akan retry hingga 100x jika tidak ditemukan

### Solve Tour
Klik tombol **"Solve Tour"**
- Program menjalankan algoritma Warnsdorff
- Papan catur menampilkan hasil visualisasi:
  - **Angka 1**: Posisi awal (warna hijau)
  - **Angka 2-63**: Posisi intermediate
  - **Angka 64**: Posisi akhir (warna merah)
  - **Garis biru**: Jalur perjalanan dengan panah
  - **Text "START"**: Marker posisi awal
  - **Text "END"**: Marker posisi akhir

### Animate (Opsional)
Klik tombol **"Animate"**
- Menampilkan animasi step-by-step
- Kotak yang sedang dikunjungi ditandai **lingkaran merah**
- Status menampilkan: "Animating... Step X/64"
- Kecepatan: 200ms per step (dapat diubah di kode)

### Reset
Klik tombol **"Reset"**
- Membersihkan papan catur
- Menghapus semua visualisasi
- Siap untuk tour baru

---

## Output Program

### Visualisasi Papan Catur
```
┌─────────────────────────────┐
│  0   1   2   3   4   5   6   7    ← Koordinat Kolom
│
0 │ [1] 60  39  34  31  18   9  64  ← Angka = urutan kunjungan
1 │ 38  35 [2] 61  10  63  32  19
2 │ 59  52  37  40  33  30  17   8
3 │ 36  49  42  51  62  11  20  29
4 │ 43  58  53  46  41  24   7  16
5 │ 50  47  44  23  54  15  28  21
6 │ 57   4  55  48  45  26  13   6
7 │  3  56  22   5  14  25  12  27
   ↑
Koordinat Baris
```

### Info Panel
```
Start: (0, 0) | Visited: 64/64 | End: (2, 1) | Type: OPEN TOUR
Status: SUCCESS
```

**Penjelasan:**
- **Start**: Posisi awal kuda
- **Visited**: Jumlah kotak yang berhasil dikunjungi
- **End**: Posisi akhir kuda
- **Type**: OPEN TOUR atau CLOSED TOUR 

### Status Indicator
- **Status: Ready** → Program siap
- **Status: Processing...** → Sedang mencari solusi
- **Status: SUCCESS** → Tour berhasil (64/64)
- **Status: Incomplete** → Tour tidak lengkap
- **Status: Animating...** → Sedang menampilkan animasi

---
