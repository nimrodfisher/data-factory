-- Supports: "MRR fell $X in August" and the driver split (findings §Answer, §1)
-- MRR bridge per month: components sum exactly to the month-over-month change (AC2).
select
    month_end,
    sum(mrr)                                                        as mrr,
    sum(mrr_change) filter (where movement = 'new')                 as new_mrr,
    sum(mrr_change) filter (where movement = 'expansion')           as expansion_mrr,
    sum(mrr_change) filter (where movement = 'contraction')         as contraction_mrr,
    sum(mrr_change) filter (where movement = 'churn')               as churned_mrr,
    sum(mrr_change) filter (where movement <> 'opening')            as net_change
from fct_mrr_monthly
group by 1
order by 1
