
#Bibliotheken
import pandas as pd
from datetime import datetime as dt
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import sys


plt.text(0.5, 0.1, "Total grid output: 100000 kWh\nTotal grid feed: 5000000kWh", size=10,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(0.6, 0.4, 0.4),
                   fc=(0.6, 0.8, 0.8),
                   )
         )

plt.show()