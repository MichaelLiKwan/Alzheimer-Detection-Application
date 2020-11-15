CREATE DATABASE alzheimersDetectionProject;

USE alzheimersDetectionProject;

CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `phoneNumber` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `reports` (
  `caretaker_user` varchar(255) NOT NULL,
  `patient_user` varchar(255) NOT NULL,
  `report_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_name`),
  ADD KEY `caretaker_user` (`caretaker_user`),
  ADD KEY `patient_user` (`patient_user`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`caretaker_user`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`patient_user`) REFERENCES `users` (`username`);