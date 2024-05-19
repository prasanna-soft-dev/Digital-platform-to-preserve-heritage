SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";



CREATE TABLE `users` (
  `name` varchar(32) DEFAULT NULL,
  `uname` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `age` varchar(32) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `gender` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  image_path VARCHAR(255),
  post_content TEXT,
  post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

