-- These queries are based on PostgreSQL db

-- filter data.
SELECT commodity,market,wholesale,retail,supply_volume,county FROM public.agriscrapper_data
WHERE commodity='Dry Maize' AND wholesale!=' - ' AND retail!=' - 'AND supply_volume!='';