import json

with open('ticker_data.json', 'r') as f:
    ticker_data = json.load(f)

missing_fields = {}


def return_None_on_error(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            e = str(e).strip(')').strip('KeyError(')
            print(f"{func.__name__}: Key not found: {e}")
            try:
                missing_fields[e] += 1
            except KeyError:
                missing_fields[e] = 1
            return None
        except TypeError as e:  # silent type error as it is all caused by None which is already reported
            # print(f"{func.__name__}: Type error: {e}")
            return None
        except ZeroDivisionError as e:
            print(f"{func.__name__}: ZeroDivisionError: {e}")
            return None

    return inner_func


def yahoo_api_get_balance_sheet_quarterly(ticker: str):
    return ticker_data[ticker.upper()]['quarterly_balance_sheet']


def yahoo_api_get_balance_sheet_yearly(ticker: str):
    return ticker_data[ticker.upper()]['yearly_balance_sheet']


def yahoo_api_get_financials_quarterly(ticker: str):
    return ticker_data[ticker.upper()]['quarterly_financials']


def yahoo_api_get_financials_yearly(ticker: str):
    return ticker_data[ticker.upper()]['yearly_financials']


def yahoo_api_get_cashflow_quarterly(ticker: str):
    return ticker_data[ticker.upper()]['quarterly_cashflow']


def yahoo_api_get_cashflow_yearly(ticker: str):
    return ticker_data[ticker.upper()]['yearly_cashflow']


# Financials
@return_None_on_error
def EBIT(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    r = yahoo_api_get_financials_quarterly(ticker)['quarterlyEBIT'][period]['reportedValue']['raw']
    if r is None:
        return None  # TODO: alternate ways to calculate EBIT
    else:
        return r


@return_None_on_error
def EBITDA(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return EBIT(ticker, latest, period) + depreciation_and_amortization(ticker, latest, period)


@return_None_on_error
def depreciation(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_quarterly(ticker)['quarterlyReconciledDepreciation'][period]['reportedValue']['raw']


@return_None_on_error
def interest_expense(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return abs(yahoo_api_get_financials_quarterly(ticker)['quarterlyInterestExpense'][period]['reportedValue']['raw'])


@return_None_on_error
def operating_income(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_quarterly(ticker)['quarterlyOperatingIncome'][period]['reportedValue']['raw']


@return_None_on_error
def net_income(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_quarterly(ticker)['quarterlyNetIncome'][period]['reportedValue']['raw']


@return_None_on_error
def revenue(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_quarterly(ticker)['quarterlyTotalRevenue'][period]['reportedValue']['raw']


@return_None_on_error
def cost_of_revenue(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_quarterly(ticker)['quarterlyCostOfRevenue'][period]['reportedValue']['raw']


# Balance sheet
@return_None_on_error
def total_assets(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyTotalAssets'][period]['reportedValue']['raw']


@return_None_on_error
def current_assets(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyCurrentAssets'][period]['reportedValue']['raw']


@return_None_on_error
def total_liabilities(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyTotalLiabilitiesNetMinorityInterest'][period]['reportedValue']['raw']


@return_None_on_error
def current_liabilities(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyCurrentLiabilities'][period]['reportedValue']['raw']


@return_None_on_error
def total_debt(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyTotalDebt'][period]['reportedValue']['raw']


@return_None_on_error
def current_debt(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyCurrentDebt'][period]['reportedValue']['raw']


@return_None_on_error
def retained_earnings(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyRetainedEarnings'][period]['reportedValue']['raw']


@return_None_on_error
def tangible_book_value(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyTangibleBookValue'][period]['reportedValue']['raw']


@return_None_on_error
def inventory(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyInventory'][period]['reportedValue']['raw']


@return_None_on_error
def cash(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyCashAndCashEquivalents'][period]['reportedValue']['raw']


@return_None_on_error
def intangible_assets(ticker: str, latest: bool = True, period: int = -1):  # includes goodwill
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyGoodwillAndOtherIntangibleAssets'][period]['reportedValue']['raw']


@return_None_on_error
def invested_capital(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_quarterly(ticker)['quarterlyInvestedCapital'][period]['reportedValue']['raw']


# Cashflow
@return_None_on_error
def operating_cash_flow(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_cashflow_quarterly(ticker)['quarterlyOperatingCashFlow'][period]['reportedValue']['raw']


@return_None_on_error
def depreciation_and_amortization(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_cashflow_quarterly(ticker)['quarterlyDepreciationAmortizationDepletion'][period]['reportedValue']['raw']


@return_None_on_error
def altman_z_score(ticker):
    x1 = (current_assets(ticker) - current_liabilities(ticker)) / total_assets(ticker)
    x2 = retained_earnings(ticker) / total_assets(ticker)
    x3 = EBIT(ticker) / total_assets(ticker)
    x4 = tangible_book_value(ticker) / total_liabilities(ticker)
    z = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
    return z


# Ratios
# Liquidity (higher the better)
@return_None_on_error
def quick_ratio(ticker):  # key
    return (current_assets(ticker) - inventory(ticker)) / current_liabilities(ticker)


@return_None_on_error
def cash_ratio(ticker):
    return cash(ticker) / current_liabilities(ticker)


@return_None_on_error
def operating_cash_ratio(ticker):
    return operating_cash_flow(ticker) / current_liabilities(ticker)


# Coverage ratios (higher the better)
@return_None_on_error
def interest_coverage_ratio(ticker):
    return EBITDA(ticker) / interest_expense(ticker)


@return_None_on_error
def debt_service_coverage_ratio(ticker):  # key
    return operating_income(ticker) / interest_expense(ticker)


@return_None_on_error
def asset_coverage_ratio(ticker):
    return (total_assets(ticker) - intangible_assets(ticker) - (current_liabilities(ticker) - current_debt(ticker))) / total_debt(ticker)


@return_None_on_error
def cash_coverage_ratio(ticker):
    return (EBIT(ticker) + depreciation(ticker)) / interest_expense(ticker)


# Leverage ratios (lower the better)
@return_None_on_error
def total_debt_to_tangible_book_value_ratio(ticker):
    return total_debt(ticker) / tangible_book_value(ticker)


@return_None_on_error
def total_debt_to_total_assets_ratio(ticker):  # key
    return total_debt(ticker) / total_assets(ticker)


@return_None_on_error
def total_debt_to_EBITDA_ratio(ticker):  # key
    return total_debt(ticker) / EBITDA(ticker)


# Piotroski’s F-score
@return_None_on_error
def ROIC(ticker):
    return net_income(ticker) / invested_capital(ticker)


@return_None_on_error
def delta_ROIC(ticker):
    old = yahoo_api_get_financials_yearly(ticker)['annualNetIncome'][0]['reportedValue']['raw'] / \
          yahoo_api_get_balance_sheet_yearly(ticker)['annualInvestedCapital'][0]['reportedValue']['raw']
    new = yahoo_api_get_financials_yearly(ticker)['annualNetIncome'][-1]['reportedValue']['raw'] / \
          yahoo_api_get_balance_sheet_yearly(ticker)['annualInvestedCapital'][-1]['reportedValue']['raw']
    return new - old


@return_None_on_error
def delta_total_debt_to_EBITDA(ticker):
    old = yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][0]['reportedValue']['raw'] / (
            yahoo_api_get_financials_yearly(ticker)['annualEBIT'][0]['reportedValue']['raw'] +
            yahoo_api_get_cashflow_yearly(ticker)['annualDepreciationAmortizationDepletion'][0]['reportedValue']['raw'])
    new = yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][-1]['reportedValue']['raw'] / (
            yahoo_api_get_financials_yearly(ticker)['annualEBIT'][-1]['reportedValue']['raw'] +
            yahoo_api_get_cashflow_yearly(ticker)['annualDepreciationAmortizationDepletion'][0]['reportedValue']['raw'])
    return new - old


@return_None_on_error
def delta_total_debt_to_total_asset(ticker):
    old = yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][0]['reportedValue']['raw'] / \
          yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalAssets'][0]['reportedValue']['raw']
    new = yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][-1]['reportedValue']['raw'] / \
          yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalAssets'][-1]['reportedValue']['raw']
    return new - old


@return_None_on_error
def delta_quick_ratio(ticker):
    old = (yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentAssets'][0]['reportedValue']['raw'] -
           yahoo_api_get_balance_sheet_yearly(ticker)['annualInventory'][0]['reportedValue']['raw']) / \
           yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentLiabilities'][0]['reportedValue']['raw']
    new = (yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentAssets'][-1]['reportedValue']['raw'] -
           yahoo_api_get_balance_sheet_yearly(ticker)['annualInventory'][-1]['reportedValue']['raw']) / \
           yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentLiabilities'][-1]['reportedValue']['raw']
    return new - old


@return_None_on_error
def delta_gross_profit(ticker):
    old = yahoo_api_get_financials_yearly(ticker)['annualGrossProfit'][0]['reportedValue']['raw']
    new = yahoo_api_get_financials_yearly(ticker)['annualGrossProfit'][-1]['reportedValue']['raw']
    return new - old


@return_None_on_error
def delta_revenue_to_total_assets(ticker):
    old = yahoo_api_get_financials_yearly(ticker)['annualTotalRevenue'][0]['reportedValue']['raw'] / \
          yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalAssets'][0]['reportedValue']['raw']
    new = yahoo_api_get_financials_yearly(ticker)['annualTotalRevenue'][-1]['reportedValue']['raw'] / \
          yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalAssets'][-1]['reportedValue']['raw']
    return new - old


@return_None_on_error
def F_score(ticker):
    score = 0
    # Profitability
    if ROIC(ticker) > 0:
        score += 1
    if operating_cash_flow(ticker) > 0:
        score += 1
    if delta_ROIC(ticker) > 0:
        score += 1
    if operating_cash_flow(ticker) / invested_capital(ticker) > ROIC(ticker):
        score += 1
    # Leverage, Liquidity and Source of Funds
    if delta_total_debt_to_EBITDA(ticker) > 0 and delta_total_debt_to_total_asset(ticker) < 0:
        score += 1
    if delta_quick_ratio(ticker) > 0:
        score += 1
    # Operating Efficiency
    if delta_gross_profit(ticker) > 0:
        score += 1
    if delta_revenue_to_total_assets(ticker) > 0:
        score += 1
    return score
