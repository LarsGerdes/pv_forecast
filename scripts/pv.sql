-- Create view with relevant data only

CREATE VIEW pv AS
SELECT date + time AS datetime, CAST(energy_positiv_ws AS INTEGER),
       CAST(reactive_energy_l_vars AS INTEGER),
       CAST(reactive_energy_c_vars AS SMALLINT), uac_l1_v, iac_l1_a,
       udc_mppt1_v, idc_mppt1_a, udc_mppt2_v, idc_mppt2_a
FROM pv_org
WHERE energy_positiv_ws IS NOT NULL;