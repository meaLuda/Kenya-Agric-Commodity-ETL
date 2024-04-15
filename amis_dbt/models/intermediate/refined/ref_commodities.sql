select
    id as commodity_id,
    commodity,
    case 
        when classification = '-' or classification is null then 'not applicable' 
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
    end as wholesale_amount,
    split_part(wholesale, '/', 2) as wholesale_unit,   
    case 
        when split_part(retail, '/', 1) = ' - ' then null
        else split_part(retail, '/', 1)::numeric 
    end as retail_amount,  
    split_part(retail, '/', 2) as retail_unit,
    county,
    date
    
from 
    {{ref('stg_amis__commodities')}}
     