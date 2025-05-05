{{ config(materialized='table') }}
select 
	year,
	occupation_group,
	sum(number_of_people) number_of_people,
	now() as updated_at
from {{ ref('total_by_occupation_group_yearly') }}
where occupation_group = 'TIDAK/BELUM BEKERJA'
group by 1,2
order by 1,3 desc