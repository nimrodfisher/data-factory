select invoice_id from stg_billing__invoices group by 1 having count(*) > 1
