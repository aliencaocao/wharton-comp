import json

with open('ticker_data.json', 'r') as f:
    ticker_data = json.load(f)

missing_fields = {}


def return_None_on_error(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            if func.__name__ == 'inner_func':
                raise e
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


def try_get_latest_ratio(func):
    def inner_func(*args, **kwargs):
        period = kwargs['period']
        if period < 0: period += 4  # convert from negative indexing to positive
        for i in range(3, -1, -1):
            kwargs['period'] = i
            r = func(*args, **kwargs)
            if r is not None:
                break
            else:
                print(f'No data for {func.__name__} for period {i}')
        else:  # loop until exhausted
            r = None
        return r

    return inner_func


def yahoo_api_get_balance_sheet_quarterly(ticker: str):
    if ticker == 'TATAMOTORS.BO':
        r = yahoo_api_get_balance_sheet_yearly(ticker)
        new_r = {}
        for k, v in r.items():
            new_r[k.replace('annual', 'quarterly')] = v
        return new_r
    return ticker_data[ticker.upper()]['quarterly_balance_sheet']


def yahoo_api_get_balance_sheet_yearly(ticker: str):
    return ticker_data[ticker.upper()]['yearly_balance_sheet']


def yahoo_api_get_financials_quarterly(ticker: str):
    if ticker == 'TATAMOTORS.BO':
        r = yahoo_api_get_financials_yearly(ticker)
        new_r = {}
        for k, v in r.items():
            new_r[k.replace('annual', 'quarterly')] = v
        return new_r

    return ticker_data[ticker.upper()]['quarterly_financials']


def yahoo_api_get_financials_yearly(ticker: str):
    return ticker_data[ticker.upper()]['yearly_financials']


def yahoo_api_get_cashflow_quarterly(ticker: str):
    if ticker == 'TATAMOTORS.BO':
        r = yahoo_api_get_cashflow_yearly(ticker)
        new_r = {}
        for k, v in r.items():
            new_r[k.replace('annual', 'quarterly')] = v
        return new_r
    return ticker_data[ticker.upper()]['quarterly_cashflow']


def yahoo_api_get_cashflow_yearly(ticker: str):
    return ticker_data[ticker.upper()]['yearly_cashflow']


# Financials
def EBIT(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualEBIT'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualPretaxIncome'][period]['reportedValue']['raw'] + \
               yahoo_api_get_financials_yearly(ticker)['annualNetInterestIncome'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    return None


def EBITDA(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualEBITDA'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return EBIT(ticker, latest, period) + depreciation_and_amortization(ticker, latest, period)
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualNormalizedEBITDA'][period]['reportedValue']['raw'] + \
               yahoo_api_get_financials_yearly(ticker)['annualTotalUnusualItems'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    return None


@return_None_on_error
def depreciation(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualReconciledDepreciation'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualDepreciationAmortizationDepletion'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    return None


def interest_expense(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return abs(yahoo_api_get_financials_yearly(ticker)['annualInterestExpense'][period]['reportedValue']['raw'])
    except KeyError as e:
        print(e)
    try:
        return abs(yahoo_api_get_financials_yearly(ticker)['annualInterestExpenseNonOperating'][period]['reportedValue']['raw'])
    except KeyError as e:
        print(e)
    try:
        return abs(yahoo_api_get_financials_yearly(ticker)['annualTotalOtherFinanceCost'][period]['reportedValue']['raw'])
    except KeyError as e:
        print(e)
    return None


@return_None_on_error
def operating_income(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_yearly(ticker)['annualOperatingIncome'][period]['reportedValue']['raw']


@return_None_on_error
def net_income(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_yearly(ticker)['annualNetIncome'][period]['reportedValue']['raw']


@return_None_on_error
def revenue(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_yearly(ticker)['annualTotalRevenue'][period]['reportedValue']['raw']


@return_None_on_error
def cost_of_revenue(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_financials_yearly(ticker)['annualCostOfRevenue'][period]['reportedValue']['raw']


# Balance sheet
@return_None_on_error
def total_assets(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalAssets'][period]['reportedValue']['raw']


@return_None_on_error
def current_assets(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentAssets'][period]['reportedValue']['raw']


@return_None_on_error
def total_liabilities(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalLiabilitiesNetMinorityInterest'][period]['reportedValue']['raw']


@return_None_on_error
def current_liabilities(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentLiabilities'][period]['reportedValue']['raw']


@return_None_on_error
def total_debt(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][period]['reportedValue']['raw']


@return_None_on_error
def current_debt(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentDebt'][period]['reportedValue']['raw']


@return_None_on_error
def retained_earnings(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualRetainedEarnings'][period]['reportedValue']['raw']


@return_None_on_error
def tangible_book_value(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualTangibleBookValue'][period]['reportedValue']['raw']


@return_None_on_error
def inventory(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualInventory'][period]['reportedValue']['raw']


@return_None_on_error
def cash(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    if ticker == 'TU':
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualCashCashEquivalentsAndShortTermInvestments'][period]['reportedValue']['raw']
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualCashAndCashEquivalents'][period]['reportedValue']['raw']


@return_None_on_error
def intangible_assets(ticker: str, latest: bool = True, period: int = -1):  # includes goodwill
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualGoodwillAndOtherIntangibleAssets'][period]['reportedValue']['raw']


@return_None_on_error
def invested_capital(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualInvestedCapital'][period]['reportedValue']['raw']


# Cashflow
def operating_cash_flow(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualOperatingCashFlow'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualCashFlowsfromusedinOperatingActivitiesDirect'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    return None


def depreciation_and_amortization(ticker: str, latest: bool = True, period: int = -1):  # TODO: try D + A separate
    if latest: period = -1
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualDepreciationAmortizationDepletion'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualReconciledDepreciation'][period]['reportedValue']['raw'] + \
               yahoo_api_get_cashflow_yearly(ticker)['annualAmortizationOfSecurities'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualReconciledDepreciation'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualAmortizationOfSecurities'][period]['reportedValue']['raw']
    except KeyError as e:
        print(e)
    return None


@return_None_on_error
@try_get_latest_ratio
def altman_z_score(ticker, latest: bool = True, period: int = -1):
    x1 = (current_assets(ticker, latest, period) - current_liabilities(ticker, latest, period)) / total_assets(ticker, latest, period)
    x2 = retained_earnings(ticker, latest, period) / total_assets(ticker, latest, period)
    x3 = EBIT(ticker, latest, period) / total_assets(ticker, latest, period)
    x4 = tangible_book_value(ticker, latest, period) / total_liabilities(ticker, latest, period)
    z = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
    return z


# Ratios
# Liquidity (higher the better)
@return_None_on_error
@try_get_latest_ratio
def quick_ratio(ticker, latest: bool = True, period: int = -1):  # key
    return (current_assets(ticker, latest, period) - inventory(ticker, latest, period)) / current_liabilities(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def cash_ratio(ticker, latest: bool = True, period: int = -1):
    return cash(ticker, latest, period) / current_liabilities(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def operating_cash_ratio(ticker, latest: bool = True, period: int = -1):
    return operating_cash_flow(ticker, latest, period) / current_liabilities(ticker, latest, period)


# Coverage ratios (higher the better)
@return_None_on_error
@try_get_latest_ratio
def interest_coverage_ratio(ticker, latest: bool = True, period: int = -1):
    return EBITDA(ticker, latest, period) / interest_expense(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def debt_service_coverage_ratio(ticker, latest: bool = True, period: int = -1):  # key
    return operating_income(ticker, latest, period) / interest_expense(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def asset_coverage_ratio(ticker, latest: bool = True, period: int = -1):
    return (total_assets(ticker, latest, period) - intangible_assets(ticker, latest, period) - (
                current_liabilities(ticker, latest, period) - current_debt(ticker, latest, period))) / total_debt(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def cash_coverage_ratio(ticker, latest: bool = True, period: int = -1):
    return (EBIT(ticker, latest, period) + depreciation(ticker, latest, period)) / interest_expense(ticker, latest, period)


# Leverage ratios (lower the better)
@return_None_on_error
@try_get_latest_ratio
def total_debt_to_tangible_book_value_ratio(ticker, latest: bool = True, period: int = -1):
    return total_debt(ticker, latest, period) / tangible_book_value(ticker, latest, period)


@return_None_on_error
def total_debt_to_total_assets_ratio(ticker, latest: bool = True, period: int = -1):  # key
    return total_debt(ticker, latest, period) / total_assets(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def total_debt_to_EBITDA_ratio(ticker, latest: bool = True, period: int = -1):  # key
    return total_debt(ticker, latest, period) / EBITDA(ticker, latest, period)


# Piotroski’s F-score
@return_None_on_error
@try_get_latest_ratio
def ROIC(ticker, latest: bool = True, period: int = -1):
    return net_income(ticker, latest, period) / invested_capital(ticker, latest, period)


@return_None_on_error
@try_get_latest_ratio
def delta_ROIC(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = ROIC(ticker, latest=False, period=0)
    new = ROIC(ticker, latest=True, period=period)
    return new - old


@return_None_on_error
@try_get_latest_ratio
def delta_total_debt_to_EBITDA(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = total_debt_to_EBITDA_ratio(ticker, latest=False, period=0)
    new = total_debt_to_EBITDA_ratio(ticker, latest=True, period=period)
    return new - old


@return_None_on_error
@try_get_latest_ratio
def delta_total_debt_to_total_asset(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = total_debt_to_total_assets_ratio(ticker, latest=False, period=0)
    new = total_debt_to_total_assets_ratio(ticker, latest=True, period=period)
    return new - old


@return_None_on_error
@try_get_latest_ratio
def delta_quick_ratio(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = quick_ratio(ticker, latest=False, period=0)
    new = quick_ratio(ticker, latest=True, period=period)
    return new - old


@return_None_on_error
@try_get_latest_ratio
def delta_gross_profit(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = yahoo_api_get_financials_yearly(ticker)['annualGrossProfit'][0]['reportedValue']['raw']
    new = yahoo_api_get_financials_yearly(ticker)['annualGrossProfit'][period]['reportedValue']['raw']
    return new - old


@return_None_on_error
@try_get_latest_ratio
def delta_revenue_to_total_assets(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = revenue(ticker, latest=False, period=0) / total_assets(ticker, latest=False, period=0)
    new = revenue(ticker, latest=True, period=period) / total_assets(ticker, latest=True, period=period)
    return new - old


@return_None_on_error
@try_get_latest_ratio
def F_score(ticker, latest: bool = True, period: int = -1):
    score = 0
    # Profitability
    if ROIC(ticker, latest=True, period=period) > 0:
        score += 1
    if operating_cash_flow(ticker, latest=True, period=period) > 0:
        score += 1
    if delta_ROIC(ticker, latest=True, period=period) > 0:
        score += 1
    if operating_cash_flow(ticker, latest=True, period=period) / invested_capital(ticker, latest=True, period=period) > ROIC(ticker, latest=True, period=period):
        score += 1
    # Leverage, Liquidity and Source of Funds
    if delta_total_debt_to_EBITDA(ticker, latest=True, period=period) > 0 and delta_total_debt_to_total_asset(ticker, latest=True, period=period) < 0:
        score += 1
    if delta_quick_ratio(ticker, latest=True, period=period) > 0:
        score += 1
    # Operating Efficiency
    if delta_gross_profit(ticker, latest=True, period=period) > 0:
        score += 1
    if delta_revenue_to_total_assets(ticker, latest=True, period=period) > 0:
        score += 1
    return score
