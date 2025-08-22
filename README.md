## Example SQLite Query

```sql
WITH target_cust_sales AS (
    SELECT
        customers.customer_id,
        customers.age,
        sales.sales_id,
        orders.order_id,
        orders.quantity,
        items.item_id,
        items.item_name
    FROM customers 
    LEFT JOIN sales ON customers.customer_id = sales.customer_id
    LEFT JOIN orders ON sales.sales_id = orders.sales_id
    LEFT JOIN items ON orders.item_id = items.item_id
    WHERE age BETWEEN 18 AND 35
      AND orders.quantity IS NOT NULL
)

SELECT
    customer_id,
    age,
    item_name AS item,
    SUM(quantity) AS quantity
FROM target_cust_sales
GROUP BY customer_id, item_name;
