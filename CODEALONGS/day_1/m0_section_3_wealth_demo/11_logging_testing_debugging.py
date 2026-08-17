import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

selected_date = "2020-06-01"
logger.info("Selected %s price dated %s", "AAPL", selected_date)
print(f"Selected AAPL price dated {selected_date}")

# Run: python -m unittest wealth_demo.test_wealth_demo -v
# Use breakpoint() to pause locally, then read tracebacks from the bottom up.
breakpoint  # breakpoint() is available when you need an interactive inspection.
