from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta


class ProviderManager:
    def __init__(self, executor, night_count, adults):
        self.executor = executor
        self.night_count = night_count
        self.adults = adults

    def fetch_single_day(self, provider_instance, day_date):
        """
        Fetch data for a single provider for a specific day.
        """
        try:
            start_time = datetime.now()
            result = provider_instance.get_result()
            spend_time = (datetime.now() - start_time).total_seconds()
            print(f"Fetched data for {provider_instance.name} on {day_date}: {len(result.get('data', []))} records in {spend_time:.2f}s")
            return {day_date.strftime('%Y-%m-%d'): result.get('data', [])}
        except Exception as e:
            print(f"Failed to fetch data for {provider_instance.name} on {day_date}: {e}")
            return {day_date.strftime('%Y-%m-%d'): []}

    def fetch_provider_data(self, provider_name, provider_instance, start_date, num_days):
        """
        Fetch data for a single provider for the next `num_days` days.
        """
        print(f"Fetching data for provider: {provider_name}")
        tasks = {
            self.executor.submit(self.fetch_single_day, provider_instance, start_date + timedelta(days=day))
            for day in range(num_days)
        }

        provider_results = {}
        for future in as_completed(tasks):
            result = future.result()
            provider_results.update(result)
        return {provider_name: provider_results}

    def get_all_providers_data(self, source, target, start_date, num_days=7):
        """
        Fetch data for all providers concurrently.
        """
        providers = [
            ("Booking", Booking(source, target, start_date, self.night_count, adults=self.adults)),
            ("Jimbo", Jimbo(source, target, start_date, self.night_count, adults=self.adults)),
            ("Deltaban", Deltaban(start_date, self.night_count, source, target, adults=self.adults)),
            # Add other providers as needed
        ]

        tasks = {
            self.executor.submit(self.fetch_provider_data, name, instance, start_date, num_days): name
            for name, instance in providers
        }

        all_results = {}
        for future in as_completed(tasks):
            name = tasks[future]
            try:
                result = future.result()
                all_results.update(result)
            except Exception as e:
                print(f"Failed to fetch data for {name}: {e}")

        return all_results
