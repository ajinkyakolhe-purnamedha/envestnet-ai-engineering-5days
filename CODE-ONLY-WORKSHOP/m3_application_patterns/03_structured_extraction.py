from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, parse_json_object, print_json


@dataclass
class TradeRequest:
    ticker: str
    allocation_pct: float

    @classmethod
    def from_model(cls, value: dict[str, object]) -> "TradeRequest":
        return cls(ticker=str(value["ticker"]).upper(), allocation_pct=float(value["allocation_pct"]))


def main() -> None:
    raw = chat([{"role": "user", "content": "Extract trade request as JSON only: ticker and allocation_pct. Text: Move AAPL to 36%."}], 40)
    print("Raw model text:", raw)
    value = parse_json_object(raw)
    if value is None:
        print("Schema result: invalid JSON from model")
        return
    try:
        request = TradeRequest.from_model(value)
    except (KeyError, TypeError, ValueError) as error:
        print("Schema result:", error)
        return
    print_json("Schema-valid request", request.__dict__)
    print("Business rule (<= 35%):", request.allocation_pct <= 35)


if __name__ == "__main__":
    main()
