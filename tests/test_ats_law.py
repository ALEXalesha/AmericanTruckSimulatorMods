"""Every mod on the files of the INSTALLED ATS: the changed parameter exists in this game
version and really changes (the "x10 really x10" law of the ETS2 project, per mod).

The differences from ETS2 found on ATS 1.61.3.18 (16.10.2026) are pinned here too:
no secondary_torque, no recharge_* and no ferries, 33 of 173 engines already have
consumption_coef, max_vehicle_count is set (not commented out), most tyres have no
roll_resistance line. If an update changes one of them, a test here fails first.
"""

import os
import re
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import build_mods  # noqa: E402

GAME = build_mods.DEFAULT_GAME
HAVE_GAME = os.path.isfile(os.path.join(GAME, "def.scs"))
ENGINES = "def/vehicle/truck/*/engine/*.sii"
TRANS = "def/vehicle/truck/*/transmission/*.sii"


def vals(text, key):
    return [m.group(1) for m in re.finditer(r"^\s*%s\s*:\s*([^#\s]+)" % re.escape(key), text, re.M)]


def one(text, key):
    v = vals(text, key)
    if len(v) != 1:
        raise AssertionError("%s: %d lines, expected 1" % (key, len(v)))
    return float(v[0])


def units(text, cls):
    return len(re.findall(r"^\s*%s\s*:" % cls, text, re.M))


@unittest.skipUnless(HAVE_GAME, "ATS not installed")
class AtsLawTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defs = build_mods.LayeredFs(GAME)
        cls.res = build_mods.build_all(GAME, tempfile.mkdtemp(prefix="atslaw_"), verbose=False)

    def stock(self, path):
        return self.defs.read(path).decode("utf-8-sig")

    def built(self, mod, path):
        return self.res[mod]["files"][path].decode("utf-8")

    def changed(self, mod, path, key, new):
        """key is in the stock file once, its stock value differs from new, the mod has new."""
        old = one(self.stock(path), key)
        self.assertNotAlmostEqual(old, float(new), places=9, msg="%s %s: stock already %s" % (mod, key, old))
        self.assertEqual(one(self.built(mod, path), key), float(new), "%s %s" % (mod, key))

    # ---- version
    def test_built_for_this_game_version(self):
        v = build_mods.game_version(GAME)
        self.assertTrue(v.startswith("1.61."), v)       # the texts say 1.61; check them after an update
        self.assertEqual(self.res["money"]["version_glob"], "1.61.*")

    # ---- Big Money: tests/test_pay_law.py (x10 of the stock values)

    # ---- Free Services
    def test_free_services(self):
        econ = "def/economy_data.sii"
        for key, new in (("tow_price_base", 0), ("tow_price_factor", 0), ("refuel_price_base", 0),
                         ("refuel_price_factor", 0)):
            self.changed("free_services", econ, key, new)
        for key in ("truck_restore_accessory_fixed_price", "truck_restore_accessory_price_coef",
                    "trailer_restore_accessory_fixed_price", "trailer_restore_accessory_price_coef"):
            self.changed("free_services", "def/service_data.sii", key, 0)
        states = build_mods.expand_path(self.defs, "def/country/*.sui")
        self.assertEqual(len(states), 22)
        for p in states:
            old = one(self.stock(p), "fuel_price")
            self.assertGreater(old, 0.1, p)                               # dollars per litre
            self.assertEqual(one(self.built("free_services", p), "fuel_price"), 0.0001, p)

    def test_ats_has_no_charging_and_no_ferries(self):
        """The ETS2 mod also zeroes recharge_* and the ferry prices; ATS 1.61 has neither."""
        econ = self.stock("def/economy_data.sii")
        self.assertEqual(vals(econ, "recharge_price_base") + vals(econ, "recharge_price"), [])
        with self.assertRaises(build_mods.PatchError):
            build_mods.expand_path(self.defs, "def/ferry/connection/*.sii")

    # ---- No Sleep
    def test_no_sleep(self):
        self.assertEqual(one(self.stock("def/economy_data.sii"), "maximum_driving_time"), 840)   # 14 h
        self.changed("no_sleep", "def/economy_data.sii", "maximum_driving_time", 10000000)

    # ---- No Fines
    def test_no_fines(self):
        police = "def/police_data.sii"
        stock = self.stock(police)
        built = self.built("no_fines", police)
        for key in ("fine_amounts", "offence_probabilty", "offence_police_probabilty"):
            old = [float(m) for m in re.findall(r"^\s*%s\[\d+\]\s*:\s*([^#\s]+)" % key, stock, re.M)]
            new = [float(m) for m in re.findall(r"^\s*%s\[\d+\]\s*:\s*([^#\s]+)" % key, built, re.M)]
            self.assertEqual(len(old), 14, key)
            self.assertEqual(new, [0.0] * 14, key)
            self.assertGreater(max(old), 0, key)
        for key in ("fine_factor_base", "fine_factor_step"):
            self.changed("no_fines", police, key, 0)
        econ = "def/economy_data.sii"
        for key in ("abandoned_job_fine", "cargo_damage_cost", "cargo_damage_cost_factor"):
            self.changed("no_fines", econ, key, 0)
        late = re.findall(r"^\s*late_delivery_max_overtime\[\d+\]\s*:\s*(\d+)", self.built("no_fines", econ), re.M)
        self.assertEqual(late, ["43200"] * 3)

    # ---- No Damage
    def test_no_damage(self):
        for key in ("truck_damage_coef", "trailer_damage_coef", "dragged_trailer_damage_coef",
                    "truck_to_trailer_dmg", "cargo_damage_ratio", "engine_wear", "transmission_wear",
                    "wheel_wear", "engine_wear_unfixable", "transmission_wear_unfixable",
                    "wheel_wear_unfixable", "trailer_wheel_wear", "trailer_wheel_wear_unfixable"):
            self.changed("no_damage", "def/damage_data.sii", key, 0)

    # ---- No Rollover
    def test_no_rollover(self):
        self.changed("no_rollover", "def/vehicle/physics.sii", "sway_bar_stiffness_factor", 3.0)

    # ---- More Traffic
    def test_more_traffic_sets_the_existing_limit(self):
        """ATS sets max_vehicle_count: 50 (ETS2 has it commented out): change it, do not add a second line."""
        self.changed("more_traffic", "def/traffic_data.sii", "max_vehicle_count", 300)

    # ---- No Fuel
    def test_no_fuel_sets_or_adds_consumption_coef(self):
        engines = build_mods.expand_path(self.defs, ENGINES, "accessory_engine_data")
        self.assertEqual(len(engines), 173)
        had = 0
        for p in engines:
            stock, built = self.stock(p), self.built("no_fuel", p)
            self.assertEqual(units(stock, "accessory_engine_data"), 1, p)
            old = vals(stock, "consumption_coef")
            if old:
                had += 1
                self.assertNotEqual(float(old[0]), 0.0001, p)
            self.assertEqual(vals(built, "consumption_coef"), ["0.0001"], p)   # exactly one line
        self.assertEqual(had, 33)

    # ---- Super Power / Hyper Power
    def check_torque(self, mod, factor):
        engines = build_mods.expand_path(self.defs, ENGINES, "accessory_engine_data")
        for p in engines:
            old = one(self.stock(p), "torque")
            self.assertGreater(old, 0, p)
            self.assertAlmostEqual(one(self.built(mod, p), "torque"), old * factor, delta=1.0, msg=p)
            self.assertEqual(vals(self.stock(p), "secondary_torque"), [], p)   # none in ATS 1.61

    def test_super_power(self):
        self.check_torque("super_power", 3)
        self.changed("super_power", "def/vehicle/physics.sii", "air_resistance", 1.5)
        self.changed("super_power", "def/vehicle/physics.sii", "brake_torque_factor", 2.0)

    def test_power_mods_lift_the_65mph_cap(self):
        """Алексей 24.10: Hyper/Super Power упирались в 104 км/ч. Это truck_speed_limit 104.607 (65 mph)
        в def/game_data.sii - жёсткий потолок грузовика игрока, опция ограничителя его не снимает."""
        self.assertAlmostEqual(one(self.stock("def/game_data.sii"), "truck_speed_limit"), 104.607, places=3)
        for mod in ("hyper_power", "super_power"):
            self.changed(mod, "def/game_data.sii", "truck_speed_limit", 1000)
        # above the gear-limited top speed of Hyper Power (~640 km/h with the longest gearbox)
        self.assertGreater(one(self.built("hyper_power", "def/game_data.sii"), "truck_speed_limit"), 700)

    def test_hyper_power(self):
        self.check_torque("hyper_power", 12)
        trans = build_mods.expand_path(self.defs, TRANS, "accessory_transmission_data")
        self.assertEqual(len(trans), 98)
        for p in trans:
            old = one(self.stock(p), "differential_ratio")
            self.assertAlmostEqual(one(self.built("hyper_power", p), "differential_ratio"), old * 0.35,
                                   delta=0.001, msg=p)
        phys = "def/vehicle/physics.sii"
        for key, new in (("air_resistance", 0.1), ("brake_torque_factor", 4.0), ("brake_cooling_rate", 0.05),
                         ("steering_sensitivity_multiplier_minimum", 0.1)):
            self.changed("hyper_power", phys, key, new)

    def test_hyper_power_grip_in_every_tyre(self):
        """ETS2 anchors grip_factor on roll_resistance; in ATS 21 of 24 tyres have none, so the
        line goes after price (every tyre has one)."""
        tyres = (build_mods.expand_path(self.defs, "def/vehicle/f_tire/*.sii", "accessory_wheel_data") +
                 build_mods.expand_path(self.defs, "def/vehicle/r_tire/*.sii", "accessory_wheel_data"))
        self.assertEqual(len(tyres), 24)
        no_roll = 0
        for p in tyres:
            stock = self.stock(p)
            no_roll += not vals(stock, "roll_resistance")
            self.assertEqual(vals(stock, "grip_factor"), [], p)
            self.assertEqual(vals(self.built("hyper_power", p), "grip_factor"), ["1.3"] * units(stock, "accessory_wheel_data"), p)
        self.assertGreaterEqual(no_roll, 20)


if __name__ == "__main__":
    unittest.main()
