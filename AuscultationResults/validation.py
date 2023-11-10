import pandas as pd
import numpy as np

theo_path = '../HeartSounds/Murmers Test.csv'
theoretical_df = pd.read_csv(theo_path)

exp_path = '../HeartSounds/michiganSoundsProcessedData.csv'
exp_df = pd.read_csv(exp_path)

file_names = []
lub_sys_error = []
lub_sys_percent_error = []
dub_dias_error = []
dub_dias_percent_error = []
bpm_error = []
bpm_percent_error = []

errors = {'File Name': file_names,
          'Lub and Sys Length Error': lub_sys_error,
          'Lub and Sys % Error': lub_sys_percent_error,
          'Dub and Dias Length Error': dub_dias_error,
          'Dub and Dias % Error': dub_dias_percent_error,
          'BPM Error': bpm_error,
          'BPM % Error': bpm_percent_error
}

print(len(theoretical_df))
print(theoretical_df.head())

for i in range(len(theoretical_df)):
    file_names.append(exp_df['File Name'][i])

    lub_and_sys_length_dif = theoretical_df['S2-S1 AVG'][i] - exp_df['Lub+Sys Length (S2-S1)'][i]
    lub_sys_percent_err = (lub_and_sys_length_dif/theoretical_df['S2-S1 AVG'][i])*100
    lub_sys_error.append(abs(lub_and_sys_length_dif))
    lub_sys_percent_error.append(abs(lub_sys_percent_err))


    dub_and_dias_length_dif = theoretical_df['S1-S2 AVG'][i] - exp_df['Dub+Dias Length (S1-S2)'][i]
    dub_dias_percent_err = (dub_and_dias_length_dif / theoretical_df['S1-S2 AVG'][i])*100
    dub_dias_error.append(abs(dub_and_dias_length_dif))
    dub_dias_percent_error.append(abs(dub_dias_percent_err))

    bpm_err = theoretical_df['BPM'][i] - exp_df['BPM'][i]
    bpm_percent_err = (bpm_err/theoretical_df['BPM'][i])*100
    bpm_error.append(abs(bpm_err))
    bpm_percent_error.append(abs(bpm_percent_err))


error_df = pd.DataFrame(errors)
error_df.to_csv('../HeartSounds/MurmersComparison.csv')
