{
  "aggregates": [
    {
      "keys": [
        "customer_id"
      ],
      "name": "f_count",
      "sql": "count ( * )"
    },
    {
      "keys": [
        "customer_id",
        "product_type_no"
      ],
      "name": "f_price",
      "sql": "avg ( price )"
    }
  ],
  "derived": [
    {
      "name": "f_log_count",
      "sql": "ln ( 1 + coalesce ( f_count , 0 ) )"
    },
    {
      "name": "f_interaction",
      "sql": "f_log_count * raw_u_age"
    }
  ]
}
