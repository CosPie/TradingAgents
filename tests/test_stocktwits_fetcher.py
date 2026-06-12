"""Tests for StockTwits fetcher guardrails."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from tradingagents.dataflows import stocktwits


@pytest.mark.unit
class TestStockTwitsFetcher:
    def test_non_equity_alias_skips_network_fetch(self):
        with patch.object(stocktwits, "urlopen") as fetch:
            out = stocktwits.fetch_stocktwits_messages("XAU")
        fetch.assert_not_called()
        assert "stocktwits skipped for XAU" in out
        assert "GC=F" in out

    def test_plain_equity_still_fetches(self):
        payload = b'{"messages":[]}'

        class _Resp:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return payload

        with patch.object(stocktwits, "urlopen", return_value=_Resp()) as fetch:
            out = stocktwits.fetch_stocktwits_messages("NVDA")
        fetch.assert_called_once()
        assert "no StockTwits messages found for $NVDA" in out
