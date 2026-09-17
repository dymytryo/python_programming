"""Generate the synthetic order dataset used by the Streamlit demos.

The data is fabricated, deterministic, and small enough to commit. Re-running
this script always produces a byte-identical `orders.csv`, so a diff on the CSV
means the generator changed, not that the random seed moved.

Run from this folder:

    python generate_orders.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

START = date(2025, 1, 1)
DAYS = 270
ROWS = 2400

REGIONS = ["West", "Midwest", "Northeast", "South"]
CHANNELS = ["Direct", "Partner", "Marketplace"]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB"]

# Per-segment (unit price range, typical units per order). Enterprise buys
# fewer, larger orders; SMB buys many small ones.
SEGMENT_SHAPE = {
    "Enterprise": ((900, 2600), (1, 12)),
    "Mid-Market": ((320, 950), (2, 30)),
    "SMB": ((45, 300), (1, 60)),
}

SEGMENT_WEIGHTS = [0.18, 0.34, 0.48]
REGION_WEIGHTS = [0.31, 0.22, 0.24, 0.23]
CHANNEL_WEIGHTS = [0.46, 0.27, 0.27]


def build_rows(seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    rows = []

    for i in range(ROWS):
        order_date = START + timedelta(days=rng.randrange(DAYS))
        segment = rng.choices(SEGMENTS, SEGMENT_WEIGHTS)[0]
        (price_low, price_high), (unit_low, unit_high) = SEGMENT_SHAPE[segment]

        units = rng.randint(unit_low, unit_high)
        unit_price = round(rng.uniform(price_low, price_high), 2)

        # Discounts cluster at the round numbers a sales team actually quotes.
        discount = rng.choices([0.0, 0.05, 0.10, 0.15, 0.25], [0.5, 0.2, 0.15, 0.1, 0.05])[0]

        gross = units * unit_price
        revenue = round(gross * (1 - discount), 2)
        # Cost of goods runs 55-72% of list price, independent of the discount,
        # so heavily discounted orders are the ones with thin margin.
        cost = round(gross * rng.uniform(0.55, 0.72), 2)

        rows.append(
            {
                "order_id": f"SO-{100000 + i}",
                "order_date": order_date.isoformat(),
                "region": rng.choices(REGIONS, REGION_WEIGHTS)[0],
                "channel": rng.choices(CHANNELS, CHANNEL_WEIGHTS)[0],
                "segment": segment,
                "units": units,
                "unit_price": unit_price,
                "discount": discount,
                "revenue": revenue,
                "cost": cost,
            }
        )

    rows.sort(key=lambda r: (r["order_date"], r["order_id"]))
    return rows


def main() -> None:
    out = Path(__file__).with_name("orders.csv")
    rows = build_rows()
    with out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
