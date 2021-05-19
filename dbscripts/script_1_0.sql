CREATE database vaccine_slot_tracker;

CREATE TABLE `vaccine_slot` (
    `center_id` INT NOT NULL,
    `pincode` INT NOT NULL,
    `age_limit` INT NOT NULL,
    `vaccine` VARCHAR(75),
    `state_name` VARCHAR(75),
    `district_name` VARCHAR(100),
    `center_name` VARCHAR(256),
    `slot_date` DATE,
    `available_capacity_dose1` INT DEFAULT 0,
    `available_capacity_dose2` INT DEFAULT 0,
    `timestamp_update_dose1` TIMESTAMP DEFAULT '1990-01-01 01:01:01',
    `timestamp_update_dose2` TIMESTAMP DEFAULT '1990-01-01 01:01:01' ,
    PRIMARY KEY (center_id, age_limit, vaccine, slot_date)
);

CREATE USER 'tracker'@'%' IDENTIFIED BY 'password123';

GRANT ALL PRIVILEGES ON vaccine_slot_tracker.vaccine_slot TO 'tracker'@'%';
