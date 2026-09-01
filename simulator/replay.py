import argparse
import csv
import time
from pathlib import Path

import httpx

DEFAULT_DATA_FILE = Path("data/sample/hvac_sensor_readings.csv")


def row_to_payload(
    row: dict[str, str],
) -> dict[str, str | float]:
    return {
        "asset_id": row["asset_id"],
        "timestamp": row["timestamp"],
        "temperature_f": float(row["temperature_f"]),
        "humidity_pct": float(row["humidity_pct"]),
        "co2_ppm": float(row["co2_ppm"]),
        "vibration_mm_s": float(row["vibration_mm_s"]),
        "power_kw": float(row["power_kw"]),
        "supply_air_temp_f": float(row["supply_air_temp_f"]),
        "return_air_temp_f": float(row["return_air_temp_f"]),
        "fan_speed_pct": float(row["fan_speed_pct"]),
    }


def replay(
    api_url: str,
    data_file: Path,
    interval: float,
) -> None:
    with data_file.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file_handle:
        reader = csv.DictReader(file_handle)

        with httpx.Client(timeout=10.0) as client:
            for row in reader:
                payload = row_to_payload(row)

                response = client.post(
                    f"{api_url}/v1/predict",
                    json=payload,
                )

                response.raise_for_status()

                prediction = response.json()

                print(
                    f"{prediction['asset_id']} "
                    f"severity={prediction['severity']} "
                    f"risk={prediction['risk_score']}"
                )

                time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--api-url",
        default="http://127.0.0.1:8000",
    )

    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
    )

    args = parser.parse_args()

    replay(
        api_url=args.api_url,
        data_file=args.data_file,
        interval=args.interval,
    )


if __name__ == "__main__":
    main()
