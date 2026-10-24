# Changelog / История изменений

## 1.0.3 - 2026-10-24

- No Rollover 1.0.3 really stops the tipping: the cargo centre of gravity is 0.5 m lower in all 81 trailer chassis (`cog_cargo_offset_min/max` -> (0, -0.5, 0)). The stiffer anti-roll bar alone (x3, a test with x10 too) did not help: a loaded trailer fell over in a sharp turn. Checked in the game on 24.10.
- Law: every trailer chassis with `cog_cargo_mass_max` gets both points, one line per chassis block.

---

- No Rollover 1.0.3 правда не даёт опрокидываться: центр тяжести груза на 0,5 м ниже во всех 81 шасси прицепов (`cog_cargo_offset_min/max` -> (0, -0.5, 0)). Одного жёсткого стабилизатора (x3, проба и с x10) не хватало: гружёный прицеп ложился на бок в резком повороте. Проверено в игре 24.10.
- Закон: у каждого шасси с `cog_cargo_mass_max` обе точки, по строке на блок шасси.

## 1.0.2 - 2026-10-24

- Hyper Power, Super Power and No Fuel now change every truck: 83 of 181 gearboxes and 4 of 177 engines were left stock. Our archive reader (tools/cityhash103.py) hashed paths over 64 characters with the CityHash 1.0 branch, but HashFS uses the 1.1 branch there, so 4573 game files (every gearbox with a retarder, all Cascadia gearboxes) were invisible. With Hyper Power those trucks stopped at 104 mph on the rev limiter; now 250 km/h and more (checked in the game).
- The `truck_speed_limit` change of 1.0.1 is gone: the game ignores `def/game_data.sii` from mods (checked with an audible value). The 65 mph cap is the Speed limiter option in Settings > Gameplay; the descriptions say so.
- Laws: two long paths with hashes from the game archives, every listed file under def/vehicle has an entry, the power mods ship no game_data.sii.

---

- Hyper Power, Super Power и No Fuel теперь меняют каждый грузовик: 83 из 181 коробки и 4 из 177 двигателей оставались заводскими. Наш читатель архивов (tools/cityhash103.py) считал хеш путей длиннее 64 символов по ветке CityHash 1.0, а HashFS там использует ветку 1.1, поэтому 4573 файла игры были невидимы (все коробки с ретардером, все коробки Cascadia). С Hyper Power такие грузовики упирались в 104 миль/ч на отсечке; теперь 250 км/ч и больше (проверено в игре).
- Правка `truck_speed_limit` из 1.0.1 убрана: `def/game_data.sii` из мода игра не применяет (проверено на слышимом параметре). Потолок 65 миль/ч - это опция «Ограничитель скорости» в Настройки > Геймплей, описания говорят об этом.
- Законы: два длинных пути с хешами из архивов игры, у каждого файла из списков def/vehicle есть запись, моды мощности не кладут game_data.sii.

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
