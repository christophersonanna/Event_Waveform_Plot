#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import pandas as pd #[will change later]

#loading data
parquet_file = pd.read_parquet(config.PROCESSED_DATA_PATH)