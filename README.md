# Shifts ETL

## Getting Started

Initialize & start shifts API and target Postgres database in the background
with

```bash
$ docker-compose up -d
```

### Calculated Shift KPIs



| Name                                  | Description                                                            |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `mean_break_length_in_minutes`        | Mean shift break time in minutes (`breaks.start` and `breaks.finish`). |
| `mean_shift_cost`                     | Mean shift cost (`shifts.cost`).                                       |
| `max_allowance_cost_14d`              | Max allowance cost in the last 14 days (`allowances.cost`).            |
| `max_break_free_shift_period_in_days` | Longest period in days when consecutive shifts did not have breaks.    |
| `min_shift_length_in_hours`           | Shortest shift duration (`shift.start` and `shift.finish`).            |
| `total_number_of_paid_breaks`         | Total number of paid shift breaks (`breaks.is_paid`).                  |

