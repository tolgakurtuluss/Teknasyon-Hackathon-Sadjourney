import boto3
import awswrangler as wr
import datetime

days = ["mo", "tu", "we", "th", "fr", "sa", "su"]
dynamodb = boto3.client("dynamodb")

def convert_to_link(lat_long_list):
    # print(lat_long_list)
    base_url = "https://yandex.com.tr/harita/?"
    ll_param = "ll=" + str(lat_long_list.iloc[0]['lattitude']) + "%2C" + str(lat_long_list.iloc[0]['longitude'])
    rtext_param = "rtext="

    for _, row in lat_long_list.iloc[1:].iterrows():
        rtext_param += str(row['longitude']) + "%2C" + str(row['lattitude']) + "~"

    rtext_param = rtext_param + "41.11132935122801%2C29.024426736290895" + "~"  # Teknasyon Base Konumu
    rtext_param = rtext_param[:-1]  # Remove the last "~" character

    link = base_url + ll_param + "&mode=routes&" + rtext_param + "&rtt=auto&ruri=~~~~~~~~~&z=12.41"

    return lat_long_list.reset_index().loc[0, "driverId"], link

def lambda_handler(event, context):
    today = datetime.date.today()
    day_number = today.isoweekday() - 1

    employees = wr.dynamodb.read_partiql_query(
        query=f"""SELECT id , lattitude, longitude, driverId FROM Employee WHERE {days[day_number]}=?""",
        parameters=[True])
    grouped = employees.groupby('driverId').apply(convert_to_link)
    for driver, link in grouped.values.tolist():
        dynamodb.put_item(TableName='links', Item={'id': {'S': driver},
                                                   'link': {'S': link}})
