CREATE DATABASE IF NOT EXISTS RouteOptimization;
USE RouteOptimization;
CREATE TABLE IF NOT EXISTS route_benchmarks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  scenario VARCHAR(50) NOT NULL,
  route_id VARCHAR(20) NOT NULL,
  distance_km DECIMAL(8,2) NOT NULL,
  time_min DECIMAL(8,2) NOT NULL,
  penalty DECIMAL(8,2) NOT NULL,
  algorithm VARCHAR(50) NOT NULL
);
INSERT INTO route_benchmarks (scenario, route_id, distance_km, time_min, penalty, algorithm) VALUES
('Normal','R1',5,20,2,'Nearest Route'),('Normal','R2',7,15,1,'Greedy'),('Normal','R3',9,25,5,'Nearest Route'),('Normal','R4',6,22,3,'Greedy'),
('Heavy Traffic','R1',5,35,4,'Nearest Route'),('Heavy Traffic','R2',7,22,2,'Greedy'),('Heavy Traffic','R3',9,40,6,'Nearest Route'),('Heavy Traffic','R4',6,30,3,'Greedy'),
('Rainy Weather','R1',5,28,3,'Nearest Route'),('Rainy Weather','R2',7,24,2,'Greedy'),('Rainy Weather','R3',9,32,5,'Nearest Route'),('Rainy Weather','R4',6,27,2,'Greedy');
