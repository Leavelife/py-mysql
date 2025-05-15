-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Bulan Mei 2025 pada 01.46
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `montoring_tugas_akhir`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `dosen`
--

CREATE TABLE `dosen` (
  `NIDN` varchar(10) NOT NULL,
  `nama_dosen` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `dosen`
--

INSERT INTO `dosen` (`NIDN`, `nama_dosen`) VALUES
('19021', 'Kartika'),
('19381', 'Azhar');

-- --------------------------------------------------------

--
-- Struktur dari tabel `dosen_mk`
--

CREATE TABLE `dosen_mk` (
  `nidn` varchar(10) NOT NULL,
  `kode_mk` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `dosen_mk`
--

INSERT INTO `dosen_mk` (`nidn`, `kode_mk`) VALUES
('19021', 'PTI201'),
('19381', 'PTI302');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `NIM` varchar(10) NOT NULL,
  `nama_mhs` varchar(100) DEFAULT NULL,
  `kelas` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mahasiswa`
--

INSERT INTO `mahasiswa` (`NIM`, `nama_mhs`, `kelas`) VALUES
('1234', 'Said', 'PTi B'),
('5678', 'Nuru', 'PTI C');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mata_kuliah`
--

CREATE TABLE `mata_kuliah` (
  `kode_mk` varchar(10) NOT NULL,
  `nama_mk` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mata_kuliah`
--

INSERT INTO `mata_kuliah` (`kode_mk`, `nama_mk`) VALUES
('PTI201', 'Basis data'),
('PTI302', 'Pemrograman Berorientasi Objek');

-- --------------------------------------------------------

--
-- Struktur dari tabel `monitoring_tugas`
--

CREATE TABLE `monitoring_tugas` (
  `id_monitoring` int(11) NOT NULL,
  `id_tugas` int(11) DEFAULT NULL,
  `status` enum('proposal','revisi','pengerjaan','selesai') NOT NULL,
  `komentar` text DEFAULT NULL,
  `NIDN` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `monitoring_tugas`
--

INSERT INTO `monitoring_tugas` (`id_monitoring`, `id_tugas`, `status`, `komentar`, `NIDN`) VALUES
(2321, 421, 'revisi', 'Kurang mendeskripsikan projek', '19021'),
(2322, 422, 'pengerjaan', 'OOP tidak semua diterapkan ', '19381');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tugas`
--

CREATE TABLE `tugas` (
  `id_tugas` int(11) NOT NULL,
  `NIM` varchar(10) DEFAULT NULL,
  `judul` text DEFAULT NULL,
  `link_dokumen` varchar(255) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tugas`
--

INSERT INTO `tugas` (`id_tugas`, `NIM`, `judul`, `link_dokumen`, `kode_mk`) VALUES
(421, '1234', 'Normalisasi data siswa sman 1 malang', 'https://google.drive/folder-tugas akhir', 'PTI201'),
(422, '5678', 'Implementasi OOP pada sistem manajemen kost', 'https://google.drive/folder-tugas akhir', 'PTI302');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`NIDN`);

--
-- Indeks untuk tabel `dosen_mk`
--
ALTER TABLE `dosen_mk`
  ADD KEY `nidn` (`nidn`,`kode_mk`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- Indeks untuk tabel `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`NIM`);

--
-- Indeks untuk tabel `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  ADD PRIMARY KEY (`kode_mk`);

--
-- Indeks untuk tabel `monitoring_tugas`
--
ALTER TABLE `monitoring_tugas`
  ADD PRIMARY KEY (`id_monitoring`),
  ADD KEY `id_tugas` (`id_tugas`),
  ADD KEY `NIDN` (`NIDN`);

--
-- Indeks untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`id_tugas`),
  ADD KEY `NIM` (`NIM`),
  ADD KEY `kode_mk` (`kode_mk`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `monitoring_tugas`
--
ALTER TABLE `monitoring_tugas`
  MODIFY `id_monitoring` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2324;

--
-- AUTO_INCREMENT untuk tabel `tugas`
--
ALTER TABLE `tugas`
  MODIFY `id_tugas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=423;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `dosen_mk`
--
ALTER TABLE `dosen_mk`
  ADD CONSTRAINT `dosen_mk_ibfk_1` FOREIGN KEY (`nidn`) REFERENCES `dosen` (`NIDN`),
  ADD CONSTRAINT `dosen_mk_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode_mk`);

--
-- Ketidakleluasaan untuk tabel `monitoring_tugas`
--
ALTER TABLE `monitoring_tugas`
  ADD CONSTRAINT `monitoring_tugas_ibfk_1` FOREIGN KEY (`id_tugas`) REFERENCES `tugas` (`id_tugas`) ON DELETE CASCADE,
  ADD CONSTRAINT `monitoring_tugas_ibfk_2` FOREIGN KEY (`NIDN`) REFERENCES `dosen` (`NIDN`) ON DELETE SET NULL;

--
-- Ketidakleluasaan untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD CONSTRAINT `tugas_ibfk_1` FOREIGN KEY (`NIM`) REFERENCES `mahasiswa` (`NIM`) ON DELETE CASCADE,
  ADD CONSTRAINT `tugas_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode_mk`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
