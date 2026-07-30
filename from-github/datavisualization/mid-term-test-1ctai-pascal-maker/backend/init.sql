CREATE TABLE IF NOT EXISTS functionalities (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(100) NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE IF NOT EXISTS robots (
  id                       SERIAL PRIMARY KEY,
  name                     VARCHAR(100) NOT NULL,
  location                 VARCHAR(200),
  ip_address               VARCHAR(45) UNIQUE,
  current_functionality_id INTEGER REFERENCES functionalities(id) ON DELETE SET NULL
);

INSERT INTO functionalities (id, name, description) VALUES
  (1, 'Dance', 'Perform a short dance routine.'),
  (2, 'Talk',  'Speak a short scripted message.'),
  (3, 'Lift',  'Move and lift light objects.'),
  (4, 'Scan',  'Scan nearby objects or markers.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO robots (id, name, location, ip_address, current_functionality_id) VALUES
  (1, 'Astra', 'Lab 1',        '10.0.1.21', 1),
  (2, 'Bolt',  'Hallway Dock', '10.0.1.22', 2),
  (3, 'Cleo',  'Workshop A',   '10.0.1.23', 3),
  (4, 'Drift', 'Charging Bay', '10.0.1.24', 4),
  (5, 'Echo',  'Storage Room', '10.0.1.25', 1)
ON CONFLICT (id) DO NOTHING;

SELECT setval('functionalities_id_seq', (SELECT MAX(id) FROM functionalities));
SELECT setval('robots_id_seq',          (SELECT MAX(id) FROM robots));
