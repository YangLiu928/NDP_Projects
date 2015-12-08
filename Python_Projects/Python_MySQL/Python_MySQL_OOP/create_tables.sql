CREATE DATABASE `lr_v1`;


CREATE TABLE `lr_v1`.`lrt_legislator` (
`legislator_id` varchar(20) DEFAULT NULL,
`type_cd` varchar(20) DEFAULT NULL,
`first_name` varchar(50) DEFAULT NULL,
`last_name` varchar(50) DEFAULT NULL,
`display_name` varchar(100) DEFAULT NULL,
`web_url`  varchar(300) DEFAULT NULL,
`valid_from_dt` datetime DEFAULT NULL,
`valid_to_dt` datetime DEFAULT NULL,
`insert_dt` datetime DEFAULT NULL,
`update_dt` datetime DEFAULT NULL,
`update_by` varchar(30) DEFAULT NULL,
KEY `idx_legislator_id` (`legislator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `lr_v1`.`lrt_legislator_served` (
`legislator_id` varchar(20) DEFAULT NULL,
`branch_cd` varchar(20) DEFAULT NULL,
`state_cd` varchar(20) DEFAULT NULL,
`district_cd` varchar(20) DEFAULT NULL,
`party_cd` varchar(20) DEFAULT NULL,
`served_from_dt` datetime DEFAULT NULL,
`served_to_dt` datetime DEFAULT NULL,
`insert_dt` datetime DEFAULT NULL,
`update_dt` datetime DEFAULT NULL,
`update_by` varchar(30) DEFAULT NULL,
KEY `idx_legislator_id` (`legislator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;