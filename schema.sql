CREATE TABLE IF NOT EXISTS cities (
  id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(60) NOT NULL UNIQUE,
  lat DOUBLE NOT NULL, lng DOUBLE NOT NULL);
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(40) NOT NULL UNIQUE, sort_order INT NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  type ENUM('lost','found') NOT NULL,
  title VARCHAR(120) NOT NULL, description TEXT NOT NULL,
  category_id INT NOT NULL, city_id INT NOT NULL,
  area VARCHAR(120) NOT NULL, lat DOUBLE NULL, lng DOUBLE NULL,
  kind VARCHAR(20) NOT NULL DEFAULT 'bag', color VARCHAR(9) NOT NULL DEFAULT '#8a6a4b',
  photo VARCHAR(255) NULL,
  status ENUM('open','claimed','recovered') NOT NULL DEFAULT 'open',
  occurred_at DATETIME NOT NULL, created_at DATETIME NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id),
  FOREIGN KEY (city_id) REFERENCES cities(id),
  INDEX idx_city_status (city_id, status, occurred_at),
  INDEX idx_type (type), INDEX idx_cat (category_id));
