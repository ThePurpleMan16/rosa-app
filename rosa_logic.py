"""Part 2 logic from 722_A1exp.ipynb: cost of a late order and best promise."""

from starter import delivery_times


def late_order_cost(costs):
  refund = costs["refund"]
  churn = costs["churn_orders"]
  margin = costs["margin"]

  total_cost = refund + (churn * margin)

  return total_cost


def best_promise(zone, time_block, promises, costs):

  best_promise = None
  best_profit = None

  late_cost = late_order_cost(costs)

  for promise in promises:
    times = delivery_times(zone, time_block, promise, seed=1)

    orders = len(times)
    late = (times > promise).sum()

    profit = orders * costs["margin"]
    late_costs = late * late_cost

    net_profit = profit - late_costs

    if best_profit is None or net_profit > best_profit:
      best_profit = net_profit
      best_promise = promise

  return best_promise, best_profit
