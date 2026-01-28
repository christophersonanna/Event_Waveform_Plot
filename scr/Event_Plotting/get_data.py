#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import z_config as config
import pandas as pd #[will change later]

#loading data
parquet_file = pd.read_parquet(config.PROCESSED_DATA_PATH)