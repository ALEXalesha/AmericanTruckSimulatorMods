# AmericanTruckSimulatorMods - OpenRoad mods for American Truck Simulator

Ten single-player mods for American Truck Simulator (game version 1.61) - the same as the [OpenRoad mods for ETS2](https://github.com/ALEXalesha/ETS2Mods) - with the tools that build them from the game's own files, plus "Деньги ATS.bat" / `money.bat` to set your money in a save.

[Русский](README.ru.md)

> Not affiliated with or endorsed by SCS Software. "American Truck Simulator" is a trademark of SCS Software. Fan mods for single player only; they do not work in TruckersMP or Convoy.

| Mod (release file) | What it does |
|---|---|
| OpenRoad: Hyper Power (`OpenRoad_Hyper_Power.scs`) | Extreme: torque x12, final drive x0.35 (gear-limited top speed about 540-640 km/h), almost no air drag, +30% grip, brakes x4. Instead of Super Power. |
| OpenRoad: Super Power (`OpenRoad_Super_Power.scs`) | Torque x3, half the air drag, brakes x2. Still drivable. |
| OpenRoad: Big Money (`OpenRoad_Big_Money.scs`) | Job pay x10; a new profile starts with $10,000,000. |
| OpenRoad: Free Services (`OpenRoad_Free_Services.scs`) | Fuel almost free ($0.0001/l) in all 22 states, free towing, emergency refuel and wear restore. |
| OpenRoad: No Sleep (`OpenRoad_No_Sleep.scs`) | The driver never gets tired. |
| OpenRoad: No Fuel (`OpenRoad_No_Fuel.scs`) | Engines use 1/10000 of the fuel. |
| OpenRoad: No Fines (`OpenRoad_No_Fines.scs`) | No police or camera fines, no cancel fine, cargo damage does not cut the pay, 30 days for late jobs. |
| OpenRoad: No Rollover (`OpenRoad_No_Rollover.scs`) | Front anti-roll bar 3x stiffer; plus the stability sliders in the options. |
| OpenRoad: No Damage (`OpenRoad_No_Damage.scs`) | No damage, no wear, no cargo damage. |
| OpenRoad: More Traffic (`OpenRoad_More_Traffic.scs`) | AI vehicle limit 50 -> 300; the density is the game variable `g_traffic`. |

## Install

- **Steam Workshop:** subscribe to the OpenRoad mods for ATS and enable them in the Mod Manager.
- **From a release:** put the `.scs` files into `Documents\American Truck Simulator\mod` and enable them in the Mod Manager in the order below.

## Change money

1. Close the game completely.
2. Double-click **`Деньги ATS.bat`** (or **`money.bat`**, the same thing) in the repository folder. It asks in Russian.
3. It shows the profiles and the money **as the game shows it** (dollars, or pesos / Canadian dollars / euros if chosen in the options), asks for the new amount (`10000000`, `10 000 000` or `10 млн`), asks to close the game if it still runs, backs up the save and writes.
4. When it says **ЗАПИСАНО** (written), start the game and load the latest save.

Needs Python 3 and `py -m pip install -r tools\requirements.txt` (pycryptodome for encrypted saves). The same in one command:

```
python tools/save_money.py --save latest --set 10000000 --apply      # without --apply: dry run
python tools/save_money.py --save autosave --restore                 # put the last backup back
```

The save keeps money in US dollars; the game shows it in the profile's currency (`g_currency`: 0 USD, 1 CAD, 2 MXN, 3 EUR) with the rate of `def/economy_data.sii`. `--set` takes the amount as shown, `--set-usd` writes dollars as is. The amount goes into `game.sii` and `info.sii` (the Load screen). Backups: `Documents\American Truck Simulator\save_backups\`. A Steam Cloud profile (`Steam\userdata\<id>\270880\remote\profiles`) is uploaded by Steam at the next launch; if Steam shows a conflict window, choose the files of this computer.

## Load order

Top of the Mod Manager list = highest priority (`mods/order.json`): Hyper Power (or off), Super Power (off when Hyper Power is on), Big Money, Free Services, No Sleep, No Fuel, No Fines, No Rollover, No Damage, More Traffic, then other mods. Mods that share a file (`economy_data.sii`, the 173 engine files, `physics.sii`) carry the changes of the mods below them, so nothing is lost.

## Changed values (ATS 1.61.3)

- Big Money: revenue_coef_per_km 0.9 -> 9, cargo_market_revenue_coef_per_km 1.0 -> 10, driver_revenue_coef_per_km 0.67 -> 6.7, driver_cargo_market_revenue_coef_per_km 0.77 -> 7.7, fixed_revenue 600 -> 6000 (x10 of the game's own values); new profile money_account 1500 -> 10,000,000.
- Free Services: tow_price_base/factor, refuel_price_base/factor -> 0; restore prices -> 0; fuel_price in 22 states (1.00-2.17 $/l) -> 0.0001.
- No Sleep: maximum_driving_time 840 -> 10,000,000.
- No Fuel: consumption_coef 0.0001 in 173 engines (33 already had one, 0.89-0.94: changed; 140: added).
- No Fines: 14 fines and offence probabilities -> 0, abandoned_job_fine 12000 -> 0, cargo damage cost -> 0, late delivery 30 days.
- No Damage: 13 damage and wear coefficients -> 0. No Rollover: sway_bar_stiffness_factor 1.0 -> 3.0.
- Super Power: torque x3, air_resistance 3.0 -> 1.5, brake_torque_factor 2.0. Hyper Power: torque x12, differential_ratio x0.35 (98 gearboxes), grip_factor 1.3 (24 tyres), air_resistance 0.1, brakes x4, brake cooling x5, steering minimum 0.25 -> 0.1.
- More Traffic: max_vehicle_count 50 -> 300.

Differences from ETS2, checked by `tests/test_ats_law.py` and `tests/test_pay_law.py` on the installed game: start money $1,500 and coefficient 0.77; no `secondary_torque`, no ferries, no charging price; 33 engines already have `consumption_coef`; `max_vehicle_count` is set, not commented out; most tyres have no `roll_resistance`, so grip goes after `price`.

## Tests and rebuild

```
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python tools\build_mods.py --install      # local alexey_*.scs
.venv\Scripts\python tools\build_workshop.py            # Workshop folders + release files
```

The build reads the installed game (Steam); no SCS files are in the repository. In the ATS Workshop these are NEW items ("Create new"), see [WORKSHOP.md](WORKSHOP.md).

## License

MIT for the tools and the change descriptions (LICENSE). The changed def files inside the `.scs` are derived from American Truck Simulator data (SCS Software).
