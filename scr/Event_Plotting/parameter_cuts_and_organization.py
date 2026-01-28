#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# should be able to suggest cuts from terminal
# spacecluster > n
# detector status = n
# ...
# export only one dataframe with correct labels (data_df)


#!!!! WIP, need to add more cuts later
#importing
from get_data import parquet_file

#extraction parameters
data_df = parquet_file[parquet_file['NSpaceCluster'] > 4].reset_index(drop=True) #write in function new var