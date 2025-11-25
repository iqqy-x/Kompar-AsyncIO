import asyncio
import aiohttp
import pandas as pd
import os
import time
from dotenv import load_dotenv
from tqdm.asyncio import tqdm_asyncio   

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEATHER_URL = "http://api.weatherapi.com/v1/current.json"


async def fetch_weather(session, row):
    lat = row["latitude"]
    lon = row["longitude"]

    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "aqi": "no"
    }

    try:
        async with session.get(WEATHER_URL, params=params, timeout=10) as resp:
            data = await resp.json()

            if "current" not in data:
                return {
                    "last_update": "No Data",
                    "suhu": None,
                    "kelembapan": None,
                    "kondisi": None,
                    "angin_ms": None,
                    "arah_angin": None,
                    "uv": None
                }

            c = data["current"]
            return {
                "last_update": c["last_updated"],
                "suhu": c["temp_c"],
                "kelembapan": c["humidity"],
                "kondisi": c["condition"]["text"],
                "angin_ms": c["wind_kph"] / 3.6,
                "arah_angin": c["wind_degree"],
                "uv": c["uv"],
            }

    except Exception as e:
        return {
            "last_update": f"Error: {str(e)}",
            "suhu": None,
            "kelembapan": None,
            "kondisi": None,
            "angin_ms": None,
            "arah_angin": None,
            "uv": None
        }


async def main():
    start_time = time.time()

    df = pd.read_excel("data/cleaned/kecamatan_cleaned.xlsx")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, row) for _, row in df.iterrows()]

        results = await tqdm_asyncio.gather(
            *tasks,
            desc="Mengambil data cuaca",
            ncols=100
        )

    df_out = pd.concat([df, pd.DataFrame(results)], axis=1)

    output_path = "data/output/hasil_cuaca.xlsx"
    df_out.to_excel(output_path, index=False)

    end_time = time.time()

    print(f"\nFile disimpan di {output_path}")
    print(f"Waktu eksekusi: {end_time - start_time:.2f} detik")


if __name__ == "__main__":
    asyncio.run(main())
