# 😋 AngkringanPedia 😋

## 🔗 Tautan Deployment

*[AngkringanPedia](http://malvin-scafi-angkringanpedia.pbp.cs.ui.ac.id/)* <--- Click Here!!

## 🤔 Apa itu AngkringanPedia?

Yuk, pecinta angkringan! Bosan bingung mau makan apa? AngkringanPedia solusinya! Dengan AngkringanPedia, kamu bisa puas menjelajah ribuan menu angkringan favoritmu, dari nasi kucing yang bikin nagih sampai gorengan yang renyah. Mau cari sate favorit? Tinggal klik! Bikin ulasan dan rating, bagi rekomendasi sama teman-teman, dan jadi bagian dari komunitas pecinta angkringan terbesar! Yuk, cobain sekarang dan rasakan sensasi kuliner angkringan yang makin seru!

## 🫂 Anggota Kelompok 
| NPM | Name | GitHub Account | 
| -- | -- | -- |
| 2306152430 | Malvin Scafi | [Cyades](https://github.com/Cyades) |
| 2306227955 | Ischika Afrilla | [kaachiii](https://github.com/kaachiii) |
| 2306216075 | Juan Lukius | [juanlukius](https://github.com/juanlukius) |
| 2306221970 | Arya Gilang | [AryaGilangP](https://github.com/AryaGilangP) |
| 2306202826 | Nobel Julian Bintang | [nobeljb](https://github.com/nobeljb) |

## 🗂️ Modul

### 🔐 Admin and Authentication

**Dikerjakan oleh Ischika Afrilla**

Modul ini mencakup fitur untuk mengelola akun pengguna dan admin, termasuk autentikasi untuk akses ke aplikasi.

Fungsi Modul:

- Registrasi: Mengizinkan pengguna dan admin untuk mendaftar akun baru.
- Login: Menyediakan mekanisme login berbasis email/username dan password untuk pengguna dan admin.
- Logout: Menyediakan tombol logout untuk menghentikan sesi pengguna.
- Manajemen Admin: Admin dapat menambah, menghapus, atau mengedit informasi akun admin lain.
- Pengawasan Akun: Admin dapat melihat dan memoderasi akun pengguna, memastikan hanya akun yang sah yang bisa mengakses sistem.

Berikut aksi yang dapat dilakukan masing-masing _role_:
| User | Guest | Admin |
| ---- | ----- | ----- |
| Registrasi akun | Registrasi akun	| Mengelola data admin | 
| Login akun | Login akun | Mengawasi akun pengguna |
| Logout akun | - | Tambah/Hapus akun admin |


### 🖥️ Dashboard

**Dikerjakan oleh Arya Gilang Prasetya**

Modul Dashboard berfungsi sebagai pusat informasi pribadi pengguna yang memuat data dan memberikan opsi untuk mengeditnya.

Fungsi Modul:
- Informasi Pengguna: Menampilkan informasi pribadi pengguna seperti nama, umur, nomor handphone, dan alamat.
- Edit Profil: Pengguna dapat mengubah informasi pribadi melalui fitur ini.
- Keamanan Data: Pengelolaan data pribadi secara aman, termasuk kemampuan admin untuk memantau perubahan.

Berikut aksi yang dapat dilakukan masing-masing _role_:
| User | Guest | Admin |
| ---- | ----- | ----- |
| Melihat dan mengedit profil | - | Melihat data pengguna |
| Memperbarui informasi pribadi	| - | Mengedit informasi pengguna |
| - | - | Menghapus akun pengguna |

### 🏠 Homepage, Search and Filter

**Dikerjakan oleh Malvin Scafi**

Modul Homepage menyediakan fungsi pencarian dan filter untuk membantu pengguna menemukan makanan sesuai preferensi.

Fungsi Modul:
- Membuat Navigation Bar, Footer dan Homepage
- Daftar Makanan: Menampilkan daftar restoran dan menu makanan yang tersedia di platform.
- Pencarian: Pengguna dapat menggunakan fitur pencarian untuk menemukan makanan tertentu.
- Filter: Menyediakan filter berdasarkan kategori, rating, bahan baku, dan harga untuk mempermudah pencarian.

Berikut aksi yang dapat dilakukan masing-masing _role_:
| User | Guest | Admin |
| ---- | ----- | ----- |
| Melihat daftar makanan | Melihat daftar makanan | Menambahkan/menghapus makanan |
| Menggunakan fitur pencarian | Menggunakan fitur pencarian	| Mengedit data makanan |
| Menggunakan fitur filter | Menggunakan fitur filter | Menggunakan fitur filter |


### 🔍 Food Catalog

**Dikerjakan oleh Nobel Julian Bintang**

Modul ini menampilkan katalog makanan yang memungkinkan pengguna untuk melihat detail produk, memberikan ulasan, dan memberikan rating.

Fungsi Modul:
- Detail Produk Makanan: Menyediakan informasi lengkap mengenai setiap makanan, termasuk deskripsi, harga, dan gambar.
- Ulasan Produk: Pengguna dapat menulis ulasan yang akan ditampilkan kepada pengguna lain.
- Rating Produk: Pengguna dapat memberikan rating pada makanan, dan rating rata-rata akan diperbarui secara otomatis.
- Moderasi Ulasan: Admin memiliki kemampuan untuk menghapus ulasan yang tidak pantas atau memoderasi konten ulasan.

Berikut aksi yang dapat dilakukan masing-masing _role_:
| User | Guest | Admin |
| ---- | ----- | ----- |
| Melihat detail produk makanan | Melihat detail produk makanan | Mengelola ulasan pengguna |
| Memberi ulasan dan rating | - | Menghapus/memoderasi ulasan |
| Melihat rating rata-rata | Melihat rating rata-rata | - |


### ⭐ Favourite

**Dikerjakan oleh Juan Lukius Barnaby**

Modul Favorit memungkinkan pengguna untuk menandai restoran atau makanan yang mereka sukai agar mudah diakses kembali.

Fungsi Modul:
- Menandai Favorit: Pengguna dapat menandai makanan atau restoran sebagai favorit.
- Daftar Favorit: Pengguna dapat melihat daftar favorit yang menampilkan gambar, nama, dan informasi dasar.
- Mengelola Favorit Pengguna: Admin dapat melihat daftar favorit pengguna dan menghapus favorit yang dianggap tidak relevan atau tidak sesuai dengan kebijakan platform.
- Akses ke Detail: Dari daftar favorit, pengguna bisa langsung mengakses halaman detail untuk memberikan ulasan atau melihat informasi lebih lanjut.

Berikut aksi yang dapat dilakukan masing-masing _role_:
| User | Guest | Admin |
| ---- | ----- | ----- |
| Menambah/menghapus favorit | - | Mengelola favorit pengguna |
| Melihat daftar favorit | - | Melihat dan menghapus favorit pengguna |
| Mengakses halaman detail dari favorit | - | - |


## 📝 Dataset

AngkringanPedia mengambil dataset dari [Menu Angkringan Jogja](https://cookpad.com/id/cari/menu%20angkringan%20jogja)

Berikut merupakan dataset yang sudah di convert menjadi .json --> [Dataset](dataset.json) 


## 🎭 Jenis Pengguna (_Role_)

Pada aplikasi kami, terdapat tiga jenis pengguna:

- User
- Guest
- Admin

Penjelasan lebih rinci tentang setiap jenis pengguna dan kewenangannya dalam aplikasi tersedia di deskripsi masing-masing modul.
