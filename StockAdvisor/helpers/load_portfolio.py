import numpy as np
import cvxopt as opt
from cvxopt import blas, solvers
import pandas as pd


assets = pd.read_csv('data/final_asset_data.csv')

# Function to calculate optimized asset allocation and return
# Calculated based on risk tolerance


def get_asset_allocation(riskTolerance, stock_tickers):

    # ipdb.set_trace()
    assets_selected = assets.loc[:, stock_tickers].dropna()
    n_tickers = len(assets_selected.columns)
    return_vec = np.array(
        assets_selected.pct_change().dropna()).reshape(n_tickers, -1)
    returns = np.asmatrix(return_vec)
    mus = 1-riskTolerance

    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(return_vec))
    pbar = opt.matrix(np.mean(return_vec, axis=1))
    # Create constraint matrices
    G = -opt.matrix(np.eye(n_tickers))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n_tickers, 1))
    A = opt.matrix(1.0, (1, n_tickers))
    b = opt.matrix(1.0)
    # Calculate efficient frontier weights using quadratic programming
    # Silent solver results
    portfolios = solvers.qp(mus*S, -pbar, G, h, A, b,
                            options={'show_progress': False, 'glpk': {'msg_lev': 'GLP_MSG_OFF'}})
    w = portfolios['x'].T
    # print(w)
    Alloc = pd.DataFrame(data=np.array(
        portfolios['x']), index=assets_selected.columns)

    returns_final = (np.array(assets_selected) * np.array(w))
    returns_sum = np.sum(returns_final, axis=1)
    returns_sum_pd = pd.DataFrame(returns_sum, index=assets_selected.index)
    returns_sum_pd = returns_sum_pd - returns_sum_pd.iloc[0, :] + 100
    return Alloc, returns_sum_pd
