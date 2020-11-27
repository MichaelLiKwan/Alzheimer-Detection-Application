-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 27, 2020 at 04:05 AM
-- Server version: 5.7.30
-- PHP Version: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `alzheimersDetectionProject`
--

CREATE DATABASE alzheimersDetectionProject;

USE alzheimersDetectionProject;

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `caretaker_user` varchar(255) NOT NULL,
  `patient_user` varchar(255) NOT NULL,
  `report_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `phoneNumber` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `password`, `firstName`, `lastName`, `phoneNumber`, `email`, `role`) VALUES
('abc', '123', 'jin', 'wen', '666', 'email.com', 'patient'),
('dorime', 'interimo', 'ameno', 'lantire', '0125078505', 'era.com', 'caretaker');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`caretaker_user`,`patient_user`,`report_name`),
  ADD KEY `caretaker_user` (`caretaker_user`),
  ADD KEY `patient_user` (`patient_user`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`caretaker_user`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`patient_user`) REFERENCES `users` (`username`);