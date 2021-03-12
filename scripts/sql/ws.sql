drop view ws;
create view ws as
select datetime, coalesce(energy_positiv_ws * (1 - prop)
                  + COALESCE(LAG(energy_positiv_ws * prop) OVER(), 0), 0) as ws
from (
    select energy_positiv_ws, floor,
           extract('epoch' from datetime - floor) / extract('epoch'
               from interval '30 min') as prop
from (
    select datetime, energy_positiv_ws,
           to_timestamp(floor(extract('epoch' from pv.datetime) / 1800) * 1800)
               as floor
    from pv
    ) as temp
    ) as temp
right join(
    select generate_series(min(datetime::date),
        max(datetime::date) + (interval '1 d') - (interval '30 min'),
        interval '30 min') as datetime
    from pv
) as ts on (floor = datetime);
