DROP DATABASE IF EXISTS `mini_aspire_app`;
CREATE DATABASE `mini_aspire_app`;

use `mini_aspire_app`;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `customer_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50),
  `date_of_birth` varchar(250) NOT NULL,
  `email_id` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `created_datetime` datetime NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB COMMENT="This table contains the details of the customer and is used to authenticate the customer";

--
-- Table structure for table `loan_application`
--

DROP TABLE IF EXISTS `loan_application`;
CREATE TABLE `loan_application` (
  `application_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `customer_id` bigint unsigned NOT NULL,
  `requested_loan_duration` int NOT NULL,
  `requested_loan_amount` decimal(13,2) NOT NULL,
  `application_status` enum('PENDING', 'APPROVED', 'DECLINED') DEFAULT NULL,
  `created_datetime` datetime NOT NULL,
  PRIMARY KEY (`application_id`),
  KEY `idx_app_timestamp` (`created_datetime`),
  KEY `idx_app_custid` (`customer_id`),
  CONSTRAINT `fk_app_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB COMMENT="This table contains the details of the loan applications submitted for the customer.";

--
-- Table structure for table `loan_details`
--

DROP TABLE IF EXISTS `loan_details`;
CREATE TABLE `loan_details` (
  `loan_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `application_id` bigint unsigned NOT NULL,
  `customer_id` bigint unsigned NOT NULL,
  `loan_duration` int NOT NULL,
  `loan_amount` decimal(13,2) NOT NULL,
  `repayment_frequency` enum('weekly', 'monthly') NOT NULL,
  `loan_status` enum('ACTIVE', 'CLOSED-OFF') DEFAULT NULL,
  `created_datetime` datetime NOT NULL,
  PRIMARY KEY (`loan_id`),
  KEY `idx_loan_status` (`loan_status`),
  KEY `idx_loan_custid` (`customer_id`),
  KEY `idx_loan_appid` (`application_id`),
  CONSTRAINT `fk_loan_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `fk_loan_application_id` FOREIGN KEY (`application_id`) REFERENCES `loan_application` (`application_id`)
) ENGINE=InnoDB COMMENT="This table contains the details of the loans approved for the customer.";

--
-- Table structure for table `repayment_calendar`
--
DROP TABLE IF EXISTS `repayment_calendar`;
CREATE TABLE `repayment_calendar` (
  `repayment_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `loan_id` bigint unsigned NOT NULL,
  `cycle` int(11) NOT NULL,
  `pay_date` date NOT NULL,
  `amount_due` decimal(13,2) NOT NULL DEFAULT '0.00',
  `amount_paid` decimal(13,2) NOT NULL DEFAULT '0.00',
  `is_record_valid` tinyint(4) NOT NULL DEFAULT '1',
  `repayment_status` enum('PENDING', 'COMPLETED') DEFAULT NULL,
  `created_datetime` datetime NOT NULL,
  PRIMARY KEY (`repayment_id`),
  KEY `idx_repay_timestamp` (`created_datetime`),
  CONSTRAINT `fk_repy_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loan_details` (`loan_id`)
) ENGINE=InnoDB COMMENT="This table contains the repayment schedule of the loans approved for the customer.";

