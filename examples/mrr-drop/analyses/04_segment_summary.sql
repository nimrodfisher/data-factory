-- Supports: dashboard breakdown table — MRR by segment and plan, Jul vs Aug vs Oct 2026
select
    segment,
    plan,
    sum(mrr) filter (where month_end = date '2026-07-31') as mrr_jul,
    sum(mrr) filter (where month_end = date '2026-08-31') as mrr_aug,
    sum(mrr) filter (where month_end = date '2026-10-31') as mrr_oct,
    count(*) filter (where month_end = date '2026-10-31' and mrr > 0) as accounts_oct
from fct_mrr_monthly
group by all
order by mrr_oct desc
