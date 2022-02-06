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

    h_p1 = [IAPWS95(T=t, P=p_amb).h for t in T]
    h_gas = [IAPWS95(T=t, x=1).h for t in T]
    h_liq = [IAPWS95(T=t, x=0).h for t in T]

    plt.plot(h_p1, T)
    plt.plot(h_gas, T, 'r-')
    plt.plot(h_liq, T, 'b-')
    plt.plot()

    plt.show()


if __name__ == '__main__':
    # test1()
    # test2()
    test3()
