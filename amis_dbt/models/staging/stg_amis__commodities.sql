select
    id,
    commodity,
    classification,
    grade,
    sex,
    market,
    wholesale,
    retail,
    supply_volume,
    county,
    date
from
    {{ source('amis','agriscrapper_data') }}
