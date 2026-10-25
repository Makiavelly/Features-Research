import json
import subprocess
import torch
import numpy
import pandas
import sklearn
import matplotlib
print(json.dumps(dict(torch=torch.__version__,cuda=torch.cuda.is_available(),numpy=numpy.__version__,pandas=pandas.__version__,sklearn=sklearn.__version__,matplotlib=matplotlib.__version__)),flush=True)
subprocess.run(['ps','-eo','pid,etime,comm'],check=True)
