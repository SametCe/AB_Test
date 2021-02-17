import pandas as pd
from scipy.stats import shapiro
from scipy import stats

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Reading Datasets. There are two different datasets to compare.
df_control = pd.read_excel("Week_05/AB_Test_Project/ab_testing_data.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("Week_05/AB_Test_Project/ab_testing_data.xlsx", sheet_name="Test Group")

df_control.head()
df_test.head()

df_control.shape
df_test.shape

df_control.info()
df_test.info()


# Setting outliers, if there are any.
def outlier_thresholds(dataframe, variable, low_quantile=0.05, up_quantile=0.95):
    quantile_one = dataframe[variable].quantile(low_quantile)
    quantile_three = dataframe[variable].quantile(up_quantile)
    interquantile_range = quantile_three - quantile_one
    up_limit = quantile_three + 1.5 * interquantile_range
    low_limit = quantile_one - 1.5 * interquantile_range
    return low_limit, up_limit


low_limit_click, up_limit_click = outlier_thresholds(df_control, "Impression")
low_limit_click, up_limit_click = outlier_thresholds(df_control, "Click")
low_limit_purchase, up_limit_purchase = outlier_thresholds(df_control, "Purchase")
low_limit_earning, up_limit_earning = outlier_thresholds(df_control, "Earning")


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


column_names_to_set = ["Impression", "Click", "Purchase", "Earning"]

for variable in column_names_to_set:
    replace_with_thresholds(df_control, variable)
    replace_with_thresholds(df_test, variable)


# Defining the AB Testing hypothesis
# H0: There is no statistical difference between the control and test groups in terms of the average number of purchases
# H1: There is statistical difference between the control and test groups in terms of the average number of purchases.
df_control["Purchase"].mean()
df_test["Purchase"].mean()


# Target variables here is "Purchase".
control_purchase = df_control["Purchase"]
test_purchase = df_test["Purchase"]

# There are 2 prerequisites for the AB test: Assumption of Normality and Homogeneity of Variance.

# Normality Test
# H0: Assumption of Normality is provided.
# H1: Assumption of Normality is not provided.
test_statistic_control, p_value_control = shapiro(control_purchase)
print('Test Statistic = %.4f, p-value = %.4f' % (test_statistic_control, p_value_control))
p_value_control < 0.05
test_statistic_test, p_value_test = shapiro(test_purchase)
print('Test Statistic = %.4f, p-value = %.4f' % (test_statistic_test, p_value_test))
p_value_test < 0.05
# Both p values are higher than 0.05 so we cant reject H0, assumption of Normality is provided.


# Variance Homogeneity Test - Levene's test
# H0: Homogeneity of Variance is provided.
# H1: Homogeneity of Variance is not provided.
stats.levene(control_purchase, test_purchase)
# p value is higher than 0.05 so we cant reject H0, Homogeneity of Variance is provided.
# In this case, both two conditions are provided.


# AB Testing hypothesis
# H0: There is no statistical difference between the control and test groups in terms of the average number of purchases
# H1: There is statistical difference between the control and test groups in terms of the average number of purchases.
test_statistic, p_value = stats.ttest_ind(control_purchase, test_purchase, equal_var=True)

print('Test Statistic = %.4f, p-value = %.4f' % (test_statistic, p_value))
# p value is higher than 0.05 so we can't reject H0.
# There is no statistical difference between the control and test groups in terms of the average number of purchases.
