-- Create database and table with original data

--CREATE DATABASE pv

CREATE TABLE pv_org
(
    date                   DATE,
    time                   TIME,
    inverter_no            SMALLINT,
    device_type            SMALLINT,
    periode_s              NUMERIC(4),
    energy_positiv_ws      NUMERIC(7),
    reactive_energy_l_vars NUMERIC(6),
    reactive_energy_c_vars NUMERIC(5),
    uac_l1_v               NUMERIC(4, 1),
    iac_l1_a               NUMERIC(4, 2),
    udc_mppt1_v            NUMERIC(5, 2),
    idc_mppt1_a            NUMERIC(4, 2),
    udc_mppt2_v            NUMERIC(4, 1),
    idc_mppt2_a            NUMERIC(4, 2),
    description            VARCHAR(50)
);

COPY pv_org
FROM PROGRAM 'more +2 "C:\Users\larsg\Documents\dateien\pv\data\pv.csv"'
DELIMITER ';'
CSV;