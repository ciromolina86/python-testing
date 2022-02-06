import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

x = np.linspace(0, 10, num=11, endpoint=True)
print(x)

y = np.cos(x)
print(y)

xnew = np.linspace(0, 10, num=41, endpoint=True)
print(xnew)

f1 = interp1d(x=x, y=y, kind='linear')
f2 = interp1d(x=x, y=y, kind='nearest')
# f3 = interp1d(x=x, y=y, kind='nearest-up')
f4 = interp1d(x=x, y=y, kind='zero')
f5 = interp1d(x=x, y=y, kind='slinear')
f6 = interp1d(x=x, y=y, kind='quadratic')
f7 = interp1d(x=x, y=y, kind='cubic')
f8 = interp1d(x=x, y=y, kind='previous')
f9 = interp1d(x=x, y=y, kind='next')

plt.plot(x, y, 'o',
         # xnew, f1(xnew), '-',
         # xnew, f2(xnew), '-',
         # xnew, f3(xnew), '-',
         # xnew, f4(xnew), '-',
         # xnew, f5(xnew), '-',
         # xnew, f6(xnew), '-',
         # xnew, f7(xnew), '-',
         xnew, f8(xnew), '-',
         xnew, f9(xnew), '-',
         )

plt.legend(['data',
            # 'linear',
            # 'nearest',
            # 'nearest-up',
            # 'zero',
            # 'slinear',
            # 'quadratic',
            # 'cubic',
            'previous',
            'next'
            ],
           loc='best')

# plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
# plt.legend(['data', 'linear', 'cubic'], loc='best')

plt.show()
