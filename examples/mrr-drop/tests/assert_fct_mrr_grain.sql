-- AC1: one row per account per month
select month_end, account_id, count(*) as n
from fct_mrr_monthly group by all having count(*) > 1
