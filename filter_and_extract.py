### Basic filtering script that continuously filters a single DataFrame by multiple criteria
### Multiple DataFrames are created, allowing a user to export whichever one they'd like, as well as more easily troubleshoot
### Main purpose is to highlight any instances of 'here' anchor text within the main body content of a page
### This code is far from ideal, and has been written quickly to serve an immediate purpose

import pandas as pd

#import all inlinks csv
df1 = pd.DataFrame(pd.read_csv('all_inlinks.csv', low_memory=False, header=0))

#filter out where source is sitemap. Update string to filter by different source
dfnositemap = df1.loc[~df1['Source']. str.contains("sitemap", na=False)]

#filter out redirects, rel=next/prev links and canonicals. We only want hyperlink data
dfhyperlinks = dfnositemap.loc[dfnositemap['Type'].str.match("Hyperlink", na=False)]

#filter out where link position is header or footer. 
dfcontentlinks = dfhyperlinks.loc[~dfhyperlinks['Link Position'].str.match("Header|Footer|Navigation",na=False)]

#Only include absolute path URLs
dfabsolute = dfcontentlinks.loc[dfcontentlinks['Path Type'].str.contains("Absolute", na=False)]

#Remove instances of '1' or previous anchor text (removing pagination)
dfremovepagination = dfabsolute.loc[~dfabsolute['Anchor'].str.match("1|Previous",na=False)]

#Extract all 'here' anchor text
dfhere = dfremovepagination[dfremovepagination['Anchor'].str.contains("here", na=False)]

#Export to CSV. Update the df to your desired dataset
dfhere.to_csv("filtered_all_inlinks.csv")