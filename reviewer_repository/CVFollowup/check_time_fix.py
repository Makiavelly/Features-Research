"""Regressions for ns/us/ms/s datetime inputs and the real graph-cutoff mismatch."""
import numpy as np
import pandas as pd
from common import ROOT,REPORT,read,write
from time_units import unix_seconds
from gnn_timefix import build

checks=[]
for unit in ['ns','us','ms','s']:
    values=pd.Series(pd.to_datetime(['2020-08-17','2020-09-14'])).dt.as_unit(unit)
    np.testing.assert_array_equal(unix_seconds(values),[1597622400,1600041600])
    checks.append(f'{unit}_to_seconds')
aware=pd.Series(pd.to_datetime(['2020-08-17T03:00:00+03:00']))
assert unix_seconds(aware)[0]==1597622400;checks.append('timezone_utc')
for invalid in [pd.Series([1597622400000]),pd.Series([pd.NaT],dtype='datetime64[ns]')]:
    try:unix_seconds(invalid)
    except (TypeError,ValueError):pass
    else:raise AssertionError('Ambiguous/missing time accepted')
checks.append('integer_units_and_NaT_rejected')
audit=read(REPORT/'graph_time_audit.json')
rows=[r for r in audit['rows'] if r['case']!='small' and r['split'] in ['val','test']]
assert len(rows)==6
assert all(r['visible_transactions_with_current_input']==0 and r['visible_transactions_with_correct_input']>0 for r in rows)
checks.append('all_six_real_val_test_splits_have_unit_bug')
for fold in range(3):build(fold,False);build(fold,True)
write(REPORT/'graph_time_fix_verification.json',{'passed':True,'checks':checks,'model_fits':0,
      'root_cause':'val/test datetime64[ms] divided by1e9 instead of converting to nanoseconds first; cutoff about1600 instead of1.6e9 seconds'})
print('TIME FIX:',len(checks),'checks passed; all6 real val/test splits affected')
