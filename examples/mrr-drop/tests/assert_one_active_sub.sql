-- an account never has two active subscriptions at the same month-end
select month_end, account_id, count(*) as n
from int_mrr__account_months group by all having count(*) > 1
