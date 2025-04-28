{{ config(materialized='view') }}
select 
	year,
	sum(number_of_people) number_of_people
from {{ ref('total_by_occupation_group_yearly') }}
group by 1
order by 1
