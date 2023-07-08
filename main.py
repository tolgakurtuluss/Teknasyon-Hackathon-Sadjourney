import pandas as pd
import math
from k_means_constrained import KMeansConstrained
import datetime
import ast

df = pd.read_csv('database/employeedata.csv')

today = datetime.date.today()
day_number = today.isoweekday()  # Monday: 1, Tuesday: 2, ..., Sunday: 7

print("Today is " + str(day_number) + "th")

df['availability'] = df['attendance_status'].apply(lambda x: ast.literal_eval(x)[day_number-2])

calisanlardf = df[df['availability'] == 1]
data = calisanlardf.iloc[:, 6:8].values.tolist()
calisanlardf

max_number_of_passenger = 9
min_number_of_passenger = 5

number_of_service = math.ceil(len(calisanlardf)/max_number_of_passenger)
number_of_service

kmeans = KMeansConstrained(
    n_clusters = number_of_service,
    size_min = min_number_of_passenger,
    size_max = max_number_of_passenger,
    random_state = 0
)

kmeans.fit_predict(data)

labeled_df = calisanlardf.iloc[:, 6:8]
labeled_df['Service Number']=kmeans.labels_

sorted_df = labeled_df.groupby(labeled_df["Service Number"], group_keys=False).apply(lambda labeled_df: labeled_df.sort_values(by=["Service Number"]))
sorted_df.to_csv("labeled_points.csv", index=False)

sorted_df[sorted_df['Service Number'] == 49]

def convert_to_link(lat_long_list):
    base_url = "https://yandex.com.tr/harita/?"
    ll_param = "ll=" + str(lat_long_list.iloc[0]['lattitude']) + "%2C" + str(lat_long_list.iloc[0]['longitude'])
    rtext_param = "rtext="

    for _, row in lat_long_list.iloc[1:].iterrows():
        rtext_param += str(row['longitude']) + "%2C" + str(row['lattitude']) + "~"

    rtext_param = rtext_param + "41.11132935122801%2C29.024426736290895" + "~" #Teknasyon Base Konumu
    rtext_param = rtext_param[:-1]  # Remove the last "~" character

    link = base_url + ll_param + "&mode=routes&" + rtext_param + "&rtt=auto&ruri=~~~~~~~~~&z=12.41"

    return link

grouped = sorted_df.groupby('Service Number').apply(convert_to_link)

driverdf = pd.read_csv('database/driverdata.csv')

driverdf['Service Number'] = range(1, len(driverdf) + 1)
finaldf = driverdf.merge(grouped.reset_index())
finaldf

#calisanlardf.merge(sorted_df)

finaldf.to_csv("database/rotaolustu.csv",index=False)