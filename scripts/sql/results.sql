-- Initilze results table
-- naive: Takes data from day before for prediction.
-- mean_daily: Predicts values with mean from day before.

drop table results;

create table results as
select datetime,
       ws as y,
       lag(ws, 48) over (order by datetime) naive,
       first_value(mean_hour) over (partition by datetime::date + (
           interval '01:00' * trunc(extract(hour from datetime))
       )) as hour,
       first_value(mean_hour_2) over (partition by datetime::date + (
           interval '02:00' * trunc(extract(hour from datetime) / 2)
       )) as hour_2,
       first_value(mean_hour_3) over (partition by datetime::date + (
           interval '03:00' * trunc(extract(hour from datetime) / 3)
       )) as hour_3,
       first_value(mean_hour_4) over (partition by datetime::date + (
           interval '04:00' * trunc(extract(hour from datetime) / 4)
       )) as hour_4,
       first_value(mean_hour_6) over (partition by datetime::date + (
           interval '06:00' * trunc(extract(hour from datetime) / 6)
       )) as hour_6,
       first_value(mean_hour_8) over (partition by datetime::date + (
           interval '08:00' * trunc(extract(hour from datetime) / 8)
       )) as hour_8,
       first_value(mean_hour_12) over (partition by datetime::date + (
           interval '12:00' * trunc(extract(hour from datetime) / 12)
       )) as hour_12,
       first_value(mean_day)
           over (partition by datetime::date) as day
from ws
left join (
    select hour,
           lag(avg, 24) over (order by hour) mean_hour
    from (
        select datetime::date
                   + (interval '01:00' * trunc(extract(hour from datetime)))
            as hour,
               avg(ws)
        from ws
        group by hour
    ) hour
) as hour on (datetime = hour)
left join (
    select hour_2,
           lag(avg, 12) over (order by hour_2) mean_hour_2
    from (
        select datetime::date
                   + (interval '02:00' * trunc(extract(hour from datetime) / 2))
            as hour_2,
               avg(ws)
        from ws
        group by hour_2
    ) hour_2
) as hour_2 on (datetime = hour_2)
left join (
    select hour_3,
           lag(avg, 8) over (order by hour_3) mean_hour_3
    from (
        select datetime::date
                   + (interval '03:00' * trunc(extract(hour from datetime) / 3))
            as hour_3,
               avg(ws)
        from ws
        group by hour_3
    ) hour_3
) as hour_3 on (datetime = hour_3)
left join (
    select hour_4,
           lag(avg, 6) over (order by hour_4) mean_hour_4
    from (
        select datetime::date
                   + (interval '04:00' * trunc(extract(hour from datetime) / 4))
            as hour_4,
               avg(ws)
        from ws
        group by hour_4
    ) hour_4
) as hour_4 on (datetime = hour_4)
left join (
    select hour_6,
           lag(avg, 4) over (order by hour_6) mean_hour_6
    from (
        select datetime::date
                   + (interval '06:00' * trunc(extract(hour from datetime) / 6))
            as hour_6,
               avg(ws)
        from ws
        group by hour_6
    ) hour_6
) as hour_6 on (datetime = hour_6)
left join (
    select hour_8,
           lag(avg, 3) over (order by hour_8) mean_hour_8
    from (
        select datetime::date
                   + (interval '08:00' * trunc(extract(hour from datetime) / 8))
            as hour_8,
               avg(ws)
        from ws
        group by hour_8
    ) hour_8
) as hour_8 on (datetime = hour_8)
left join (
    select hour_12,
           lag(avg, 2) over (order by hour_12) mean_hour_12
    from (
        select datetime::date
                   + (interval '12:00' *
                      trunc(extract(hour from datetime) / 12))
            as hour_12,
               avg(ws)
        from ws
        group by hour_12
    ) hour_12
) as hour_12 on (datetime = hour_12)
left join (
    select day,
           lag(avg) over (order by day) mean_day
    from (
        select datetime::date as day,
               avg(ws)
        from ws
        group by day
    ) day
) as day on (datetime = day);


select datetime::date + (interval '02:00' * trunc(extract(hour from datetime) / 2))
    as hour
from ws;