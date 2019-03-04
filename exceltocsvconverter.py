import pandas as pd
data_xls = pd.read_excel('/Users/balasubramaniramamurthy/Documents/mypgm/Dashboard/exports/hitachi_pool_excel.xls', 'Sheet1', index_col=None)
data_xls.to_csv('/Users/balasubramaniramamurthy/Documents/mypgm/Dashboard/exports/Adobe_Hitachipool_New.csv', encoding='utf-8', index=False)


#mongoimport -d Dashboardtest_database -c db_hitachipool --type csv --file /Users/balasubramaniramamurthy/Documents/mypgm/Dashboard/exports/hitachi_pool.csv --headerline