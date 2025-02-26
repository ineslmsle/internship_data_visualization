
CREATE DATABASE IF NOT EXISTS sensors;

CREATE TABLE IF NOT EXISTS `sensors_types` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ;

CREATE TABLE IF NOT EXISTS `sensors_area` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ;

CREATE TABLE IF NOT EXISTS `sensors_room` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ;

CREATE TABLE IF NOT EXISTS `sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `type` int NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `serial_number` VARCHAR(50) UNIQUE,
    `number` int,
    `area` int NOT NULL,
    `room` int NOT NULL,
    `longitude` decimal(10,2),
    `latitude` decimal(10,2),
    `altitude` decimal(10,2),
    UNIQUE (`longitude`, `latitude`, `altitude`),
    UNIQUE(`type`, `name`),
    FOREIGN KEY (`type`) REFERENCES `sensors_types`(`id`),
    FOREIGN KEY (`area`) REFERENCES `sensors_area`(`id`),
    FOREIGN KEY (`room`) REFERENCES `sensors_room`(`id`)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `WIA_sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `temperature` decimal(10,2),
    `humidity` decimal(10,2),   
    `light` decimal(10,2),
    `motion` decimal(10,2),
    `soundAvg` decimal(10,2),
    `soundPeak` decimal(10,2),
    `time_recorded` datetime NOT NULL,
    `sensor_id` int NOT NULL,
    UNIQUE (`time_recorded`, `sensor_id`),
    FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `WIA_avg` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `area_id` int,
    `room_id` int,
    `date_begin` datetime NOT NULL,
    `date_end` datetime NOT NULL,
    `temperature` decimal(10,2),
    `humidity` decimal(10,2),   
    `light` decimal(10,2),
    `motion` decimal(10,2),
    `soundAvg` decimal(10,2),
    `soundPeak` decimal(10,2),
    UNIQUE (`date_begin`,`date_end`, `area_id`, `room_id`),
    FOREIGN KEY (`area_id`) REFERENCES `sensors_area`(`id`),
    FOREIGN KEY (`room_id`) REFERENCES `sensors_room`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `HiData_sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `occupancy` decimal(10,2) NOT NULL,
    `light` decimal(10,2) NOT NULL,
    `noise` decimal(10,2) NOT NULL,
    `time_recorded` datetime NOT NULL,
    `sensor_id` int NOT NULL,
    UNIQUE (`time_recorded`, `sensor_id`),
    FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `HiData_avg` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `area_id` int NOT NULL,
    `date_begin` datetime NOT NULL,
    `date_end` datetime NOT NULL,
    `occupancy` decimal(10,2),
    `light` decimal(10,2),
    `noise` decimal(10,2),
    UNIQUE (`date_begin`,`date_end`, `area_id`),
    FOREIGN KEY (`area_id`) REFERENCES `sensors_area`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `CIVIC_class` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `CIVIC_sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `date_begin` datetime NOT NULL,
    `date_end` datetime NOT NULL,
    `zone` int NOT NULL,
    `asset` int NOT NULL,
    `class` int NOT NULL,
    `speed` decimal(10,2) NOT NULL,
    `headway` decimal(10,2) NOT NULL,
    `occupancy` decimal(10,2) NOT NULL,
    `gap` decimal(10,2) NOT NULL,
    `volume` decimal(10,2) NOT NULL,
    `sensor_id` int NOT NULL,
    UNIQUE (`date_begin`, `date_end`, `sensor_id`),
    FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`),
    FOREIGN KEY (`class`) REFERENCES `CIVIC_class`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `4DA_WIA_types` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `4DA_WIA_sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `type` int NOT NULL,
    `value` decimal(10,2),   
    `time_recorded` datetime NOT NULL,
    `sensor_id` int NOT NULL,
    UNIQUE (`time_recorded`, `sensor_id`, `type`),
    FOREIGN KEY (`type`) REFERENCES `4DA_WIA_types`(`id`),
    FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `4DA_BBB_types` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `4DA_BBB_sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `type` int NOT NULL,
    `value` decimal(10,2),   
    `time_recorded` datetime NOT NULL,
    `sensor_id` int NOT NULL,
    UNIQUE (`time_recorded`, `sensor_id`, `type`),
    FOREIGN KEY (`type`) REFERENCES `4DA_BBB_types`(`id`),
    FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `4DA_CIVIC_types` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `4DA_CIVIC_sensor` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `type` int NOT NULL,
    `value` decimal(10,2),   
    `time_recorded` datetime NOT NULL,
    `sensor_id` int NOT NULL,
    UNIQUE (`time_recorded`, `sensor_id`, `type`),
    FOREIGN KEY (`type`) REFERENCES `4DA_CIVIC_types`(`id`),
    FOREIGN KEY (`sensor_id`) REFERENCES `sensor`(`id`)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `CIVIC_count` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `zone` int NOT NULL,
    `date_begin` datetime NOT NULL,
    `date_end` datetime NOT NULL,
    `pedestrian` decimal(10,2),   
    `bike` decimal(10,2),
    `long_truck` decimal(10,2),
    `motorcycle` decimal(10,2),
    `short_truck` decimal(10,2),
    `car` decimal(10,2),
    `undefined` decimal(10,2),
    UNIQUE (`zone`, `date_begin`, `date_end`)

) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `TFI_bus_stop` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `bus_stop_id` int NOT NULL,
    `route` VARCHAR(20) NOT NULL,
    `headsign` VARCHAR(20) NOT NULL,
    `scheduled_arrival` datetime NOT NULL

) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Firebase_types` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Firebase_people_count` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `type` int NOT NULL,
    `time` datetime NOT NULL,
    `count` int NOT NULL,
    FOREIGN KEY (`type`) REFERENCES `Firebase_types`(`id`),
    UNIQUE (`type`, `time`)

) ENGINE=InnoDB;