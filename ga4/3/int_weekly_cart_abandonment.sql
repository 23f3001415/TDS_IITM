-- models/intermediate/int_weekly_cart_abandonment.sql

-- 1. IMPORTING OUR STAGING DATA
-- We use the {{ ref() }} function to grab our cleaned upstream data.
with carts as (
    select * from {{ ref('stg_carts') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

-- 2. FILTERING AND FORMATTING DATES
-- We only want carts from the last 30 days, and we need to group them by week.
recent_carts as (
    select
        cart_id,
        customer_id,
        -- date_trunc rounds the exact timestamp down to the start of the week
        date_trunc('week', created_at) as cart_week
    from carts
    -- Filter to only look at trends over the last 30 days
    where created_at >= current_date - interval '30 days'
),

-- 3. APPLYING BUSINESS LOGIC (THE JOIN)
-- We join our recent carts to our orders to see which carts resulted in a sale.
cart_conversion as (
    select
        c.cart_id,
        c.customer_id,
        c.cart_week,
        o.order_id,
        
        -- Business Logic: If a cart doesn't have a matching order_id, it was abandoned.
        case
            when o.order_id is null then true
            else false
        end as is_abandoned

    from recent_carts c
    -- A LEFT JOIN keeps all carts, and attaches order data ONLY if it exists
    left join orders o 
        on c.cart_id = o.cart_id
)

-- 4. FINAL OUTPUT
-- We output this cleaned, prepped data for the downstream Mart models to use.
select * from cart_conversion
