## Example SQLite Query

```sql
with target_cust_sales as (select
    customers.customer_id,
    customers.age,
    sales.sales_id,
    orders.order_id,
    orders.quantity,
    items.item_id,
    items.item_name
from customers 
left join sales on customers.customer_id = sales.customer_id
left join orders on sales.sales_id = orders.sales_id
left join items on orders.item_id = items.item_id
where age between 18 and 35
and orders.quantity is not null
)

select
    customer_id,
    age,
    item_name as item,
    sum(quantity) as quantity
from target_cust_sales
group by customer_id, item_name
