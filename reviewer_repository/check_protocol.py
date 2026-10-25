"""Small regressions against actual project implementations; numpy/pandas required."""
from pathlib import Path
import sys,tempfile
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'CVFollowup'))
from time_units import unix_seconds
for unit in ['ns','us','ms','s']:
    series=pd.Series(pd.to_datetime(['2020-08-17','2020-09-14'])).dt.as_unit(unit)
    np.testing.assert_array_equal(unix_seconds(series),[1597622400,1600041600])
assert unix_seconds(pd.Series(pd.to_datetime(['2020-08-17T03:00:00+03:00'])))[0]==1597622400
for bad in [pd.Series([1600041600000]),pd.Series([pd.NaT],dtype='datetime64[ns]')]:
    try:unix_seconds(bad)
    except (TypeError,ValueError):pass
    else:raise AssertionError('Ambiguous/missing time accepted')
sys.path.insert(0,str(ROOT/'CVBenchmark'))
# common is deliberately loaded from CVBenchmark for its metric implementation.
from common import metrics
pred=np.array([list(range(12)),list(range(12))])
targets=pd.DataFrame({'article_id':[[0,2,10001],[10002]]})
value,ap=metrics(pred,targets)
np.testing.assert_allclose(ap,[(1+2/3)/3,0])
assert value['users']==2 and value['zero_retrievable_users']==1
try:metrics(np.zeros((2,12),dtype=int),targets)
except AssertionError:pass
else:raise AssertionError('Duplicate recommendations accepted')
print('PASS: time units, timezone, invalid timestamps, full-target AP denominator, inaccessible targets, duplicate top12')
