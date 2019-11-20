with winning_time as (
    select min("time") "time", game, "date"
    from "time"
    group by game, "date"
    having game = :game
       and "date" = :date
)

select player."name" player,
       winning_time.game game,
       winning_time."date" "date",
       winning_time."time" "time"
from winning_time
 inner join "time" on "time"."time" = winning_time."time"
 inner join player on "time".player_id = player.id
