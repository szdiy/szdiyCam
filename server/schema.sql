
-- // Initialize Database //

-- meta table
CREATE TABLE IF NOT EXISTS meta (
  key text primary key,
  value text
);

INSERT INTO meta
  SELECT 'version', '1'
  where NOT EXISTS ( select * from meta where key = 'version' );

-- Device Table
CREATE TABLE IF NOT EXISTS device (
  device_id text primary key,
  device_desc text
);

INSERT INTO device
  SELECT 'default', 'SZDIY Camera default'
  where NOT EXISTS ( select * from device where device_id = 'default');

-- image table
CREATE TABLE IF NOT EXISTS screenshot (
  device_id text,
  time real,
  type text,
  image_hash text,
  image_key text,
  PRIMARY KEY ( device_id, time ),
  FOREIGN KEY ( device_id ) REFERENCES device (device_id)
    ON DELETE CASCADE ON UPDATE NO ACTION
);
