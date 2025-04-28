-- citizen by occupation and year
{{ config(materialized='table') }}
select 
	year,
	occupation_group,
	sum(value) as number_of_people,
    now() as updated_at
from dbt.westjava_occupation
group by 1,2
order by 1,3 desc