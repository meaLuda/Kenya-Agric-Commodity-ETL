with refined_commodities as (
    select
        id as commodity_id,
        commodity,
        supply_volume::numeric as supply_volume,
        market,
        county,
        date::date as date_created,
        case
            when
                classification = '-' or classification is null then 'Unclassified'
            else classification
        end as classification,
        case
            when grade = '-' or grade is null then 'not applicable'
            else grade
        end as grade,
        case
            when sex = '-' or sex is null then 'not applicable'
            else sex
        end as sex,
        case
            when split_part(wholesale, '/', 1) = ' - ' then null
            else split_part(wholesale, '/', 1)::numeric
        end as wholesale_price,
        case
            when split_part(wholesale, '/', 2) = ' - ' then null
            else split_part(wholesale, '/', 2)
        end as wholesale_unit,
        case
            when split_part(retail, '/', 1) = ' - ' then null
            else split_part(retail, '/', 1)::numeric
        end as retail_price,
        case
            when split_part(retail, '/', 2) = ' - ' then null
            else split_part(retail, '/', 2)
        end as retail_unit
    from
        {{ ref('stg_amis__commodities') }}
    where county != 'test'
)

select * from refined_commodities
