from app.etl.currency_etl import (
    transform_currency
)


def test_transform_currency():

    sample = {

        "base_code": "USD",

        "conversion_rates": {

            "KES": 129.5
        }
    }

    result = transform_currency(
        sample,
        "KES"
    )

    assert (
        result["base_currency"]
        == "USD"
    )

    assert (
        result["target_currency"]
        == "KES"
    )

    assert (
        result["exchange_rate"]
        == 129.5
    )