import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import linalg

from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.covariance import ShrunkCovariance, LedoitWolf
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

print(__doc__)

df_test = pd.read_csv('C://Users//lenovo//Desktop//my_test_aam.csv', encoding='gbk')
df_test.dropna(how='any', inplace=True)
df_test.set_index('DateTime', inplace=True)
ls_cols = df_test.columns.tolist()

for col in ls_cols:
    ret_col_name = col.split('.')[0]+'_ret'
    df_test.loc[:, ret_col_name] = df_test.loc[:, col] / df_test.loc[:, col].shift(1) - 1

ls_cols_ret = [col.split('.')[0]+'_ret' for col in ls_cols]
df_test.loc[:, ls_cols_ret].plot()


X = df_test.loc[:, ls_cols_ret]
X.dropna(inplace=True)
pca = PCA(n_components=8)
print(pca)
pca.fit(X)
print(pca.explained_variance_ratio_)
ls_explained = pca.explained_variance_ratio_
ls_explained_cum = np.cumsum(ls_explained)

reduced_x = pca.fit_transform(X)
print(pca.explained_variance_)

import seaborn as sns

sns.pairplot(X.iloc[:,:5])
sns.pairplot(X.iloc[:,-3:])

cor = X.corr()



###############################################################################
# Moving Averages
###############################################################################


def SMA(ys, w=5):
    """

    :param ys: column vector of price series with str time index
    :param w: lag number
    :return
    """
    MA = ys.rolling(window=w).apply(np.mean)

    ls_ix = ys.index.tolist()
    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(w, len(ls_ix) - 1):
        if ys.iloc[i] < MA.iloc[i] and ys.iloc[i + 1] > MA.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = 1
        elif ys.iloc[i] > MA.iloc[i] and ys.iloc[i + 1] < MA.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = -1
        else:
            signal.loc[ls_ix[i + 1]] = 0

    dict_results = {
        'SMA': MA,
        'signal': signal
    }
    return dict_results


def LWMA(ys, w=5):
    """

    :param ys: column vector of price series with str time index
    :param w: lag number
    :return
    """
    MA = ys.rolling(window=w).apply(lambda x: np.average(x, weights=np.arange(w, 0, -1)))

    ls_ix = ys.index.tolist()
    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(w, len(ls_ix) - 1):
        if ys.iloc[i] < MA.iloc[i] and ys.iloc[i + 1] > MA.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = 1
        elif ys.iloc[i] > MA.iloc[i] and ys.iloc[i + 1] < MA.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = -1
        else:
            signal.loc[ls_ix[i + 1]] = 0

    dict_results = {
        'LWMA': MA,
        'signal': signal
    }
    return dict_results


def EWMA(ys, w=5):
    exponential = 2 / (w + 1)
    MA = pd.Series(0.0, index=ys.index.tolist())
    MA[w - 1] = SMA(ys, w)['SMA'][w - 1]
    MA[:w - 1] = np.nan
    for i in range(w, len(ys)):
        MA[i] = exponential * ys[i] + (1 - exponential) * MA[i - 1]

    ls_ix = ys.index.tolist()
    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(w, len(ls_ix) - 1):
        if ys.iloc[i] < MA.iloc[i] and ys.iloc[i + 1] > MA.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = 1
        elif ys.iloc[i] > MA.iloc[i] and ys.iloc[i + 1] < MA.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = -1
        else:
            signal.loc[ls_ix[i + 1]] = 0

    dict_results = {
        'EWMA': MA,
        'signal': signal
    }

    return dict_results

###############################################################################
# Moving Averages Crossovers
###############################################################################


def MAC(ys, ws, wl, method='SMA'):
    if method == 'SMA':
        MAs = SMA(ys, ws)['SMA']
        MAl = SMA(ys, wl)['SMA']

    MAC = MAs - MAl

    ls_ix = ys.index.tolist()
    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(wl, len(ls_ix) - 1):
        if MAC.iloc[i] < 0 < MAC.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = 1
        elif MAC.iloc[i + 1] < 0 < MAC.iloc[i]:
            signal.loc[ls_ix[i + 1]] = -1
        else:
            signal.loc[ls_ix[i + 1]] = 0

    dict_results = {
        'MAC': MAC,
        'signal': signal
    }

    return dict_results


###############################################################################
# Moving Averages Convergence Divergence
###############################################################################


def MACD(ys, ws=12, wl=26, wsignal=9):
    MACD = EWMA(ys, ws)['EWMA'] - EWMA(ys, wl)['EWMA']
    y = MACD.dropna()

    signalline = EWMA(y, wsignal)['EWMA']
    SL = pd.Series(np.nan, index=ys.index.tolist())
    SL[signalline.index.tolist()] = signalline

    ls_ix = ys.index.tolist()
    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(wl, len(ls_ix) - 1):
        if MACD.iloc[i] < SL.iloc[i] and MACD.iloc[i + 1] > SL.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = 1
        elif MACD.iloc[i] > SL.iloc[i] and MACD.iloc[i + 1] < SL.iloc[i + 1]:
            signal.loc[ls_ix[i + 1]] = -1
        else:
            signal.loc[ls_ix[i + 1]] = 0

    dict_results = {
        'MACD': MACD,
        'SL': SL,
        'signal': signal
    }

    return dict_results


def MACD_adj(ys, ws=12, wl=26, wsignal=9):
    MACD = EWMA(ys, ws)['EWMA'] - EWMA(ys, wl)['EWMA']
    y = MACD.dropna()

    signalline = EWMA(y, wsignal)['EWMA']
    SL = pd.Series(np.nan, index=ys.index.tolist())
    SL[signalline.index.tolist()] = signalline

    ls_ix = ys.index.tolist()
    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(wl, len(ls_ix) - 1):
        if SL.iloc[i + 1] > 0 and \
                (MACD.iloc[i] < SL.iloc[i] and MACD.iloc[i + 1] > SL.iloc[i + 1]):
            signal.loc[ls_ix[i + 1]] = 1
        elif SL.iloc[i + 1] < 0 and \
                (MACD.iloc[i] > SL.iloc[i] and MACD.iloc[i + 1] < SL.iloc[i + 1]):
            signal.loc[ls_ix[i + 1]] = -1
        else:
            signal.loc[ls_ix[i + 1]] = 0

    MACD = MACD.apply(lambda x: round(x, 2))
    SL = SL.apply(lambda x: round(x, 2))

    HIST = MACD - SL

    dict_results = {
        'MACD': MACD,
        'SL': SL,
        'HIST': HIST,
        'signal': signal
    }

    return dict_results


###############################################################################
# Relative Strength Index
###############################################################################


def RSI(ys, w=14, ul=70, dl=30):
    l = len(ys)
    ls_ix = ys.index.tolist()

    ys_chg_p = (ys.diff(1)).apply(lambda x: max(x, 0))
    ys_chg_n = (ys.diff(1)).apply(lambda x: np.abs(min(x, 0)))

    RS = pd.Series(data=np.nan, index=ys.index.tolist())
    RSI = pd.Series(data=np.nan, index=ys.index.tolist())
    for t in range(w, l):
        # print(t)
        if ys_chg_n.iloc[t - w + 1:t + 1].sum() == 0:
            RS.iloc[t] = np.nan
            RSI.iloc[t] = 100
        else:
            RS.iloc[t] = ys_chg_p.iloc[t - w + 1:t + 1].sum() / ys_chg_n.iloc[t - w + 1:t + 1].sum()
            RSI.iloc[t] = 100 - 100 / (1 + RS.iloc[t])

    signal = pd.Series(data=np.nan, index=ls_ix)

    for i in range(w, l - 1):
        if RSI[i] < dl < RSI[i + 1]:
            signal[i + 1] = 1
        elif RSI[i + 1] < ul < RSI[i]:
            signal[i + 1] = -1
        else:
            signal[i + 1] = 0

    dict_results = {
        'RSI': RSI,
        'signal': signal
    }

    return dict_results


def VIX_calc(T, F, K0, Ki, delta_Ki, R):



    return vix


# Equity Tactical Asset Allocation

df_X_test1 = df_test.loc[:'2010-01-01', :]
df_X_test2 = df_test.loc['2019-01-01':, :]
df_X = df_test.loc['2010-01-01':'2019-01-01', :]

# Part One Technical Analysis

df_MACD = pd.DataFrame()
for stock_index in df_X.columns.tolist()[:3]:
    print(stock_index)
    df_MACD.loc[:, stock_index + '_MACD_signal'] = MACD(df_X.loc[:, stock_index])['signal']

df_RSI = pd.DataFrame()
for stock_index in df_X.columns.tolist()[:3]:
    print(stock_index)
    df_RSI.loc[:, stock_index + '_RSI_signal'] = RSI(df_X.loc[:, stock_index])['signal']

# Part Two Sentimental Analysis

# Part Three Liquidity Factor

# Part Four Economic Momentum

# Part Five Company Earning Factor

# Part Six Equity Valuation

# Part Seven External Factors

