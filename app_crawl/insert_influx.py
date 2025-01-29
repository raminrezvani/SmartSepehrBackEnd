
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

class Influxdb():
    def __init__(self):
        # InfluxDB Configuration
        self.INFLUXDB_URL = "http://mqtt.angizehco.com:8086"  # Replace with your InfluxDB URL
        self.INFLUXDB_TOKEN = "H6hcY5TKsp1ff0W8g6Rfb84EvAmZ79wPBbafiBodU67sfS_dfcFIKtFNsUHxKx4wt9J9ehdtHrImOwsEETOmgg=="  # Replace with your InfluxDB token
        self.INFLUXDB_ORG = "angizeh"  # Replace with your InfluxDB organization
        self.INFLUXDB_BUCKET = "system_metrics_server185"  # Replace with your InfluxDB bucket name

        # Initialize InfluxDB Client
        self.client = InfluxDBClient(url=self.INFLUXDB_URL, token=self.INFLUXDB_TOKEN, org=self.INFLUXDB_ORG)
        # write_api = client.write_api(write_options=WritePrecision.NS)
        self.write_api = self.client.write_api()


    def count_system_threads(self):
        total_threads = 0
        for process in psutil.process_iter():
            try:
                # Access the number of threads for the process
                total_threads += process.num_threads()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Ignore processes that no longer exist or cannot be accessed
                continue
        return total_threads

    def capture_logs(self,count_call,provider):
        point = (
            Point("system_metrics")
            .field("count_call", count_call)
            .field("provider", provider)
            .time(time.time_ns(), WritePrecision.NS)
        )

        # Write the point to InfluxDB
        try:
            self.write_api.write(bucket=provider, org=self.INFLUXDB_ORG, record=point)
            # print(f"Data written: count_call={count_call}%, provider={provider}% ")
        except Exception as e:
            print(f"Failed to write data to InfluxDB: {e}")




    def capture_metrics(self):
        """Capture system metrics and write to InfluxDB."""
        while True:
            # Get CPU and RAM usage
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            # Get total thread count
            thread_count = self.count_system_threads()
            # Create a data point
            point = (
                Point("system_metrics")
                    .field("cpu_usage", cpu_usage)
                    .field("ram_usage", ram_usage)
                    .field('thread_count', thread_count)
                    .time(time.time_ns(), WritePrecision.NS)
            )

            # Write the point to InfluxDB
            try:
                self.write_api.write(bucket=self.INFLUXDB_BUCKET, org=self.INFLUXDB_ORG, record=point)
                print(f"Data written: CPU={cpu_usage}%, RAM={ram_usage}%, Thread={thread_count}")
            except Exception as e:
                print(f"Failed to write data to InfluxDB: {e}")

            # Sleep for a second before the next capture
            time.sleep(1)
