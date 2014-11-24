#!/usr/bin/env python

import pandas as pd
from matplotlib import pyplot as plt

input_file = 'vw_bits.csv'

d = pd.read_csv( input_file )
plt.plot( d.bits, d.loss )
plt.show()
