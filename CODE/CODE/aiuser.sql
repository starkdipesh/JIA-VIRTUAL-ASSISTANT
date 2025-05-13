-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 17, 2025 at 10:27 AM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aiuser`
--

-- --------------------------------------------------------

--
-- Table structure for table `owner`
--

CREATE TABLE `owner` (
  `username` varchar(15) NOT NULL,
  `emailid` varchar(30) NOT NULL,
  `dob` date NOT NULL,
  `pasword` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `owner`
--

INSERT INTO `owner` (`username`, `emailid`, `dob`, `pasword`) VALUES
('DipeshNakrani', 'dipeshPatel12@gmail.com', '2002-01-19', 'JimmyPokar'),
('DipeshPatel', 'dpatel7440646225@gmail.com', '2002-01-19', 'jimmyPokar'),
('hetpatel', 'hetpatel134@gmail.com', '2002-12-13', 'hetpatel'),
('JayPatel', 'jaypatel1243@gmail.com', '2004-06-03', 'jaypatel'),
('jimmyPokar', 'jimmy7440646225@gmail.com', '2002-01-19', 'DipeshPatel'),
('mihirSuthar', 'mihir12345@gmail.com', '2005-02-15', 'mihirs'),
('nikitaPunjabi', 'nikitapunjabi@gmail.com', '1987-02-23', 'nikitap'),
('parthMakwana', 'parthmk1234@gmail.com', '2005-04-01', 'parthMakwana'),
('Priyanshu', 'priyanshu@gmail.com', '2004-12-10', 'helipatel');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `owner`
--
ALTER TABLE `owner`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
