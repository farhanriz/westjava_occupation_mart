with source as (
    SELECT 
        *
    FROM {{ ref('total_yearly') }}
)
SELECT 
    year,
    SUM(number_of_people) 
FROM source
GROUP BY year
HAVING SUM(number_of_people) < 0