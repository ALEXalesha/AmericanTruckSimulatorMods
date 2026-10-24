"""Checks for the Steam Workshop folders (tools/build_workshop.py). Needs the game and Pillow.

Rules from the SCS modding wiki (SCS Workshop Uploader validation):
upload root = versions.sii + version package only; manifest/icon/description
next to each other; icon JPG exactly 276x162, < 1 MB; description UTF-8 .txt,
< 1 MB; every .sii starts with "SiiNunit"; no unreferenced .txt/.jpg; no .scs.
Preview image 640x360 (SCS forum), Steam limit 1 MB.
"""

import json
import os
import re
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tests"))

import build_mods  # noqa: E402
from test_mods import HAVE_GAME, jpeg_size, values  # noqa: E402

CATEGORIES = {"truck", "trailer", "interior", "tuning_parts", "ai_traffic", "sound", "paint_job", "cargo_pack",
              "map", "ui", "weather_setup", "physics", "graphics", "models", "movers", "walkers", "prefabs", "other"}
MANIFEST_FIELDS = ["package_version", "author", "category", "icon", "description_file"]
# The SCS Workshop Uploader rejects these in Workshop packages (ERROR 00010 for compatible_versions,
# WARN 00002 for display_name): versions come from versions.sii and the name from the Steam page.
WORKSHOP_FORBIDDEN = ["compatible_versions", "display_name"]
# personal data that must never reach a public upload
def private_strings():
    """Personal strings that must never reach a public upload.

    None of them is written in this file (it is public itself): they come from the
    local git config (user.email, publish.privateName, publish.privateExtra), the
    Gitea remote, the folder this repository lives in and the Steam user/profile
    folders on this PC. On a machine without them only the generic checks remain.
    """
    import glob
    import subprocess

    def git(*args):
        try:
            return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True,
                                  text=True, encoding="utf-8").stdout.strip()
        except OSError:
            return ""

    out = {b"gmail.com", b"steam\\userdata", b"steam/userdata"}
    email = git("config", "user.email")
    if email:
        out.add(email.lower().encode())
    for word in (git("config", "publish.privateName") + " " +
                 git("config", "publish.privateExtra").replace("|", " ")).split():
        if len(word) >= 4:
            out.add(word.lower().encode("utf-8"))
    origin = git("remote", "get-url", "origin")
    # Only the Gitea HOST is private. The owner nick and the repo name are public: since
    # the rename the Gitea repo name equals the GitHub one, so it must not be flagged.
    m = re.match(r"^[a-z]+://([^/:]+)", origin)
    if m:
        out.add(m.group(1).lower().encode())
    parent = os.path.dirname(ROOT)
    for variant in (parent, parent.replace("\\", "/")):
        out.add(variant.lower().encode())
    for d in glob.glob(r"C:\Program Files (x86)\Steam\userdata\*"):
        out.add(os.path.basename(d).lower().encode())
        for prof in glob.glob(os.path.join(d, "270880", "remote", "profiles", "*")):
            out.add(os.path.basename(prof).lower().encode())
    return sorted(x for x in out if len(x) >= 4)


FORBIDDEN = private_strings()
ZERO_KEYS = ["fuel_price", "consumption_coef", "air_resistance", "differential_ratio", "grip_factor",
             "brake_torque_factor", "torque", "steering_sensitivity_multiplier_minimum"]

_DIRS = []


def rb(path):
    with open(path, "rb") as fh:
        return fh.read()


def rt(path):
    return rb(path).decode("utf-8")


def folders():
    if not _DIRS:
        import build_workshop
        out = tempfile.mkdtemp(prefix="atsws_test_")
        _DIRS.extend(build_workshop.build(out, verbose=False))
    return _DIRS


@unittest.skipUnless(HAVE_GAME, "game not installed")
class WorkshopTest(unittest.TestCase):
    def test_one_folder_per_mod(self):
        self.assertEqual(len(folders()), len(build_mods.load_order()))

    def test_public_names_are_not_private(self):
        """After the Gitea rename the repo name equals the public GitHub name: only the
        Gitea host is private, never the owner nick or the repo name."""
        for public in (b"americantrucksimulatormods", b"alexalesha",
                       b"github.com/alexalesha/americantrucksimulatormods"):
            self.assertFalse(any(bad in public for bad in FORBIDDEN), public)

    def test_layout(self):
        for base in folders():
            names = sorted(x for x in os.listdir(base) if x != "steam_changelog.txt")
            self.assertEqual(names, ["preview.jpg", "steam_description.txt", "steam_page.txt", "upload"])
            self.assertEqual(sorted(os.listdir(os.path.join(base, "upload"))), ["universal", "versions.sii"])
            v = rb(os.path.join(base, "upload", "versions.sii"))
            self.assertTrue(v.startswith(b"SiiNunit"))
            self.assertEqual(len(re.findall(rb"package_version_info\s*:\s*\.universal", v)), 1)
            self.assertIn(b'package_name: "universal"', v)

    def test_manifest_icon_description(self):
        for base in folders():
            uni = os.path.join(base, "upload", "universal")
            man = rt(os.path.join(uni, "manifest.sii"))
            self.assertTrue(man.startswith("SiiNunit"))
            for f in MANIFEST_FIELDS:
                self.assertRegex(man, r"(?m)^\s*%s(\[\])?\s*:" % f, "%s: %s missing" % (base, f))
            for c in re.findall(r'category\[\]\s*:\s*"([^"]+)"', man):
                self.assertIn(c, CATEGORIES)
            for f in WORKSHOP_FORBIDDEN:
                self.assertNotRegex(man, r"(?m)^\s*%s(\[\])?\s*:" % f, "%s: %s must not be in a Workshop manifest" % (base, f))
            icon = rb(os.path.join(uni, "mod_icon.jpg"))
            self.assertEqual(jpeg_size(icon), (276, 162))
            self.assertLess(len(icon), 1024 * 1024)
            desc = rb(os.path.join(uni, "mod_description.txt"))
            self.assertLess(len(desc), 1024 * 1024)
            text = desc.decode("utf-8")
            self.assertIn("1.61", text)
            self.assertIn("-----", text)            # EN part, then RU part
            self.assertRegex(text, "[а-яА-Я]")
            prev = rb(os.path.join(base, "preview.jpg"))
            self.assertEqual(jpeg_size(prev), (640, 360))
            self.assertLess(len(prev), 1024 * 1024)
            page = rt(os.path.join(base, "steam_page.txt"))
            self.assertGreater(len(page.split("DESCRIPTION", 1)[1]), 50)

    def test_paste_files_crlf(self):
        # The uploader's description box is a plain Windows edit field: a bare LF is dropped
        # on paste and the whole text becomes one paragraph. Files meant for copy-paste use CRLF.
        for base in folders():
            for name in ("steam_page.txt", "steam_description.txt"):
                data = rb(os.path.join(base, name))
                self.assertGreater(data.count(b"\n"), 5, name)
                self.assertEqual(data.count(b"\n"), data.count(b"\r\n"), "%s: bare LF in %s" % (base, name))
            only = rt(os.path.join(base, "steam_description.txt"))
            self.assertTrue(only.startswith("[b]"), base)      # just the text, nothing to cut off
            self.assertIn("\r\n\r\n", only)
            self.assertIn("-----", only)
            self.assertIn(only, rt(os.path.join(base, "steam_page.txt")))

    def test_change_note_exactly_for_updated_mods(self):
        """1.0.0 items were "Create new" (no note). A mod whose version moved past 1.0.0 is an
        Update and needs steam_changelog.txt with its own version's note; nobody else gets one."""
        import build_workshop
        order = build_mods.load_order()
        for i, name in enumerate(order):
            base = [b for b in folders() if os.path.basename(b) == build_workshop.folder_name(i, name)][0]
            version = build_mods.load_spec(name)["version"]
            note = os.path.join(base, "steam_changelog.txt")
            if version == "1.0.0":
                self.assertFalse(os.path.exists(note), name)
            else:
                self.assertTrue(os.path.exists(note), name)
                self.assertIn(version, rt(note), name)

    def test_other_authors_line_names_every_replaced_file(self):
        """Алексей 24.10 («только написать в описаниях»): каждый мод честно пишет, какие файлы игры
        заменяет целиком - чужой мод с тем же файлом перекрывает его. Строка строится из mod.json,
        поэтому не отстаёт от сборки; у каждого шаблона пути - человеческое имя, не «*»."""
        import build_workshop
        order = build_mods.load_order()
        for i, name in enumerate(order):
            base = [b for b in folders() if os.path.basename(b) == build_workshop.folder_name(i, name)][0]
            text = rt(os.path.join(base, "upload", "universal", "mod_description.txt"))
            for lang, head in (("en", "Other authors' mods"), ("ru", "Моды других авторов")):
                files = build_workshop.replaced_files(name, lang)
                self.assertTrue(files, name)
                for f in files:
                    self.assertNotIn("*", f, "%s: no human name for %s" % (name, f))
                line = [l for l in text.splitlines() if l.startswith(head)]
                self.assertEqual(len(line), 1, "%s %s" % (name, lang))
                for f in files:
                    self.assertIn(f, line[0], "%s %s" % (name, lang))

    def test_texts_are_for_ats(self):
        """The texts came from the ETS2 project: no euro, no 36 countries, no ferries promised,
        the ATS numbers (0.77 -> 7.7, $1,500, 22 states, 177 engines, 181 gearboxes)."""
        all_text = ""
        for base in folders():
            all_text += rt(os.path.join(base, "upload", "universal", "mod_description.txt"))
        for bad in ("€", "EUR", "Euro Truck", "36 countries", "36 стран", "Ла-Манш", "Channel",
                    "203 engines", "170 gearboxes", "DAF", "Scania", "Iveco"):
            self.assertNotIn(bad, all_text, bad)
        for good in ("0.77 -> 7.7", "$1,500", "1500 $", "22 states", "22 штатах", "177 engines",
                     "181 gearboxes", "American Truck Simulator/config.cfg", "840"):
            self.assertIn(good, all_text, good)

    def test_files_valid_for_uploader(self):
        for base in folders():
            uni = os.path.join(base, "upload", "universal")
            for dp, _dn, fn in os.walk(uni):
                for f in fn:
                    p = os.path.join(dp, f)
                    rel = os.path.relpath(p, uni).replace("\\", "/")
                    self.assertFalse(f.endswith(".scs"), rel)
                    if f.endswith((".txt", ".jpg")):
                        self.assertIn(rel, ("mod_icon.jpg", "mod_description.txt"), "unreferenced " + rel)
                    if f.endswith(".sii"):
                        self.assertTrue(rb(p).startswith(b"SiiNunit"), rel)
                    self.assertTrue(f.endswith((".sii", ".sui", ".txt", ".jpg")), rel)

    def test_no_zero_divisors(self):
        for base in folders():
            for dp, _dn, fn in os.walk(os.path.join(base, "upload")):
                for f in fn:
                    if f.endswith((".sii", ".sui")):
                        text = rt(os.path.join(dp, f))
                        for k in ZERO_KEYS:
                            for v in values(text, k):
                                self.assertGreater(float(v), 0.0, "%s %s %s" % (base, f, k))

    def test_release_assets(self):
        import zipfile
        import build_workshop
        out = tempfile.mkdtemp(prefix="atsrel_test_")
        assets = build_workshop.release_assets(folders(), out)
        scs = [a for a in assets if a.endswith(".scs")]
        self.assertEqual(len(scs), len(folders()))
        for a in scs:
            self.assertTrue(os.path.basename(a).startswith("OpenRoad_"))
            with zipfile.ZipFile(a) as z:
                names = z.namelist()
                self.assertIn("manifest.sii", names)
                man = z.read("manifest.sii").decode("utf-8")
                # installed locally, so the Mod Manager fields are back
                self.assertRegex(man, r'display_name: "OpenRoad: [^"]+"')
                self.assertIn('compatible_versions[]: "1.61.*"', man)
                self.assertTrue(man.startswith("SiiNunit") and man.rstrip().endswith("}"))
                self.assertFalse([n for n in names if n.endswith("/") or "\\" in n])
                for n in names:
                    for bad in FORBIDDEN:
                        self.assertNotIn(bad, z.read(n).lower(), "%s:%s" % (a, n))
        self.assertTrue(any(a.endswith("OpenRoad_Workshop_Folders.zip") for a in assets))
        # every asset is free of personal data (names too). The money tool is code: it
        # names the generic Steam userdata folder, so only the real personal strings count.
        for a in assets:
            if a.endswith(".zip"):
                bads = FORBIDDEN
                if a.endswith(build_workshop.MONEY_ZIP):
                    bads = [b for b in FORBIDDEN if not b.startswith(b"steam")]
                with zipfile.ZipFile(a) as z:
                    for n in z.namelist():
                        blob = n.lower().encode("utf-8") + b"\n" + z.read(n).lower()
                        for bad in bads:
                            self.assertNotIn(bad, blob, "%s:%s" % (a, n))

    def test_mods_zip(self):
        """OpenRoad_ATS_Mods.zip: the same ten .scs and the install note with the load order."""
        import zipfile
        import build_workshop
        out = tempfile.mkdtemp(prefix="atsrel_test_")
        assets = build_workshop.release_assets(folders(), out)
        mz = [a for a in assets if a.endswith(build_workshop.MODS_ZIP)]
        self.assertEqual(len(mz), 1)
        with zipfile.ZipFile(mz[0]) as z:
            names = z.namelist()
            scs = sorted(n for n in names if n.endswith(".scs"))
            self.assertEqual(scs, sorted(os.path.basename(a) for a in assets if a.endswith(".scs")))
            for n in scs:
                with open(os.path.join(out, n), "rb") as fh:
                    self.assertEqual(z.read(n), fh.read(), n)
            note = z.read("INSTALL - УСТАНОВКА.txt")
            self.assertNotIn(b"\n", note.replace(b"\r\n", b""))      # Windows line ends
            text = note.decode("utf-8")
            pos = [text.index(ws_title) for ws_title in
                   [build_workshop.ws(n)["title"] for n in build_mods.load_order()]]
            self.assertEqual(pos, sorted(pos))                      # the load order, top first
            self.assertIn("American Truck Simulator\\mod", text)

    def test_money_zip_runs(self):
        """ATS_Money_Tool.zip unpacked elsewhere: the tool starts (no missing module), the
        .bat files keep CRLF, and there is no .venv or project file it would rely on."""
        import subprocess
        import zipfile
        import build_workshop
        out = tempfile.mkdtemp(prefix="atsmoney_test_")
        path = build_workshop.money_zip(out)
        dest = tempfile.mkdtemp(prefix="atsmoney_unz_")
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            z.extractall(dest)
        for rel in build_workshop.MONEY_FILES + ["requirements.txt", "README - ПРОЧТИ.txt"]:
            self.assertIn(rel, names)
        for bat in ("Деньги ATS.bat", "money.bat"):
            data = open(os.path.join(dest, bat), "rb").read()
            self.assertNotIn(b"\n", data.replace(b"\r\n", b""), bat)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        for script in ("tools/money_menu.py", "tools/save_money.py"):
            r = subprocess.run([sys.executable, "-I", os.path.join(dest, script), "--help"],
                               cwd=dest, capture_output=True, text=True, encoding="utf-8", env=env)
            self.assertEqual(r.returncode, 0, script + "\n" + r.stderr)

    def test_steps_file(self):
        """The short upload guide: one row per mod with its folder and tag, Create new."""
        import build_workshop
        out = tempfile.mkdtemp(prefix="atssteps_test_")
        path = build_workshop.write_steps(out)
        data = open(path, "rb").read()
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        text = data.decode("utf-8")
        self.assertNotIn("{table}", text)
        self.assertIn("Create new", text)
        for i, n in enumerate(build_mods.load_order()):
            w = build_workshop.ws(n)
            row = [l for l in text.splitlines() if build_workshop.folder_name(i, n) in l]
            self.assertEqual(len(row), 1, n)
            self.assertIn(w["title"], row[0])
            self.assertTrue(row[0].rstrip().endswith(w["type_tag"]), row[0])
        for bad in FORBIDDEN:
            self.assertNotIn(bad, data.lower())

    def test_no_personal_data(self):
        for base in folders():
            for dp, _dn, fn in os.walk(base):
                for f in fn:
                    p = os.path.join(dp, f)
                    blob = (os.path.relpath(p, base) + "\n").encode("utf-8").lower() + rb(p).lower()
                    for bad in FORBIDDEN:
                        self.assertNotIn(bad, blob, "%s contains %r" % (p, bad))


if __name__ == "__main__":
    unittest.main()
