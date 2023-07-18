import pandas as pd
import copy


class DataStitchingNoiseReduced:
    def __init__(self, method, raw_data_sb, st_noise, p2p_noise, cleared_data_sb):
        self.no_runs = len(raw_data_sb)
        self.no_st_runs = len(raw_data_sb[0])
        self.method = method
        self.raw_data_sb = raw_data_sb
        self.st_noise = st_noise
        self.p2p_noise = p2p_noise
        self.cleared_data_sb = cleared_data_sb

        raw_data_merged = list()
        cleared_data_merged = list()

        for idx in range(self.no_runs):
            raw_data_merged.append(pd.concat(raw_data_sb[idx], axis=1).sort_index(axis=1))
            cleared_data_merged.append(pd.concat(cleared_data_sb[idx], axis=1).sort_index(axis=1))

        self.raw_data_merged = raw_data_merged
        self.cleared_data_merged = cleared_data_merged

        raw_data_merged_wn = list()
        for run in self.raw_data_merged:
            tmp = run.transpose()
            tmp.index = 10**7 / tmp.index
            raw_data_merged_wn.append(tmp)

        cleared_data_merged_wn = list()
        for run in self.cleared_data_merged:
            tmp = run.transpose()
            tmp.index = 10**7 / tmp.index
            cleared_data_merged_wn.append(tmp)

        self.raw_data_merged_wn = raw_data_merged_wn
        self.cleared_data_merged_wn = cleared_data_merged_wn
