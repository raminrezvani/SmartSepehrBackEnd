# influx
# add= mqtt.angizehco:8086
# user=  leo
#pass =  Goldenhand76

# grafana
# http://mqtt.angizehco.com:3000/login
# admin
# admin

import time
import psutil
from influxdb_client import InfluxDBClient, Point, WritePrecision

# InfluxDB Configuration
INFLUXDB_URL = "http://mqtt.angizehco.com:8086"  # Replace with your InfluxDB URL
INFLUXDB_TOKEN = "H6hcY5TKsp1ff0W8g6Rfb84EvAmZ79wPBbafiBodU67sfS_dfcFIKtFNsUHxKx4wt9J9ehdtHrImOwsEETOmgg=="  # Replace with your InfluxDB token
INFLUXDB_ORG = "angizeh"  # Replace with your InfluxDB organization
INFLUXDB_BUCKET = "system_metrics_server185"  # Replace with your InfluxDB bucket name

# Initialize InfluxDB Client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
# write_api = client.write_api(write_options=WritePrecision.NS)
write_api = client.write_api()

def send_metrics_to_influx(call_count):
    """
    Send custom CPU and RAM usage values to InfluxDB.
    :param cpu_usage: CPU usage percentage.
    :param ram_usage: RAM usage percentage.
    """
    point = (
        Point("system_metrics")
        .field("call_count", call_count)
        .time(time.time_ns(), WritePrecision.NS)
    )

    try:
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"Data written: CPU={cpu_usage}%, RAM={ram_usage}%")
    except Exception as e:
        print(f"Failed to write data to InfluxDB: {e}")

