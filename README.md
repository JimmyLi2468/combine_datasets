# combine_datasets
combine two fund datasets and identify themes

## To run the program
Download and store `analyze.py`, `fund_a.txt `,`fund_b.txt`, and `states.py` in the same directory

run `python analyze.py`

**To create output files**
Uncomment line `226` and line `230`

## Question 1

Dataset `fund_a` and `fund_b` are combined into one dataframe containing features both in fund_a and those only in fund_b

*Duplicates* are found by comparing `['fund_name', 'asset_class', 'strategy', 'status', 'manager', 'fund_vintage_year', 'fund_size']`

If all are equal for these characters, the two entries are considered duplicates
```
duplicate = df[df.duplicated(subset=['fund_name','asset_class','strategy','status','manager','fund_vintage_year','fund_size'], keep=False)]

```

Any information in the second entry of the duplicate pair, is inserted to the first entry of the pair, for example:

There are two entries in fund_a and fund_b found are considered duplicates:
```
                             fund_name     asset_class   strategy  status                           manager  fund_vintage_year  fund_size  status manager_country
87   Thompson Street Capital Partners V  Private Equity  PE-BUYOUT  Closed  Thompson Street Capital Partners               2018     1150.0  Closed   United States
184  Thompson Street Capital Partners V  Private Equity  PE-BUYOUT  Closed  Thompson Street Capital Partners               2018     1150.0  Closed              US
```
Then the first entry
```
fund_id                                                              16323-31F
fund_name                                   Thompson Street Capital Partners V
......
manager_post_code                                                        63105
preferred_industries         [Business Products and Services (B2B),Healthca...
firm_id                                                                   NULL
manager_fax                                                               NULL
primary_geographic_focus                                                  NULL
```
is modified using the second entry to fill any value that is NULL in the first
```
fund_id                                                              16323-31F
fund_name                                   Thompson Street Capital Partners V
......
manager_post_code                                                        63105
preferred_industries         [Business Products and Services (B2B),Healthca...
firm_id                                                                   2204
manager_fax                                                    +1 314 446 3310
primary_geographic_focus                                         North America
```

**To obtain the full dataset, type 8 when prompt to select theme** 

a csv file called `combined_dataset.csv` will be stored into your local directory as well


## Question 2

You will be prompt with several options

```
 asset class: 1, strategy: 2, fund country: 3, 
  status: 4, geographic focus: 5, industry focus: 6, 
  fund size: 7, full dataset: 8, quit: 0
  
  What theme (core data (default) use flag -c, full data -a): 
```

You can choose which ever you like or just quit the program by typing 0

**Note**: Option 8 is the result dataset that combines `fund_a` and `fund_b` with duplicates combined to single entries. Option 8 will output the full dataset on screen as well as store the dataset to a csv file in your local directory called `combined_dataset.csv`

Under each option, you will be given the possible values associated with each option

For example, for strategy (option 2):
```
What theme (core data (default) use flag -c, full data -a): 2
{'PC-DISTRESSED', 'PE-GROWTH', 'PE-DISTRESSED', 'PE-BALANCED', 'PE-BUYOUT', 'VC-EARLY', 'VC-LATE'} 
```
Then type in your choice of parameter. You will get all entries that has `strategy == PE-DISTRESSED`:
```
Type strategy: PE-DISTRESSED
                 fund_name     asset_class  ...                               preferred_industries primary_geographic_focus
2           Rutland Fund I  Private Equity  ...  [Business Products and Services (B2B),Consumer...                     NULL
22           Meriturn Fund  Private Equity  ...                     [Commercial Services,Forestry]                     NULL
114  Questor Partners Fund  Private Equity  ...                               [Financial Services]            North America
115           Rutland Fund  Private Equity  ...                    [Consumer Services,Industrials]                   Europe
116   Sun Capital Partners  Private Equity  ...                                      [Diversified]            North America
174        Valtegra Fund I  Private Equity  ...                         [Logistics & Distribution]                   Europe

[6 rows x 9 columns]
```

Follow the steps, you will be able to query through the 7 options



