-- AC2: new + expansion - contraction - churn = change in total MRR, every month
with totals as (
    select month_end, sum(mrr) as mrr, sum(mrr_change) filter (where movement <> 'opening') as movements
    from fct_mrr_monthly group by 1
)
select month_end, mrr - lag(mrr) over (order by month_end) - movements as diff
from totals
qualify month_end > (select min(month_end) from totals) and abs(diff) > 0.01
