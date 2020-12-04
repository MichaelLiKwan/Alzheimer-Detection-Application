CREATE DATABASE alzheimersDetectionProject;

USE alzheimersDetectionProject;
-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 27, 2020 at 05:53 AM
-- Server version: 5.7.30
-- PHP Version: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `alzheimersDetectionProject`
--

-- --------------------------------------------------------

--
-- Table structure for table `caretakers`
--

CREATE TABLE `caretakers` (
  `caretaker_user` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `caretakers`
--

INSERT INTO `caretakers` (`caretaker_user`) VALUES
('dorime'),
('michael');

-- --------------------------------------------------------

--
-- Table structure for table `caretaker_patient`
--

CREATE TABLE `caretaker_patient` (
  `caretaker_user` varchar(255) NOT NULL,
  `patient_user` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `patient_user` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`patient_user`) VALUES
('abc'),
('ladygaga');

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
-- Table structure for table `trackers`
--

CREATE TABLE `trackers` (
  `patient_user` varchar(255) NOT NULL
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
('abc', '123', 'jin', 'loh', '012507850', 'abc.com', 'patient'),
('dorime', 'interimo', 'ameno', 'lantire', '666', 'adapare.com', 'caretaker'),
('ladygaga', 'ladygaga', 'lady', 'gaga', '12345', 'gaga.com', 'patient'),
('michael', 'angelo', 'satan', 'satan', '666', 'hellskitchen.com', 'caretaker');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `caretakers`
--
ALTER TABLE `caretakers`
  ADD PRIMARY KEY (`caretaker_user`);

--
-- Indexes for table `caretaker_patient`
--
ALTER TABLE `caretaker_patient`
  ADD PRIMARY KEY (`caretaker_user`,`patient_user`),
  ADD KEY `patient_user` (`patient_user`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`patient_user`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`caretaker_user`,`patient_user`,`report_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `caretakers`
--
ALTER TABLE `caretakers`
  ADD CONSTRAINT `caretakers_ibfk_1` FOREIGN KEY (`caretaker_user`) REFERENCES `users` (`username`);

--
-- Constraints for table `caretaker_patient`
--
ALTER TABLE `caretaker_patient`
  ADD CONSTRAINT `caretaker_patient_ibfk_1` FOREIGN KEY (`caretaker_user`) REFERENCES `caretakers` (`caretaker_user`),
  ADD CONSTRAINT `caretaker_patient_ibfk_2` FOREIGN KEY (`patient_user`) REFERENCES `patients` (`patient_user`);

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`patient_user`) REFERENCES `users` (`username`);

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`caretaker_user`,`patient_user`) REFERENCES `caretaker_patient` (`caretaker_user`, `patient_user`);