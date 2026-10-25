"""Critical H002 invariants: deduplication and validator syntax correction."""
import unittest
from h002_run import program_key
from features import validate_expression
import duckdb


class H002Tests(unittest.TestCase):
    def test_duplicate_explanations_names_and_spacing(self):
        first = {'rationale':'a', 'aggregates':[{'name':'f_x','keys':['customer_id'],'sql':'COUNT(*)'}],
                 'derived':[{'name':'f_y','sql':'f_x + 1'}]}
        other = {'rationale':'b', 'aggregates':[{'name':'f_z','keys':['customer_id'],'sql':'count( * )'}],
                 'derived':[{'name':'f_w','sql':'f_z+1'}]}
        self.assertEqual(program_key(first), program_key(other))
        other['derived'][0]['sql']='f_z+2'
        self.assertNotEqual(program_key(first), program_key(other))

    def test_within_group_numeric_aggregate(self):
        sql = 'mode() WITHIN GROUP (ORDER BY price)'
        validate_expression(sql, aggregate=True)
        self.assertEqual(duckdb.sql(f'SELECT {sql} FROM (VALUES (1),(1),(3)) t(price)').fetchone()[0],1)
        for bad in ['sum(price) OVER ()', 'quantile_cont(0.5) WITHIN GROUP (ORDER BY label)']:
            with self.assertRaises(ValueError):
                validate_expression(bad, aggregate=True)


if __name__ == '__main__':
    unittest.main()
