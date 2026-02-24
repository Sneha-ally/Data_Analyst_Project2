--- total number of tickets
select count(*) as total_tickets
From customer_support_tickets;
--- tickets by channel
select ticket_channel,count(*) AS ticket_count
from customer_support_tickets
group by ticket_channel
order by ticket_count desc;

----- Average resolution time (hours) by ticket priority
select ticket_priority,AVG(resolution_time_hours) as avg_satisfaction
from customer_support_tickets
group by ticket_priority
order by avg_satisfaction DESC;

---Closure rate percentage
select 
 ROUND(avg(cast(is_closed AS float)) * 100,2) AS Closure_rate_percentage
 from customer_support_tickets;

 -- SLA breach calculation
SELECT 
    ticket_priority,
    COUNT(*) AS total_tickets,
    SUM(CASE 
            WHEN resolution_time_hours >
                CASE 
                    WHEN ticket_priority = 'Critical' THEN 24
                    WHEN ticket_priority = 'High' THEN 48
                    WHEN ticket_priority = 'Medium' THEN 72
                    ELSE 96
                END
            THEN 1 ELSE 0 
        END) AS breached_tickets,
        
    ROUND(
        SUM(CASE 
                WHEN resolution_time_hours >
                    CASE 
                        WHEN ticket_priority = 'Critical' THEN 24
                        WHEN ticket_priority = 'High' THEN 48
                        WHEN ticket_priority = 'Medium' THEN 72
                        ELSE 96
                    END
                THEN 1 ELSE 0 
            END
        ) * 100.0 / COUNT(*), 2
    ) AS breach_percentage

FROM customer_support_tickets
GROUP BY ticket_priority
ORDER BY breach_percentage DESC;

--- products with highest tickets
select product_purchased,COUNT(*) as ticket_count
from customer_support_tickets
group by product_purchased
order by ticket_count desc;

---Check if longer resolution reduces satisfaction
select resolution_time_hours,AVG(customer_satisfaction_rating) as avg_satisfaction
from customer_support_tickets
group by resolution_time_hours
order by resolution_time_hours;