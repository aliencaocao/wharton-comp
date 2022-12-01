import orjson as json
import xueqiu

with open('ticker_data.json', 'r') as f:
    ticker_data = json.loads(f.read())


def return_None_on_error(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            if func.__name__ == 'inner_func':
                raise e
            e = str(e).strip(')').strip('KeyError(')
            print(f"{func.__name__}: Key not found: {e}")
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
        if period >= 0: period -= 4  # convert from positive indexing to negative
        for i in range(period, -5, -1):
            kwargs['latest'] = False
            kwargs['period'] = i
            try:
                r = func(*args, **kwargs)
            except TypeError:
                print(f'No data for {func.__name__} for period {i}')
            except IndexError:
                r = None
                break
            except Exception as e:
                print(f'other exception, ticker: {args[0]}', e)
            else:
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
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualPretaxIncome'][period]['reportedValue']['raw'] + \
               yahoo_api_get_financials_yearly(ticker)['annualNetInterestIncome'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


def EBITDA(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualEBITDA'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return EBIT(ticker, latest, period) + depreciation_and_amortization(ticker, latest, period)
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualNormalizedEBITDA'][period]['reportedValue']['raw'] + \
               yahoo_api_get_financials_yearly(ticker)['annualTotalUnusualItems'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


@return_None_on_error
def depreciation(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualReconciledDepreciation'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualDepreciationAmortizationDepletion'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


def interest_expense(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return abs(yahoo_api_get_financials_yearly(ticker)['annualInterestExpense'][period]['reportedValue']['raw'])
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return abs(yahoo_api_get_financials_yearly(ticker)['annualInterestExpenseNonOperating'][period]['reportedValue']['raw'])
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return abs(yahoo_api_get_financials_yearly(ticker)['annualTotalOtherFinanceCost'][period]['reportedValue']['raw'])
    except (KeyError, TypeError) as e:
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


def current_assets(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentAssets'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalAssets'][period]['reportedValue']['raw'] - yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalNonCurrentAssets'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


@return_None_on_error
def total_liabilities(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalLiabilitiesNetMinorityInterest'][period]['reportedValue']['raw']


def current_liabilities(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentLiabilities'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalLiabilitiesNetMinorityInterest'][period]['reportedValue']['raw'] - yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalNonCurrentLiabilitiesNetMinorityInterest'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


@return_None_on_error
def total_debt(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][period]['reportedValue']['raw']


def current_debt(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualCurrentDebt'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_balance_sheet_yearly(ticker)['annualTotalDebt'][period]['reportedValue']['raw'] - yahoo_api_get_balance_sheet_yearly(ticker)['annualLongTermDebt'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


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
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualCashFlowsfromusedinOperatingActivitiesDirect'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


def depreciation_and_amortization(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualDepreciationAmortizationDepletion'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualReconciledDepreciation'][period]['reportedValue']['raw'] + \
               yahoo_api_get_cashflow_yearly(ticker)['annualAmortizationOfSecurities'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_financials_yearly(ticker)['annualReconciledDepreciation'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    try:
        return yahoo_api_get_cashflow_yearly(ticker)['annualAmortizationOfSecurities'][period]['reportedValue']['raw']
    except (KeyError, TypeError) as e:
        print(e)
    return None


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
@try_get_latest_ratio
def quick_ratio(ticker, latest: bool = True, period: int = -1):  # key
    try:
        return (current_assets(ticker, latest, period) - inventory(ticker, latest, period)) / current_liabilities(ticker, latest, period)
    except Exception as e:
        print(e)
    return xueqiu.quick_ratio(ticker, latest, period)   # this quick ratio function does error handling within it (and returns None if got error), so no need try/except here anymore


@try_get_latest_ratio
def cash_ratio(ticker, latest: bool = True, period: int = -1):
    return cash(ticker, latest, period) / current_liabilities(ticker, latest, period)


@try_get_latest_ratio
def operating_cash_ratio(ticker, latest: bool = True, period: int = -1):
    return operating_cash_flow(ticker, latest, period) / current_liabilities(ticker, latest, period)


# Coverage ratios (higher the better)
@try_get_latest_ratio
def interest_coverage_ratio(ticker, latest: bool = True, period: int = -1):
    return EBITDA(ticker, latest, period) / interest_expense(ticker, latest, period)


@try_get_latest_ratio
def debt_service_coverage_ratio(ticker, latest: bool = True, period: int = -1):  # key
    return operating_income(ticker, latest, period) / interest_expense(ticker, latest, period)


@try_get_latest_ratio
def asset_coverage_ratio(ticker, latest: bool = True, period: int = -1):
    return (total_assets(ticker, latest, period) - intangible_assets(ticker, latest, period) - (
                current_liabilities(ticker, latest, period) - current_debt(ticker, latest, period))) / total_debt(ticker, latest, period)


@try_get_latest_ratio
def cash_coverage_ratio(ticker, latest: bool = True, period: int = -1):
    return (EBIT(ticker, latest, period) + depreciation(ticker, latest, period)) / interest_expense(ticker, latest, period)


# Leverage ratios (lower the better)
@try_get_latest_ratio
def total_debt_to_tangible_book_value_ratio(ticker, latest: bool = True, period: int = -1):
    return total_debt(ticker, latest, period) / tangible_book_value(ticker, latest, period)


@try_get_latest_ratio
def total_debt_to_total_assets_ratio(ticker, latest: bool = True, period: int = -1):  # key
    return total_debt(ticker, latest, period) / total_assets(ticker, latest, period)


@try_get_latest_ratio
def total_debt_to_EBITDA_ratio(ticker, latest: bool = True, period: int = -1):
    return total_debt(ticker, latest, period) / EBITDA(ticker, latest, period)


# Piotroski’s F-score
@try_get_latest_ratio
def ROIC(ticker, latest: bool = True, period: int = -1):
    return net_income(ticker, latest, period) / invested_capital(ticker, latest, period)


@try_get_latest_ratio
def ROA(ticker, latest: bool = True, period: int = -1):
    return net_income(ticker, latest, period) / total_assets(ticker, latest, period)


@try_get_latest_ratio
def delta_ROA(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = ROA(ticker, latest=False, period=period-1)
    new = ROA(ticker, latest=True, period=period)
    return new - old


@try_get_latest_ratio
def delta_total_debt_to_EBITDA(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = total_debt_to_EBITDA_ratio(ticker, latest=False, period=0)
    new = total_debt_to_EBITDA_ratio(ticker, latest=True, period=period)
    return new - old


@try_get_latest_ratio
def delta_total_debt_to_total_asset(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = total_debt_to_total_assets_ratio(ticker, latest=False, period=0)
    new = total_debt_to_total_assets_ratio(ticker, latest=True, period=period)
    return new - old


@try_get_latest_ratio
def delta_quick_ratio(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = quick_ratio(ticker, latest=False, period=0)
    new = quick_ratio(ticker, latest=True, period=period)
    return new - old


@try_get_latest_ratio
def delta_gross_profit(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = yahoo_api_get_financials_yearly(ticker)['annualGrossProfit'][period-1]['reportedValue']['raw']
    new = yahoo_api_get_financials_yearly(ticker)['annualGrossProfit'][period]['reportedValue']['raw']
    return new - old


@try_get_latest_ratio
def delta_revenue_to_total_assets(ticker, latest: bool = True, period: int = -1):
    if latest: period = -1
    old = revenue(ticker, latest=False, period=0) / total_assets(ticker, latest=False, period=period-1)
    new = revenue(ticker, latest=True, period=period) / total_assets(ticker, latest=True, period=period)
    return new - old


def F_score(ticker, latest: bool = True, period: int = -1):  # allow BOD
    if latest: period = -1
    score = 0
    # Profitability
    roic = ROIC(ticker, latest=True, period=period)
    if roic is None or roic > 0:
        print('ROIC pass')
        score += 1
    ocf = operating_cash_flow(ticker, latest=True, period=period)
    if ocf is None or ocf > 0:
        print('OCF pass')
        score += 1
    droic = delta_ROA(ticker, latest=True, period=period)
    if droic is None or droic > 0:
        print('delta ROIC pass')
        score += 1
    ocf_to_invested_cap = operating_cash_flow(ticker, latest=True, period=period) / invested_capital(ticker, latest=True, period=period)
    if ocf_to_invested_cap is None or roic is None or ocf_to_invested_cap > roic:
        print('OCF/IC pass')
        score += 1
    # Leverage, Liquidity and Source of Funds
    d_debt_to_EDITDA = delta_total_debt_to_EBITDA(ticker, latest=True, period=period)
    d_debt_to_asset = delta_total_debt_to_total_asset(ticker, latest=True, period=period)
    if (d_debt_to_EDITDA is None or d_debt_to_EDITDA > 0) and (d_debt_to_asset is None or d_debt_to_asset < 0):
        print('Debt/EDITDA pass')
        score += 1
    d_quick_ratio = delta_quick_ratio(ticker, latest=True, period=period)
    if d_quick_ratio is None or d_quick_ratio > 0:
        print('Quick pass')
        score += 1
    # Operating Efficiency
    d_gross_profit = delta_gross_profit(ticker, latest=True, period=period)
    if d_gross_profit is None or d_gross_profit > 0:
        print('Gross profit pass')
        score += 1
    d_rev_to_asset = delta_revenue_to_total_assets(ticker, latest=True, period=period)
    if d_rev_to_asset is None or d_rev_to_asset > 0:
        print('Rev/Asset pass')
        score += 1
    return score
