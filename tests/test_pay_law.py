"""Job pay law for ATS: "x10 really x10" (copied from the ETS2 project, report of 10.10.2026).

In ETS2 Big Money 1.0-1.1 set revenue_per_km_base 15 -> 150 and the freight
market paid as before. The delivery log of a 1.61 save showed how the engine
pays a job:
    pay ~= fixed + distance * units * unit_reward_per_km * revenue_coef * bonuses
where revenue_coef is revenue_coef_per_km (freight market), cargo_market_...
(cargo market), driver_revenue_coef_per_km (quick jobs, hired drivers) or
driver_cargo_market_... (hired drivers on the cargo market). revenue_per_km_base
is not a factor. ATS 1.61 is the same engine and has the same keys in
def/economy_data.sii, but its own stock values (driver_cargo_market 0.77, not
0.70 as in ETS2) - so the ATS mod multiplies the values read from the installed
game by 10 ("scale": 10), it does not copy the ETS2 numbers.

The first class needs neither the game nor a save; the second reads the ATS
files and the built mod.
"""

import json
import os
import re
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import build_mods  # noqa: E402

PAY_KEYS = ("revenue_coef_per_km", "cargo_market_revenue_coef_per_km", "driver_revenue_coef_per_km",
            "driver_cargo_market_revenue_coef_per_km", "fixed_revenue")
# def/economy_data.sii of ATS 1.61.3.18 (read 16.10.2026)
ATS_STOCK = {"revenue_coef_per_km": 0.9, "cargo_market_revenue_coef_per_km": 1.0,
             "driver_revenue_coef_per_km": 0.67, "driver_cargo_market_revenue_coef_per_km": 0.77,
             "fixed_revenue": 600.0}
GAME = build_mods.DEFAULT_GAME
HAVE_GAME = os.path.isfile(os.path.join(GAME, "def.scs"))


def money_patches():
    with open(os.path.join(ROOT, "mods", "money", "mod.json"), encoding="utf-8") as fh:
        spec = json.load(fh)
    return {p["key"]: p for p in spec["patches"]["def/economy_data.sii"]}


def value(text, key):
    found = re.findall(r"^\s*%s\s*:\s*([^#\s]+)" % re.escape(key), text, re.M)
    if len(found) != 1:
        raise AssertionError("%s: %d lines" % (key, len(found)))
    return float(found[0])


class BigMoneySpecTest(unittest.TestCase):
    def test_scales_every_pay_key_x10(self):
        p = money_patches()
        self.assertEqual(sorted(p), sorted(PAY_KEYS))
        for key in PAY_KEYS:
            self.assertEqual(p[key].get("scale"), 10, key)
            self.assertNotIn("value", p[key], key)          # no fixed ETS2 number

    def test_does_not_touch_revenue_per_km_base(self):
        self.assertNotIn("revenue_per_km_base", money_patches())


@unittest.skipUnless(HAVE_GAME, "ATS not installed")
class BigMoneyOnGameFilesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        defs = build_mods.LayeredFs(GAME)
        cls.stock = defs.read("def/economy_data.sii").decode("utf-8-sig")
        cls.stock_start = defs.read("def/initial_save/normal/game.sii").decode("utf-8-sig")
        res = build_mods.build_all(GAME, tempfile.mkdtemp(prefix="atspay_"), verbose=False)
        cls.econ = res["money"]["files"]["def/economy_data.sii"].decode("utf-8")
        cls.start = res["money"]["files"]["def/initial_save/normal/game.sii"].decode("utf-8")

    def test_stock_values_are_the_ats_ones(self):
        """If a game update changes them, this fails and the texts (0.77 -> 7.7 ...) need a look."""
        for key, v in ATS_STOCK.items():
            self.assertAlmostEqual(value(self.stock, key), v, places=6, msg=key)

    def test_built_pay_is_exactly_ten_times_stock(self):
        for key in PAY_KEYS:
            old, new = value(self.stock, key), value(self.econ, key)
            self.assertGreater(old, 0, key)
            self.assertAlmostEqual(new, old * 10, places=6, msg=key)

    def test_revenue_per_km_base_stays(self):
        self.assertEqual(value(self.econ, "revenue_per_km_base"), value(self.stock, "revenue_per_km_base"))

    def test_new_profile_start_money(self):
        self.assertEqual(value(self.stock_start, "money_account"), 1500)      # ATS: $1,500 (ETS2: 2,000 EUR)
        self.assertEqual(value(self.start, "money_account"), 10000000)


if __name__ == "__main__":
    unittest.main()
