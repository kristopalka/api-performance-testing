from vizualization.utils.load import get_dataframe, load_durations_dataframe

services = ["gin"] # "flask", "fastapi", "spring",
rps_tab = list(range(50, 801, 50))
rps_tab = [50, 100, 150]
iter = [4]


for service in services:
    for rps in rps_tab:
        for i in iter:
            get_dataframe(f'const_rps/iter_{i}', service, "hello", 120, rps, force_process=True)



# import os
# import re
#
# path_base = "./../../results/const_rps"
#
# regex_pattern = r'raw_.*json'
#
# for root, dirs, files in os.walk(path_base):
#     for file in files:
#         if re.match(regex_pattern, file):
#             file_raw = os.path.join(root, file)
#             file_proc = re.sub(r'raw_(.*)\.json', r'proc_\1.csv', file_raw)



