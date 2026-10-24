# Changelog / История изменений

## 1.0.1 - 2026-10-24

- Hyper Power and Super Power lift the game's 65 mph cap: `truck_speed_limit` 104.607 -> 1000 in `def/game_data.sii`. Players reported that the trucks stopped at 104 km/h; the cap works even with the speed limiter option off.
- Every Workshop description lists the game files its mod replaces and says that another author's mod with the same file overrides it when higher in the Mod Manager (and the other way round). The line is built from mod.json, a test checks it for all ten mods.
- Super Power no longer claims that only the speed limiter option caps the speed.

---

- Hyper Power и Super Power снимают потолок игры 65 миль/ч: `truck_speed_limit` 104.607 -> 1000 в `def/game_data.sii`. Грузовики упирались в 104 км/ч; потолок действует и с выключенным ограничителем.
- В описании каждого мода в Мастерской перечислены файлы игры, которые он заменяет, и сказано, что чужой мод с тем же файлом перекрывает его, если стоит выше в Менеджере модов (и наоборот). Строка строится из mod.json, тест проверяет все десять модов.
- Super Power больше не пишет, что скорость режет только настройка ограничителя.

## 1.0.0 - 2026-10-16

- First version for American Truck Simulator 1.61: the ten OpenRoad mods of the ETS2 project (ETS2Mods 1.2.1), built from the ATS files.
- ATS differences: Big Money multiplies the game's own values x10 (driver_cargo_market 0.77 -> 7.7), new profile $10,000,000 instead of $1,500; Free Services without ferries and charging (ATS has none), fuel in 22 states; No Fuel sets consumption_coef where it exists (33 engines) and adds it to the other 140; More Traffic changes max_vehicle_count 50 -> 300 (set in ATS, not commented out); Hyper Power puts tyre grip after price (most ATS tyres have no roll_resistance); no secondary_torque.
- "Деньги ATS.bat" / money.bat: money in dollars (or the profile's currency), backup, --restore, info.sii too.
- Laws on the installed game: tests/test_ats_law.py, tests/test_pay_law.py.
- Release files: OpenRoad_ATS_Mods.zip (all ten mods + install note), ATS_Money_Tool.zip ("Деньги ATS.bat" with the modules it needs; a test runs the unpacked copy), the single .scs and the Workshop folders; workshop/ also gets a short Russian upload guide (tools/workshop_steps.ru.txt).

---

- Первая версия для American Truck Simulator 1.61: десять модов OpenRoad из проекта ETS2 (ETS2Mods 1.2.1), собранные из файлов ATS.
- Отличия ATS: Big Money умножает значения самой игры x10 (driver_cargo_market 0.77 -> 7.7), новый профиль 10 000 000 $ вместо 1500 $; Free Services без паромов и зарядки (в ATS их нет), топливо в 22 штатах; No Fuel меняет consumption_coef там, где он есть (33 двигателя), и добавляет остальным 140; More Traffic меняет max_vehicle_count 50 -> 300 (в ATS он задан, а не закомментирован); Hyper Power ставит сцепление шин после price (у большинства шин ATS нет roll_resistance); secondary_torque нет.
- «Деньги ATS.bat» / money.bat: деньги в долларах (или в валюте профиля), копия, --restore, сумма и в info.sii.
- Законы на файлах установленной игры: tests/test_ats_law.py, tests/test_pay_law.py.
- Файлы выпуска: OpenRoad_ATS_Mods.zip (все десять модов и инструкция), ATS_Money_Tool.zip («Деньги ATS.bat» с нужными модулями; тест запускает распакованную копию), отдельные .scs и папки Мастерской; в workshop/ ещё короткая инструкция загрузки по-русски (tools/workshop_steps.ru.txt).
