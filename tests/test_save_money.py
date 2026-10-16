"""save_money.py and the game's display currency (copied from the ETS2 project, report of 10.10.2026).

ATS keeps money in US dollars. The game shows it in the currency chosen in the
profile (config.cfg of the profile: uset g_currency "N", an index into the
currency list of def/economy_data.sii: 0 USD, 1 CAD, 2 MXN, 3 EUR in ATS 1.61).
--set takes the amount as the game shows it and the tool prints both: USD in
the file and the amount on screen. --set-usd writes USD as is. The numbers below
use Mexican pesos (index 2, ratio 17.156) - the only ATS currency far from the dollar.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import save_money  # noqa: E402

TEXT = ("SiiNunit\n{\neconomy : _nameless.1 {\n bank: _nameless.2\n experience_points: 44339\n}\n\n"
        "bank : _nameless.2 {\n money_account: 50000000\n coinsurance_fixed: 0\n}\n}\n")

ECONOMY = """SiiNunit
{
economy_data : economy.data.storage
{
	currency_code[]: "USD"
	currency_ratio[]: 1
	currency_sign1[]: ""
	currency_sign2[]: "$"
	currency_sign3[]: ""

	currency_code[]: "CAD"
	currency_ratio[]: 1.3909
	currency_sign1[]: ""
	currency_sign2[]: "$"
	currency_sign3[]: ""

	currency_code[]: "MXN"
	currency_ratio[]: 17.156
	currency_sign1[]: ""
	currency_sign2[]: "$"
	currency_sign3[]: ""
}
}
"""


class CurrencyTest(unittest.TestCase):
    def test_parse_currency_list(self):
        cur = save_money.parse_currencies(ECONOMY)
        self.assertEqual([c["code"] for c in cur], ["USD", "CAD", "MXN"])
        self.assertAlmostEqual(cur[2]["ratio"], 17.156)
        self.assertEqual(cur[2]["sign2"], "$")

    def test_builtin_table_matches_1_61(self):
        cur = save_money.BUILTIN_CURRENCIES
        self.assertEqual([c["code"] for c in cur], ["USD", "CAD", "MXN", "EUR"])
        self.assertAlmostEqual(cur[2]["ratio"], 17.156)

    def test_builtin_table_matches_the_installed_game(self):
        if not os.path.isfile(os.path.join(save_money.GAME_DIR, "def.scs")):
            self.skipTest("ATS not installed")
        game = save_money.game_currencies()
        self.assertEqual([(c["code"], c["ratio"]) for c in game],
                         [(c["code"], c["ratio"]) for c in save_money.BUILTIN_CURRENCIES])

    def test_pesos(self):
        mxn = save_money.BUILTIN_CURRENCIES[2]
        self.assertEqual(save_money.to_screen(50000000, mxn), 857800000)
        self.assertEqual(save_money.from_screen(857800000, mxn), 50000000)
        self.assertEqual(save_money.from_screen(50000000, mxn), 2914432)
        usd = save_money.BUILTIN_CURRENCIES[0]
        self.assertEqual(save_money.from_screen(50000000, usd), 50000000)

    def test_profile_currency_index(self):
        d = tempfile.mkdtemp(prefix="atscur_")
        try:
            self.assertEqual(save_money.profile_currency_index(d), 0)      # no config.cfg: USD
            with open(os.path.join(d, "config.cfg"), "w", encoding="utf-8") as fh:
                fh.write('uset g_lang "ru_ru"\nuset g_currency "2"\n')
            self.assertEqual(save_money.profile_currency_index(d), 2)
        finally:
            shutil.rmtree(d)


class CommandLineTest(unittest.TestCase):
    """End to end on a throw-away profile folder: --set in the screen currency, read back."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="atsmoney_")
        self.prof = os.path.join(self.tmp, "414C6578")
        os.makedirs(os.path.join(self.prof, "save", "autosave"))
        with open(os.path.join(self.prof, "save", "autosave", "game.sii"), "w", encoding="utf-8") as fh:
            fh.write(TEXT)
        with open(os.path.join(self.prof, "config.cfg"), "w", encoding="utf-8") as fh:
            fh.write('uset g_currency "2"\n')
        self.backups = os.path.join(self.tmp, "backups")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_tool(self, *args):
        cmd = [sys.executable, os.path.join(ROOT, "tools", "save_money.py"),
               "--profile-dir", self.prof, "--backup-dir", self.backups] + list(args)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def money_in_file(self):
        kind, _raw, money, _w = save_money.read_money(os.path.join(self.prof, "save", "autosave", "game.sii"))
        return money

    def test_show_both_currencies(self):
        out = self.run_tool("--save", "autosave")
        self.assertIn("50,000,000 USD", out)
        self.assertIn("857,800,000 MXN", out)

    def test_set_in_screen_currency(self):
        out = self.run_tool("--save", "autosave", "--set", "1000000000", "--apply")
        self.assertEqual(self.money_in_file(), 58288645)          # 1e9 / 17.156 = 58,288,645.4
        self.assertIn("1,000,000,000 MXN", out)
        self.assertIn("58,288,645 USD", out)
        self.assertTrue(os.listdir(os.path.join(self.backups, "414C6578")))
        # impossible to miss (report 10.10: a dry run was taken for a write)
        self.assertIn("WRITTEN: 58,288,645 USD in the file = 999,999,994 MXN on screen", out)
        self.assertIn("Now start the game and load the latest save", out)
        self.assertNotIn("NOTHING WRITTEN", out)

    def test_set_usd(self):
        self.run_tool("--save", "autosave", "--set-usd", "70000000", "--apply")
        self.assertEqual(self.money_in_file(), 70000000)

    def test_dry_run_writes_nothing(self):
        out = self.run_tool("--save", "autosave", "--set", "1000000000")
        self.assertEqual(self.money_in_file(), 50000000)
        self.assertIn("NOTHING WRITTEN", out)
        self.assertIn("add --apply", out)
        self.assertNotIn("WRITTEN:", out)
        self.assertFalse(os.path.exists(self.backups))

    def test_save_latest(self):
        older = os.path.join(self.prof, "save", "1")
        os.makedirs(older)
        with open(os.path.join(older, "game.sii"), "w", encoding="utf-8") as fh:
            fh.write(TEXT)
        os.utime(os.path.join(older, "game.sii"), (1600000000, 1600000000))
        out = self.run_tool("--save", "latest", "--set-usd", "777", "--apply")
        self.assertIn("latest save: autosave", out)
        self.assertEqual(self.money_in_file(), 777)
        kind, _raw, money, _w = save_money.read_money(os.path.join(older, "game.sii"))
        self.assertEqual(money, 50000000)

    def test_currency_override(self):
        out = self.run_tool("--save", "autosave", "--currency", "USD", "--set", "123456", "--apply")
        self.assertEqual(self.money_in_file(), 123456)
        self.assertIn("123,456 USD", out)


INFO = ("SiiNunit\n{\nsave_container : _nameless.1 {\n name: \"\"\n file_time: 1700000000\n"
        " info_players_experience: 1\n info_money_account: %d\n info_explored_ratio: 0.1\n}\n}\n")


class SaveFolderTest(unittest.TestCase):
    """Independent review of 16.10.2026, checked on a copy of a real ETS2 1.61 profile.

    1. The game names its saves autosave, autosave_job, autosave_job_1..9, autosave_drive,
       autosave_drive_1..9. --restore --save autosave looked for backups "autosave_*" and took
       the last one by name - "autosave_job_3_<time>" sorts after "autosave_<time>", so the
       backup of ANOTHER save was copied into autosave.
    2. The money is also in info.sii of the save (info_money_account, what the Load screen
       shows). In every real save it equals the bank's money_account. The tool wrote only
       game.sii, so the Load screen kept showing the old amount - it looked as if nothing had
       been written.
    3. Two writes of the same save within one second: the backup folder name (to the second)
       already existed and the second write failed.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="atsfold_")
        self.prof = os.path.join(self.tmp, "414C6578")
        self.backups = os.path.join(self.tmp, "backups")
        for name, money in (("autosave", 50000000), ("autosave_job_3", 3333), ("autosave_drive", 4444)):
            d = os.path.join(self.prof, "save", name)
            os.makedirs(d)
            with open(os.path.join(d, "game.sii"), "w", encoding="utf-8") as fh:
                fh.write(TEXT.replace("50000000", str(money)))
            with open(os.path.join(d, "info.sii"), "w", encoding="utf-8") as fh:
                fh.write(INFO % money)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def money(self, save):
        return save_money.read_money(os.path.join(self.prof, "save", save, "game.sii"))[2]

    def info_money(self, save):
        with open(os.path.join(self.prof, "save", save, "info.sii"), encoding="utf-8") as fh:
            return int(re.search(r"info_money_account:\s*(-?\d+)", fh.read()).group(1))

    def cli(self, *args):
        cmd = [sys.executable, os.path.join(ROOT, "tools", "save_money.py"),
               "--profile-dir", self.prof, "--backup-dir", self.backups] + list(args)
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def test_restore_takes_the_backup_of_the_same_save(self):
        self.cli("--save", "autosave", "--set-usd", "111", "--apply")
        # later backups of saves whose names start with "autosave_"
        for other in ("autosave_job_3", "autosave_drive"):
            src = os.path.join(self.prof, "save", other)
            shutil.copytree(src, os.path.join(self.backups, "414C6578", other + "_20991231-235959"))
        out = self.cli("--save", "autosave", "--restore")
        self.assertEqual(self.money("autosave"), 50000000, out)      # its own money, not 3333/4444
        self.assertIn(os.sep + "autosave_2", out)

    def test_info_sii_follows_the_money(self):
        save_money.write_money(self.prof, "autosave", 106393165, self.backups)
        self.assertEqual(self.money("autosave"), 106393165)
        self.assertEqual(self.info_money("autosave"), 106393165)
        self.assertEqual(self.info_money("autosave_job_3"), 3333)    # other saves untouched

    def test_save_without_info_sii(self):
        os.remove(os.path.join(self.prof, "save", "autosave", "info.sii"))
        save_money.write_money(self.prof, "autosave", 777, self.backups)
        self.assertEqual(self.money("autosave"), 777)

    def test_two_writes_in_one_second(self):
        a = save_money.write_money(self.prof, "autosave", 1, self.backups)[2]
        b = save_money.write_money(self.prof, "autosave", 2, self.backups)[2]
        self.assertNotEqual(a, b)
        self.assertEqual(self.money("autosave"), 2)
        # both backups are real copies of what was there before each write
        self.assertEqual(save_money.read_money(os.path.join(a, "game.sii"))[2], 50000000)
        self.assertEqual(save_money.read_money(os.path.join(b, "game.sii"))[2], 1)


if __name__ == "__main__":
    unittest.main()
