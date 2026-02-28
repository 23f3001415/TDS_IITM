# Question 4: dbt - Operations Performance Mart

## Final Answer (submit this SQL)
```sql
{{ config(
    materialized='table',
    tags=['ops', 'returns', 'mart', 'daily'],
    meta={
      'owner': 'orbit_ops_analytics',
      'freshness': {'expected_update': 'daily', 'sla_hours': 24}
    }
) }}

with returns as (
    select
        return_id,
        shipment_id,
        order_id,
        customer_id,
        return_created_at,
        return_received_at,
        return_completed_at,
        return_status,
        return_reason
    from {{ ref('stg_returns') }}
),

shipments as (
    select
        shipment_id,
        shipped_at,
        delivered_at,
        fulfillment_center,
        carrier
    from {{ ref('stg_shipments') }}
),

returns_enriched as (
    select
        r.return_id,
        coalesce(r.shipment_id, s.shipment_id) as shipment_id,
        r.order_id,
        r.customer_id,
        coalesce(r.return_received_at, r.return_created_at) as return_event_ts,
        r.return_completed_at,
        coalesce(lower(r.return_status), 'unknown') as return_status,
        coalesce(r.return_reason, 'unspecified') as return_reason,
        coalesce(s.fulfillment_center, 'unknown') as fulfillment_center,
        coalesce(s.carrier, 'unknown') as carrier
    from returns r
    left join shipments s
        on r.shipment_id = s.shipment_id
),

last_45_days as (
    select
        *
    from returns_enriched
    where cast(return_event_ts as date) >= cast({{ dbt.dateadd('day', -45, 'current_date') }} as date)
),

processing_metrics as (
    select
        {{ dbt.date_trunc('day', 'return_event_ts') }} as metric_date,
        return_id,
        fulfillment_center,
        carrier,
        return_reason,
        return_status,
        coalesce(
            {{ dbt.datediff('return_event_ts', 'return_completed_at', 'hour') }},
            0
        ) as processing_hours
    from last_45_days
),

daily_rollup as (
    select
        metric_date,
        count(distinct return_id) as returns_count,
        avg(processing_hours) as avg_processing_hours,
        sum(case when return_status in ('approved', 'completed', 'closed') then 1 else 0 end) as completed_returns,
        sum(case when return_status in ('initiated', 'pending', 'in_transit') then 1 else 0 end) as open_returns
    from processing_metrics
    group by 1
)

select
    metric_date,
    coalesce(returns_count, 0) as returns_count,
    coalesce(avg_processing_hours, 0) as avg_processing_hours,
    coalesce(completed_returns, 0) as completed_returns,
    coalesce(open_returns, 0) as open_returns
from daily_rollup
order by metric_date
```

## ELI15 Step-by-Step (for a complete novice)
1. `{{ config(...) }}` sets how dbt builds this mart table and adds freshness metadata.
2. Pull return data from `stg_returns` and shipment context from `stg_shipments` using `{{ ref() }}`.
3. Join them to create one enriched returns dataset.
4. Use `coalesce(...)` so missing values become safe defaults.
5. Keep only records from the last 45 days.
6. Convert timestamps to daily buckets (`metric_date`).
7. Compute processing time in hours for each return.
8. Aggregate at daily grain and calculate:
   - total returns
   - average processing hours
   - completed vs open returns
9. Output BI-ready daily columns, ordered by date.
