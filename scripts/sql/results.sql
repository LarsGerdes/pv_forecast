-- Create results table with seasonal naive prediction
-- Takes data from day before for prediction.

drop table results;

create table results as
    select datetime, ws as y, lag(ws, 48) over () naive from ws;