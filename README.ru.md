# AmericanTruckSimulatorMods - моды OpenRoad для American Truck Simulator

Десять модов для одиночной игры American Truck Simulator (версия 1.61) - те же, что [моды OpenRoad для ETS2](https://github.com/ALEXalesha/ETS2Mods), и инструменты, которые собирают их из файлов самой игры, плюс «Деньги ATS.bat» - поставить свою сумму денег в сохранении.

[English](README.md)

[![Status](https://img.shields.io/badge/status-stable-brightgreen)](#) [![Release](https://img.shields.io/github/v/release/ALEXalesha/AmericanTruckSimulatorMods)](https://github.com/ALEXalesha/AmericanTruckSimulatorMods/releases/latest) [![CI](https://github.com/ALEXalesha/AmericanTruckSimulatorMods/actions/workflows/ci.yml/badge.svg)](https://github.com/ALEXalesha/AmericanTruckSimulatorMods/actions/workflows/ci.yml) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![ATS](https://img.shields.io/badge/American_Truck_Simulator-mods-1B2838?logo=steam&logoColor=white)](https://store.steampowered.com/app/270880/) [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-D97757?logo=claude&logoColor=white)](https://claude.com/claude-code)

Код, тесты и документация этого проекта написаны Claude (Anthropic) в Claude Code. Идеи, проверка и решения - Алексей.

> Проект не связан с SCS Software и не одобрен ею. «American Truck Simulator» - товарный знак SCS Software. Моды фанатские, только для одиночной игры; в TruckersMP и Конвое они не работают.

| Мод (файл в выпуске) | Что делает |
|---|---|
| OpenRoad: Hyper Power (`OpenRoad_Hyper_Power.scs`) | Безумный: момент x12, главная пара x0.35 (потолок по передачам около 540-640 км/ч), почти нет сопротивления воздуха, сцепление +30%, тормоза x4. Вместо Super Power. |
| OpenRoad: Super Power (`OpenRoad_Super_Power.scs`) | Момент x3, сопротивление воздуха вдвое меньше, тормоза x2. Управляемо. |
| OpenRoad: Big Money (`OpenRoad_Big_Money.scs`) | Оплата рейсов x10; новый профиль начинает с 10 000 000 $. |
| OpenRoad: Free Services (`OpenRoad_Free_Services.scs`) | Топливо почти даром (0.0001 $/л) во всех 22 штатах, бесплатные эвакуация, экстренная заправка и восстановление износа. |
| OpenRoad: No Sleep (`OpenRoad_No_Sleep.scs`) | Водитель не устаёт. |
| OpenRoad: No Fuel (`OpenRoad_No_Fuel.scs`) | Двигатели тратят 1/10000 топлива. |
| OpenRoad: No Fines (`OpenRoad_No_Fines.scs`) | Нет штрафов полиции и камер, нет штрафа за отказ, повреждение груза не уменьшает оплату, 30 дней на опоздание. |
| OpenRoad: No Rollover (`OpenRoad_No_Rollover.scs`) | Передний стабилизатор в 3 раза жёстче; плюс ползунки устойчивости в настройках. |
| OpenRoad: No Damage (`OpenRoad_No_Damage.scs`) | Нет урона, износа и повреждения груза. |
| OpenRoad: More Traffic (`OpenRoad_More_Traffic.scs`) | Лимит машин ИИ 50 -> 300; плотность - переменная игры `g_traffic`. |

## Установка

- **Мастерская Steam:** подписаться на моды OpenRoad для ATS и включить их в Менеджере модов.
- **Из выпусков:** на странице [последнего выпуска](https://github.com/ALEXalesha/AmericanTruckSimulatorMods/releases/latest) скачать `OpenRoad_ATS_Mods.zip` (все десять модов, внутри короткая инструкция) или отдельные `.scs`. Файлы `.scs` положить в `Документы\American Truck Simulator\mod`.
- **Как включить:** запустить игру, выбрать профиль, открыть **Менеджер модов**, перенести нужные моды в список активных в порядке ниже (верхний - главный), нажать «Подтвердить изменения». Super Power не включать вместе с Hyper Power.

Файлы выпуска:

| Файл | Что это |
|---|---|
| `OpenRoad_ATS_Mods.zip` | Все десять модов `.scs` и инструкция по установке |
| `OpenRoad_<Имя>.scs` | Те же моды по одному |
| `ATS_Money_Tool.zip` | «Деньги ATS.bat» с нужными файлами (см. «Поменять деньги») |
| `OpenRoad_Workshop_Folders.zip` | Готовые папки для загрузчика Мастерской Steam |

## Поменять деньги

Деньги лежат в сохранении. Как поставить свою сумму:

1. Полностью закрыть игру.
2. Дважды щёлкнуть **`Деньги ATS.bat`** (или **`money.bat`** - то же самое) в папке репозитория. Без репозитория: скачать `ATS_Money_Tool.zip` из выпуска, распаковать в любую папку и запустить `Деньги ATS.bat` оттуда.
3. Он покажет профили и деньги **так, как их показывает игра** (в долларах; если в настройках выбраны песо, канадские доллары или евро - в них), спросит новую сумму (`10000000`, `10 000 000` или `10 млн`), попросит закрыть игру, если она ещё запущена, сделает копию сохранения и запишет.
4. Когда он напишет **ЗАПИСАНО**, запустить игру и загрузить последнее сохранение («Продолжить»).

Нужен Python 3 с python.org и пакет для шифрованных сохранений: `py -m pip install -r tools\requirements.txt`. Если в проекте есть `.venv`, берётся он.

То же одной командой (10 000 000 в валюте игры, в самое новое сохранение):

```
python tools/save_money.py --save latest --set 10000000 --apply
```

Без `--apply` ничего не записывается: скрипт крупно пишет «NOTHING WRITTEN / НИЧЕГО НЕ ЗАПИСАНО». `--restore` возвращает последнюю копию этого сохранения:

```
python tools/save_money.py --save autosave --restore
```

Подробности:
- В сохранении деньги лежат в долларах США. Игра показывает их в валюте из настроек («Геймплей» - «Валюта», в `config.cfg` профиля `g_currency`: 0 USD, 1 CAD, 2 MXN, 3 EUR) по курсу из `def/economy_data.sii`. `--set` принимает сумму как на экране, `--set-usd` - доллары как есть, `--currency MXN` - валюта вместо валюты профиля.
- Сумма пишется в `game.sii` и в `info.sii` сохранения (её показывает экран загрузки).
- Копия до правки: `Документы\American Truck Simulator\save_backups\<профиль>\<сохранение>_<время>\`.
- **Облако Steam.** Профиль с облаком лежит в `Steam\userdata\<номер>\270880\remote\profiles`. При следующем запуске игры Steam видит, что файл изменился на этом компьютере, и сам отправляет его в облако. Только если облачная копия тоже менялась (играли на другом компьютере), Steam покажет окно конфликта: тогда выбрать файлы этого компьютера, иначе вернётся старая сумма.

## Порядок модов

Верхний в списке активных модов - главный. Сверху вниз (`mods/order.json`):

1. Hyper Power (или выключен, если нужен Super Power)
2. Super Power (выключить, если включён Hyper Power)
3. Big Money
4. Free Services
5. No Sleep
6. No Fuel
7. No Fines
8. No Rollover
9. No Damage
10. More Traffic
11. другие моды

Некоторые моды меняют один и тот же файл: `economy_data.sii` (Big Money, Free Services, No Sleep, No Fines), 173 файла двигателей (Hyper/Super Power, No Fuel), `physics.sii` (Hyper/Super Power, No Rollover). Игра берёт только самую верхнюю копию, поэтому каждый мод несёт и правки модов ниже по списку - ничего не теряется. Hyper Power заменяет Super Power и его x3 не несёт. Обратная сторона: мод в одиночку приносит правки нижних в общих файлах (например, Big Money в одиночку тоже даёт бесплатную эвакуацию).

## Что поменяно (ATS 1.61.3)

| Мод | Файл | Параметр: было -> стало |
|---|---|---|
| Big Money | `def/economy_data.sii` | revenue_coef_per_km 0.9 -> 9, cargo_market_revenue_coef_per_km 1.0 -> 10, driver_revenue_coef_per_km 0.67 -> 6.7, driver_cargo_market_revenue_coef_per_km 0.77 -> 7.7, fixed_revenue 600 -> 6000 (всё x10 от значений игры) |
| Big Money | `def/initial_save/normal/game.sii` | money_account 1500 -> 10 000 000 |
| Free Services | `def/economy_data.sii` | tow_price_base 150 -> 0, tow_price_factor 0.4 -> 0, refuel_price_base 150 -> 0, refuel_price_factor 3 -> 0 |
| Free Services | `def/service_data.sii` | truck/trailer_restore_accessory_fixed_price 1000 -> 0, ..._price_coef 1.1 -> 0 |
| Free Services | `def/country/*.sui` (22 штата) | fuel_price (1.00-2.17 $/л) -> 0.0001 |
| No Sleep | `def/economy_data.sii` | maximum_driving_time 840 -> 10 000 000 |
| No Fuel | 173 двигателя | consumption_coef -> 0.0001 (у 33 он уже был, 0.89-0.94, у 140 добавлен) |
| No Fines | `def/police_data.sii` | fine_amounts[0..13] -> 0, offence_probabilty / offence_police_probabilty -> 0, fine_factor_base/step -> 0 |
| No Fines | `def/economy_data.sii` | abandoned_job_fine 12000 -> 0, cargo_damage_cost 5 -> 0, cargo_damage_cost_factor 0.04 -> 0, late_delivery_max_overtime -> 43200 (30 дней) |
| No Damage | `def/damage_data.sii` | 13 коэффициентов урона и износа -> 0 |
| No Rollover | `def/vehicle/physics.sii` | sway_bar_stiffness_factor 1.0 -> 3.0 |
| Super Power | двигатели, `physics.sii` | torque x3, air_resistance 3.0 -> 1.5, brake_torque_factor 1.0 -> 2.0 |
| Hyper Power | двигатели, 98 коробок, 24 шины, `physics.sii` | torque x12, differential_ratio x0.35, grip_factor 1.3 (добавлен), air_resistance 3.0 -> 0.1, brake_torque_factor 4.0, brake_cooling_rate 0.01 -> 0.05, steering_sensitivity_multiplier_minimum 0.25 -> 0.1 |
| More Traffic | `def/traffic_data.sii` | max_vehicle_count 50 -> 300 |

Чем ATS отличается от ETS2 (поэтому это не простая копия): другие стартовые деньги (1500 $) и коэффициент 0.77; нет `secondary_torque`, паромов и цены зарядки; у части двигателей `consumption_coef` уже есть (мод его меняет, а не добавляет второй); `max_vehicle_count` в ATS задан, а не закомментирован; у большинства шин нет строки `roll_resistance`, поэтому сцепление вставляется после `price`. Всё это проверяют законы `tests/test_ats_law.py` и `tests/test_pay_law.py` на файлах установленной игры.

## Тесты и пересборка

```
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python tools\build_mods.py --install
```

Сборка читает файлы самой игры из установки Steam; файлов SCS в репозитории нет. Если обновление игры переименует параметр, сборка остановится с ошибкой, а законы покажут, что именно поменялось.

## Локальные сборки и пакет для Мастерской

- `python tools/build_mods.py --install` собирает локальные `alexey_*.scs` (то же содержимое, свои имена пакетов) в `build/` и `Документы\American Truck Simulator\mod`.
- `python tools/build_workshop.py` собирает публичные версии «OpenRoad»: папки для Мастерской в `workshop/` и файлы выпуска в `release/`. В Мастерской ATS это НОВЫЕ предметы («Create new», не Update). Подробно - в [WORKSHOP.md](WORKSHOP.md).

## Лицензия

Инструменты и описания правок - под лицензией MIT (файл LICENSE). Изменённые def-файлы внутри `.scs` сделаны из данных American Truck Simulator (SCS Software).
