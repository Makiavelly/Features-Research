{
  "aggregates": [
    {
      "column": "days_ago",
      "keys": [
        "customer_id"
      ],
      "name": "f_recency",
      "op": "min",
      "window": 180
    },
    {
      "column": "*",
      "keys": [
        "customer_id"
      ],
      "name": "f_recent",
      "op": "count",
      "window": 7
    }
  ],
  "derived": [
    {
      "expr": {
        "args": [
          {
            "ref": "f_recent"
          },
          {
            "args": [
              {
                "ref": "f_recency"
              },
              1
            ],
            "op": "add"
          }
        ],
        "op": "divide"
      },
      "name": "f_rate"
    },
    {
      "expr": {
        "args": [
          {
            "ref": "f_rate"
          }
        ],
        "op": "log1p"
      },
      "name": "f_log_rate"
    }
  ]
}
