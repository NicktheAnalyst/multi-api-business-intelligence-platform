import requests

from datetime import datetime

from app.database.db import SessionLocal

from app.database.models import Currency

from app.utils.logger import logger

from app.utils.config import (
    EXCHANGE_RATE_API_KEY
)


CURRENCY_PAIRS = [

    ("USD", "KES"),

    ("EUR", "KES"),

    ("GBP", "KES"),

    ("USD", "EUR")
]


def extract_currency_rate(base):

    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{EXCHANGE_RATE_API_KEY}/latest/{base}"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        logger.exception(
            f"Currency extraction failed: {base}"
        )

        return None
    

def transform_currency(
    data,
    target_currency
):

    if not data:
        return None

    return {

        "base_currency":
            data["base_code"],

        "target_currency":
            target_currency,

        "exchange_rate":
            data["conversion_rates"][
                target_currency
            ],

        "timestamp":
            datetime.utcnow()
    }


def validate_currency(data):

    if not data:
        return False

    if data["exchange_rate"] <= 0:
        return False

    return True


def load_currency(
    session,
    currency_data
):

    row = Currency(

        base_currency=
            currency_data[
                "base_currency"
            ],

        target_currency=
            currency_data[
                "target_currency"
            ],

        exchange_rate=
            currency_data[
                "exchange_rate"
            ],

        timestamp=
            currency_data[
                "timestamp"
            ]
    )

    session.add(row)


def run_currency_etl():

    logger.info(
        "Currency ETL started"
    )

    session = SessionLocal()

    try:

        inserted = 0

        processed_bases = {}

        for base, target in CURRENCY_PAIRS:

            if base not in processed_bases:

                processed_bases[
                    base
                ] = extract_currency_rate(
                    base
                )

            raw_data = processed_bases[
                base
            ]

            transformed = (
                transform_currency(
                    raw_data,
                    target
                )
            )

            if (
                transformed
                and validate_currency(
                    transformed
                )
            ):

                load_currency(
                    session,
                    transformed
                )

                inserted += 1

        session.commit()

        logger.info(
            f"Inserted {inserted} "
            f"currency records"
        )

    except Exception:

        session.rollback()

        logger.exception(
            "Currency ETL failed"
        )

    finally:

        session.close()

        logger.info(
            "Currency ETL finished"
        )



if __name__ == "__main__":

    run_currency_etl()           