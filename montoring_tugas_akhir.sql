-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 19 Bulan Mei 2025 pada 17.17
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

DELIMITER $$
--
-- Prosedur
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_periksa_tugas` (IN `p_id_tugas` INT, IN `p_nidn` VARCHAR(10), IN `p_komentar` TEXT)   BEGIN
    DECLARE v_kode_mk VARCHAR(10);
    DECLARE v_nidn_dosen VARCHAR(10);

    -- Cari kode_mk dari tugas
    SELECT kode_mk INTO v_kode_mk FROM tugas WHERE id_tugas = p_id_tugas;
    IF v_kode_mk IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tugas tidak ditemukan';
    END IF;

    -- Ambil NIDN pengampu dari mata_kuliah
    SELECT nidn INTO v_nidn_dosen FROM dosen_mk WHERE kode_mk = v_kode_mk;
    IF v_nidn_dosen IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Dosen pengampu tidak ditemukan';
    END IF;

    -- Cek apakah nidn cocok
    IF p_nidn != v_nidn_dosen THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Anda tidak memiliki izin mengomentari tugas ini';
    END IF;

    -- Update monitoring_tugas
    UPDATE monitoring_tugas
    SET NIDN = p_nidn, komentar = p_komentar
    WHERE id_tugas = p_id_tugas;

END$$

DELIMITER ;

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
('19301', 'Wahyu'),
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
('19301', 'PTI303'),
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
('1234', 'Muhammad Said Agiel Bahadjai', 'PTI_B'),
('2345', 'Nabigh Nailur', 'PTI_C'),
('5678', 'Nuru Syhri Ramadhan', 'PTI_C'),
('9012', 'Radiska Rizki Ramadhani Nuraini', 'TI_B');

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
('PTI302', 'Pemrograman Berorientasi Objek'),
('PTI303', 'Dasar Pemrograman Komputer');

-- --------------------------------------------------------

--
-- Struktur dari tabel `monitoring_tugas`
--

CREATE TABLE `monitoring_tugas` (
  `id_monitoring` int(11) NOT NULL,
  `id_tugas` int(11) DEFAULT NULL,
  `komentar` text DEFAULT NULL,
  `NIDN` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `monitoring_tugas`
--

INSERT INTO `monitoring_tugas` (`id_monitoring`, `id_tugas`, `komentar`, `NIDN`) VALUES
(2333, 421, 'Kurang mendeskripsikan projekt', '19021'),
(2334, 422, 'OOP tidak semua diterapkan', '19381'),
(2335, 423, 'Silahkan lanjut pengerjaan isi', '19301'),
(2336, 424, 'Pembuatan aplikasi tahap 2', '19021');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tugas`
--

CREATE TABLE `tugas` (
  `id_tugas` int(11) NOT NULL,
  `NIM` varchar(10) DEFAULT NULL,
  `judul` text DEFAULT NULL,
  `link_dokumen` varchar(255) DEFAULT NULL,
  `kode_mk` varchar(10) DEFAULT NULL,
  `status` enum('proposal','revisi','pengerjaan','selesai') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tugas`
--

INSERT INTO `tugas` (`id_tugas`, `NIM`, `judul`, `link_dokumen`, `kode_mk`, `status`) VALUES
(421, '1234', 'Normalisasi data sisuva sman 1 malang', 'https://github.com/me/normalisasi-data', 'PTI201', 'revisi'),
(422, '5678', 'Implementasi OOP pada sistem manajemen kost', 'https://github.com/me/manajemen-kost', 'PTI303', 'pengerjaan'),
(423, '9012', 'Penggunaan python untuk pembelajaran dasar dpk', 'https://github/me/penggunaan-python', 'PTI303', 'proposal'),
(424, '2345', 'Optimasi Kinerja Query pada Sistem Basis Data Relasional dengan Penggunaan Indeks', 'https://github/me/optimasi-kinerja', 'PTI201', 'proposal');

--
-- Trigger `tugas`
--
DELIMITER $$
CREATE TRIGGER `after_insert_tugas` AFTER INSERT ON `tugas` FOR EACH ROW BEGIN
  INSERT INTO monitoring_tugas (id_tugas, komentar, NIDN)
  VALUES (NEW.id_tugas, NULL, NULL);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_monitoring_tugas`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_monitoring_tugas` (
`NIM` varchar(10)
,`nama_mhs` varchar(100)
,`judul` text
,`nama_mk` varchar(100)
,`link_dokumen` varchar(255)
,`status` enum('proposal','revisi','pengerjaan','selesai')
,`komentar` text
,`nama_dosen` varchar(100)
);

-- --------------------------------------------------------

--
-- Struktur untuk view `v_monitoring_tugas`
--
DROP TABLE IF EXISTS `v_monitoring_tugas`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_monitoring_tugas`  AS SELECT `m`.`NIM` AS `NIM`, `m`.`nama_mhs` AS `nama_mhs`, `t`.`judul` AS `judul`, `mk`.`nama_mk` AS `nama_mk`, `t`.`link_dokumen` AS `link_dokumen`, `t`.`status` AS `status`, `mt`.`komentar` AS `komentar`, `d`.`nama_dosen` AS `nama_dosen` FROM ((((`tugas` `t` join `mahasiswa` `m` on(`m`.`NIM` = `t`.`NIM`)) left join `monitoring_tugas` `mt` on(`mt`.`id_tugas` = `t`.`id_tugas`)) left join `mata_kuliah` `mk` on(`mk`.`kode_mk` = `t`.`kode_mk`)) left join `dosen` `d` on(`mt`.`NIDN` = `d`.`NIDN`)) ;

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
  ADD KEY `monitoring_tugas_ibfk_2` (`NIDN`);

--
-- Indeks untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`id_tugas`),
  ADD KEY `kode_mk` (`kode_mk`),
  ADD KEY `tugas_ibfk_1` (`NIM`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `monitoring_tugas`
--
ALTER TABLE `monitoring_tugas`
  MODIFY `id_monitoring` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2337;

--
-- AUTO_INCREMENT untuk tabel `tugas`
--
ALTER TABLE `tugas`
  MODIFY `id_tugas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=456;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `dosen_mk`
--
ALTER TABLE `dosen_mk`
  ADD CONSTRAINT `dosen_mk_ibfk_1` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode_mk`),
  ADD CONSTRAINT `dosen_mk_ibfk_2` FOREIGN KEY (`nidn`) REFERENCES `dosen` (`NIDN`);

--
-- Ketidakleluasaan untuk tabel `monitoring_tugas`
--
ALTER TABLE `monitoring_tugas`
  ADD CONSTRAINT `monitoring_tugas_ibfk_1` FOREIGN KEY (`id_tugas`) REFERENCES `tugas` (`id_tugas`) ON DELETE CASCADE,
  ADD CONSTRAINT `monitoring_tugas_ibfk_2` FOREIGN KEY (`NIDN`) REFERENCES `dosen` (`NIDN`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD CONSTRAINT `tugas_ibfk_1` FOREIGN KEY (`NIM`) REFERENCES `mahasiswa` (`NIM`) ON DELETE SET NULL ON UPDATE NO ACTION,
  ADD CONSTRAINT `tugas_ibfk_2` FOREIGN KEY (`kode_mk`) REFERENCES `mata_kuliah` (`kode_mk`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
