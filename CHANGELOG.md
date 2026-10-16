# Changelog / История изменений

## 1.0.0 - 2026-10-16

- First version for American Truck Simulator 1.61: the ten OpenRoad mods of the ETS2 project (ETS2Mods 1.2.1), built from the ATS files.
- ATS differences: Big Money multiplies the game's own values x10 (driver_cargo_market 0.77 -> 7.7), new profile $10,000,000 instead of $1,500; Free Services without ferries and charging (ATS has none), fuel in 22 states; No Fuel sets consumption_coef where it exists (33 engines) and adds it to the other 140; More Traffic changes max_vehicle_count 50 -> 300 (set in ATS, not commented out); Hyper Power puts tyre grip after price (most ATS tyres have no roll_resistance); no secondary_torque.
- "Деньги ATS.bat" / money.bat: money in dollars (or the profile's currency), backup, --restore, info.sii too.
- Laws on the installed game: tests/test_ats_law.py, tests/test_pay_law.py.

---

- Первая версия для American Truck Simulator 1.61: десять модов OpenRoad из проекта ETS2 (ETS2Mods 1.2.1), собранные из файлов ATS.
- Отличия ATS: Big Money умножает значения самой игры x10 (driver_cargo_market 0.77 -> 7.7), новый профиль 10 000 000 $ вместо 1500 $; Free Services без паромов и зарядки (в ATS их нет), топливо в 22 штатах; No Fuel меняет consumption_coef там, где он есть (33 двигателя), и добавляет остальным 140; More Traffic меняет max_vehicle_count 50 -> 300 (в ATS он задан, а не закомментирован); Hyper Power ставит сцепление шин после price (у большинства шин ATS нет roll_resistance); secondary_torque нет.
- «Деньги ATS.bat» / money.bat: деньги в долларах (или в валюте профиля), копия, --restore, сумма и в info.sii.
- Законы на файлах установленной игры: tests/test_ats_law.py, tests/test_pay_law.py.
