-- test / internal accounts never reach the marts
select f.account_id from fct_mrr_monthly f join stg_billing__accounts a using (account_id) where a.is_test
