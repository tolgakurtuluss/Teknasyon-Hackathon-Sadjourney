import xml.etree.ElementTree as ET
import pandas as pd
import os 
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#IBB kameraları webapi servisi

url = "https://tkmservices.ibb.gov.tr/web/api/IntensityMap/v1/Camera"
file_name = "file.xml"

try:
    urllib.request.urlretrieve(url, file_name)
    print("XML file downloaded successfully.")
except urllib.error.URLError as e:
    print("Failed to download the XML file:", e)

tree = ET.parse(file_name)
root = tree.getroot()

namespaces = {
    'i': 'http://www.w3.org/2001/XMLSchema-instance',
    'default': 'http://schemas.datacontract.org/2004/07/TKMWebApi.Controllers.IntensityMap.Models',
    'd3p1': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
}

columns = ['GroupId', 'ID', 'Images', 'Name', 'VideoURL', 'VideoURL_SSL', 'XCoord', 'YCoord', 'Group']
data = []

for camera_group in root.findall('default:CameraGroupedList', namespaces):

    group_id = camera_group.find('default:GroupId', namespaces).text
    id = camera_group.find('default:ID', namespaces).text
    images = [img.text for img in camera_group.findall('.//d3p1:string', namespaces)]
    name = camera_group.find('default:Name', namespaces).text
    video_url = camera_group.find('default:VideoURL', namespaces).text
    video_url_ssl = camera_group.find('default:VideoURL_SSL', namespaces).text
    x_coord = camera_group.find('default:XCoord', namespaces).text
    y_coord = camera_group.find('default:YCoord', namespaces).text
    group = camera_group.find('default:Group', namespaces).text
    
    data.append({
        'GroupId': group_id,
        'ID': id,
        'Images': images,
        'Name': name,
        'VideoURL': video_url,
        'VideoURL_SSL': video_url_ssl,
        'XCoord': x_coord,
        'YCoord': y_coord,
        'Group': group
    })

df = pd.DataFrame(data, columns=columns)
print(df)

df1 = df[['ID', 'Name', 'VideoURL','XCoord','YCoord']]
df1.to_csv("database/kamera.csv")

os.remove(file_name)