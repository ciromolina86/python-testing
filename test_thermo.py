import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def test1():
    from iapws.ammonia import NH3

    T = np.linspace(-50 + 273, 100 + 273, 200)  # range of temperatures in K
    P = np.linspace(0.1, 1.2, 5)  # range of pressures in MPa

    for p in P:
        gas = [NH3(T=t, P=p) for t in T]
        print(gas[0].name)
        #
        S = [s.s for s in gas]
        H = [s.h for s in gas]

        # plt.plot(S, T, 'k-')  # MPa
        plt.plot(H, T, 'g-')  # MPa
    #
    # # saturated vapor and liquid entropy lines
    #
    # svap = [s.s for s in [NH3(T=t, x=1) for t in T]]
    # hvap = [s.h for s in [NH3(T=t, x=1) for t in T]]
    #
    # sliq = [s.s for s in [NH3(T=t, x=0) for t in T]]
    # hliq = [s.h for s in [NH3(T=t, x=0) for t in T]]
    #
    # plt.plot(hvap, T, 'r-')
    # plt.plot(hliq, T, 'b-')
    #
    # # plt.xlabel('Entropy (kJ/(kg K)')
    # plt.xlabel('Enthalpy (kJ/kg)')
    #
    # plt.ylabel('Temperature (K)')

    plt.show()


def test2():
    from iapws import IAPWS95
    sat_steam = IAPWS95(P=1, x=1)  # saturated steam with known P
    sat_liquid = IAPWS95(T=370, x=0)  # saturated liquid with known T
    steam = IAPWS95(P=2.5, T=500)  # steam with known P and T
    print(sat_steam.h, sat_liquid.h, steam.h)  # calculated enthalpies

    T = np.linspace(200 + 273, 500 + 273, 200)  # range of temperatures in K

    for P in np.linspace(1, 12, 10):
        gas = [IAPWS95(T=t, P=P) for t in T]

        S = [s.s for s in gas]
        # H = [s.h for s in gas]

        plt.plot(S, T, 'k-')  # MPa
        # plt.plot(H, T, 'g-')  # MPa

        plt.show()


def test3():
    from iapws import IAPWS95

    T = np.linspace(300, 372 + 273, 200)  # range of temperatures in Kelvin
    p_amb = 0.1  # pressure in MPa

    h_p1 = [IAPWS95(T=t, P=0.1).h for t in T]
    h_p2 = [IAPWS95(T=t, P=0.2).h for t in T]
    h_gas = [IAPWS95(T=t, x=1).h for t in T]
    h_liq = [IAPWS95(T=t, x=0).h for t in T]

    plt.plot(h_p1, T)
    plt.plot(h_p2, T)
    plt.plot(h_gas, T, 'r-')
    plt.plot(h_liq, T, 'b-')
    plt.plot()

    plt.show()


def test4_th_animation():
    from iapws import IAPWS95
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.animation import FuncAnimation

    T = np.linspace(300, 372 + 273, 200)  # range of temperatures in Kelvin
    P = np.linspace(0.1, 1, 10)  # range of pressures in MPa

    fig = plt.gcf()
    ax = plt.gca()
    xdata, ydata = [], []
    ln_inst, = plt.plot([], [], 'ro')
    ln_track, = plt.plot([], [], 'r--')
    h_gas, = plt.plot([IAPWS95(T=t, x=1).h for t in T], T, label='gas')
    h_liq, = plt.plot([IAPWS95(T=t, x=0).h for t in T], T, label='liquid')

    def init():
        ax.set_xlim(0, 3500)
        ax.set_ylim(300, 700)

        return ln_inst, ln_track,

    def update(frame):
        temp = 400

        xdata.append(IAPWS95(T=temp, P=frame).h)
        ydata.append(temp)
        ln_track.set_data(xdata, ydata)
        ln_inst.set_data(IAPWS95(T=temp, P=frame).h, temp)

        # print(frame)
        return ln_inst, ln_track,

    ani = FuncAnimation(fig, update, frames=range(10000), init_func=init, blit=True, interval=1 / 40, repeat=False)
    plt.xlabel('Enthalpy (kJ/kg)')
    plt.ylabel('Temp (K)')
    plt.show()


def test4_ts_animation():
    from iapws.ammonia import NH3
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.animation import FuncAnimation

    T = np.linspace(-50 + 273, 120 + 273, 200)  # range of temperatures in Kelvin
    P = np.linspace(0.1, 1.2, 5)  # range of pressures in MPa

    fig = plt.gcf()
    ax = plt.gca()
    xdata, ydata = [], []
    ln_inst, = plt.plot([], [], 'ro')
    ln_track, = plt.plot([], [], 'r--')
    s_gas, = plt.plot([NH3(T=t, x=1).s for t in T], T, label='gas')
    s_liq, = plt.plot([NH3(T=t, x=0).s for t in T], T, label='liquid')

    def init():
        return ln_inst, ln_track,

    def update(frame):
        temp = 300

        xdata.append(NH3(T=temp, P=P[frame]).s)
        ydata.append(temp)
        ln_track.set_data(xdata, ydata)
        ln_inst.set_data(NH3(T=temp, P=P[frame]).s, temp)

        # print(frame)
        return ln_inst, ln_track,

    ani = FuncAnimation(fig, update, frames=range(5), init_func=init, blit=True, interval=1 / 1, repeat=False)
    plt.xlabel('Entropy (kJ/(kg K)')
    plt.ylabel('Temp (K)')
    plt.show()


def test5_ts_data_animation():
    from iapws.ammonia import NH3
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.animation import FuncAnimation

    df = pd.read_csv('C:\\Users\\cmolina.ITG.000\\Downloads\\Bre3_Dataset 03012022.csv')
    T1 = df.loc[:, 'REF___CT1___PV_TNHI'].values[:1000] + 273  # range of temperatures in Kelvin
    P1 = df.loc[:, 'REF___CT1___PV_PNHI'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT1 = zip(P1, T1)
    T2 = df.loc[:, 'REF___CT1___PV_TNHO'].values[:1000] + 273  # range of temperatures in Kelvin
    P2 = df.loc[:, 'REF___CT1___PV_PNHO'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT2 = zip(P2, T2)
    T3 = df.loc[:, 'REF___LI1___PV_C_TNHI'].values[:1000] + 273  # range of temperatures in Kelvin
    P3 = df.loc[:, 'REF___LI1___PV_C_PNHI'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT3 = zip(P3, T3)
    T4 = df.loc[:, 'REF___LI1___PV_C_TNHO'].values[:1000] + 273  # range of temperatures in Kelvin
    P4 = df.loc[:, 'REF___LI1___PV_C_PNHO'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT4 = zip(P4, T4)
    T5 = df.loc[:, 'REF___LI2___PV_C_TNHI'].values[:1000] + 273  # range of temperatures in Kelvin
    P5 = df.loc[:, 'REF___LI2___PV_C_PNHI'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT5 = zip(P5, T5)
    T6 = df.loc[:, 'REF___LI2___PV_C_TNHO'].values[:1000] + 273  # range of temperatures in Kelvin
    P6 = df.loc[:, 'REF___LI2___PV_C_PNHO'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT6 = zip(P6, T6)

    fig = plt.gcf()
    ax = plt.gca()
    x1data, y1data = [], []
    x2data, y2data = [], []
    ln1, = plt.plot([], [], 'bo')
    ln2, = plt.plot([], [], 'ro')
    ln3, = plt.plot([], [], 'bo')
    ln4, = plt.plot([], [], 'ro')
    ln5, = plt.plot([], [], 'bo')
    ln6, = plt.plot([], [], 'ro')
    # ln_track, = plt.plot([], [], 'r--')
    T = np.linspace(-40, 120, 200)  # range of temperatures in Celsius
    T += 273  # range of temperatures in Kelvin

    def init():
        ax.set_xlim(0, 10)
        ax.set_ylim(200, 500)
        h_gas, = plt.plot([NH3(T=t, x=1).s for t in T], T, label='gas', c='k')
        h_liq, = plt.plot([NH3(T=t, x=0).s for t in T], T, label='liquid', c='k')
        plt.xlabel('Entropy (kJ/(kg K)')
        plt.ylabel('Temp (K)')
        # plt.legend()

        return ln1, ln2, ln3, ln4, ln5, ln6,

    def update(frame):
        press1, temp1 = next(PT1)
        print('1', press1, temp1)
        press2, temp2 = next(PT2)
        print('2', press2, temp2)
        press3, temp3 = next(PT3)
        print('3', press3, temp3)
        press4, temp4 = next(PT4)
        print('4', press4, temp4)
        press5, temp5 = next(PT5)
        print('5', press5, temp5)
        press6, temp6 = next(PT6)
        print('6', press6, temp6)

        ln1.set_data(NH3(T=temp1, P=press1).s, temp1)
        ln2.set_data(NH3(T=temp2, P=press2).s, temp2)
        ln3.set_data(NH3(T=temp3, P=press3).s, temp3)
        ln4.set_data(NH3(T=temp4, P=press4).s, temp4)
        ln5.set_data(NH3(T=temp5, P=press5).s, temp5)
        ln6.set_data(NH3(T=temp6, P=press6).s, temp6)

        return ln1, ln2, ln3, ln4, ln5, ln6,

    ani = FuncAnimation(fig, update, frames=range(10000), init_func=init, blit=True, interval=1 / 100, repeat=False)
    plt.show()


def test5_th_data_animation():
    from iapws.ammonia import NH3
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.animation import FuncAnimation

    df = pd.read_csv('C:\\Users\\cmolina.ITG.000\\Downloads\\Bre3_Dataset 03012022.csv')
    T1 = df.loc[:, 'REF___CT1___PV_TNHI'].values[:1000] + 273  # range of temperatures in Kelvin
    P1 = df.loc[:, 'REF___CT1___PV_PNHI'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT1 = zip(P1, T1)
    T2 = df.loc[:, 'REF___CT1___PV_TNHO'].values[:1000] + 273  # range of temperatures in Kelvin
    P2 = df.loc[:, 'REF___CT1___PV_PNHO'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT2 = zip(P2, T2)
    T3 = df.loc[:, 'REF___LI1___PV_C_TNHI'].values[:1000] + 273  # range of temperatures in Kelvin
    P3 = df.loc[:, 'REF___LI1___PV_C_PNHI'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT3 = zip(P3, T3)
    T4 = df.loc[:, 'REF___LI1___PV_C_TNHO'].values[:1000] + 273  # range of temperatures in Kelvin
    P4 = df.loc[:, 'REF___LI1___PV_C_PNHO'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT4 = zip(P4, T4)
    T5 = df.loc[:, 'REF___LI2___PV_C_TNHI'].values[:1000] + 273  # range of temperatures in Kelvin
    P5 = df.loc[:, 'REF___LI2___PV_C_PNHI'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT5 = zip(P5, T5)
    T6 = df.loc[:, 'REF___LI2___PV_C_TNHO'].values[:1000] + 273  # range of temperatures in Kelvin
    P6 = df.loc[:, 'REF___LI2___PV_C_PNHO'].values[:1000] * 0.00689476  # range of pressures in MPa
    PT6 = zip(P6, T6)

    fig = plt.gcf()
    ax = plt.gca()
    ln1, = plt.plot([], [], 'o', label='CT1___PV_NHI')
    ln2, = plt.plot([], [], 'o', label='CT1___PV_NHO')
    ln3, = plt.plot([], [], 'o', label='LI1___PV_C_NHI')
    ln4, = plt.plot([], [], 'o', label='LI1___PV_C_NHO')
    ln5, = plt.plot([], [], 'o', label='LI2___PV_C_NHI')
    ln6, = plt.plot([], [], 'o', label='LI2___PV_C_NHO')

    T = np.linspace(-40, 100, 200)  # range of temperatures in Celsius
    T += 273  # range of temperatures in Kelvin

    h_gas, = plt.plot([NH3(T=t, x=1).h for t in T], T, label='gas')
    h_liq, = plt.plot([NH3(T=t, x=0).h for t in T], T, label='liquid')
    P = np.linspace(0.02, 0.1, 3)  # range of pressures in MPa

    for p in P:
        gas = [NH3(T=t, P=p).h for t in T]
        plt.plot(gas, T, label=f'P={p}')

    plt.xlabel('Enthalpy (kJ/kg)')
    plt.ylabel('Temp (K)')
    ax.legend()

    def init():
        ax.set_xlim(-250, 2000)
        ax.set_ylim(200, 450)

        return ln1, ln2, ln3, ln4, ln5, ln6,

    def update(frame):
        press1, temp1 = next(PT1)
        ln1.set_data(NH3(T=temp1, P=press1).h, temp1)
        press2, temp2 = next(PT2)
        ln2.set_data(NH3(T=temp2, P=press2).h, temp2)
        press3, temp3 = next(PT3)
        ln3.set_data(NH3(T=temp3, P=press3).h, temp3)
        press4, temp4 = next(PT4)
        ln4.set_data(NH3(T=temp4, P=press4).h, temp4)
        press5, temp5 = next(PT5)
        ln5.set_data(NH3(T=temp5, P=press5).h, temp5)
        press6, temp6 = next(PT6)
        ln6.set_data(NH3(T=temp6, P=press6).h, temp6)

        return ln1, ln2, ln3, ln4, ln5, ln6,

    ani = FuncAnimation(fig, update, frames=range(10000), init_func=init, blit=True, interval=1 / 100, repeat=False)
    # plt.legend()
    plt.show()


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    # inspectData()
    # test4_th_animation()
    # test4_ts_animation()
    # test5_ts_data_animation()
    test5_th_data_animation()
