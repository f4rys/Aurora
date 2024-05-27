dictionary_en = {
    # Navigation bar
    "devices": "DEVICES",
    "smart_mode": "SMART MODE",
    "analytics": "ANALYTICS",
    "schedules": "SCHEDULES",
    "help": "HELP",
    # Device widget
    "white": "White",
    "colour": "Colour",
    "countdown": "Countdown",
    "set_countdown": "Set countdown",
    "cancel_countdown": "Cancel countdown",
    "remaining_time": "Remaining time",
    # All devices
    "reload_in_progress": "Reloading devices...",
    "reload_completed": "Reload",
    # Settings
    "smart_mode_settings": "Smart Mode",
    "language": "Language",
    "smart_mode_label": "Assistance with device control",
    "language_label": "Interface language",
    "max_retry_label": "Number of attempts to connect to the device",
    "max_retry_0": "Fastest, but not reliable",
    "max_retry_3": "Best for most scenarios",
    "max_retry_5": "Slowest, but most efficient",
    # Profile
    "api_key": "API Key",
    "api_secret": "API Secret",
    "api_region": "API Region",
    "api_device_id": "API Device ID",
    "change_credentials_button": "Change credentials",
    "fetch_data_button": "Fetch new devices and local keys",
    # Action bar label titles
    "devices_title": "Devices",
    "smart_mode_title": "Smart mode",
    "analytics_title": "Analytics",
    "schedules_title": "Schedules",
    "help_title": "Help",
    "settings_title": "Settings",
    "profile_title": "Profile",
    "credentials_title": "Setup credentials",
    # Tooltips
    "profile_tooltip": "Credentials",
    "settings_tooltip": "Settings",
    "hide_tooltip": "Hide window",
    "exit_tooltip": "Exit program",
    "bulb_label_tooltip": "Device name",
    "bulb_tooltip": "ON/OFF",
    "brightness_tooltip": "Brightness",
    "temperature_tooltip": "Temperature",
    "contrast_tooltip": "Contrast",
    "colour_tooltip": "Colour",
    "time_edit_tooltip": "Enter time",
    "countdown_accept_button_tooltip": "Switch device state after the specified time has elapsed",
    "reload_button_tooltip": "Try to establish new connection with devices",
    "device_button_tooltip": "Click to open control panel",
    "device_on_tooltip": "Device on. Click to switch",
    "device_off_tooltip": "Device off. Click to switch",
    "device_offline_tooltip": "Device offline",
    "analytics_devices_tooltip": "Select the devices to be included in the analysis",
    "select_all_tooltip": "Select all devices",
    "deselect_all_tooltip": "Deselect all devices",
    "analytics_plot_tooltip": "This chart shows how many commands were sent to the device(s) on a given day",
    "change_credentials_tooltip": "Enter new credentials if you want to switch cloud projects",
    "fetch_data_tooltip": "Use this to fetch new data if you have added new devices to cloud / app",
    "switch_action_tooltip": "Switch",
    "bright_and_temp_action_tooltip": "Brightness and temperature",
    "colour_action_tooltip": "Colour",
    "switch_on_tooltip": "Switch: ON",
    "switch_off_tooltip": "Switch: OFF",
    "enable_disable_schedule_tooltip": "Enable / disable schedule",
    "edit_schedule_tooltip": "Edit schedule",
    "delete_schedule_tooltip": "Delete schedule",
    # Days
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
    "sunday": "Sunday",
    # Analytics
    "computing_analytics": "Computing analytics..",
    "devices_usage": "Devices usage in the last 7 days",
    "select_device_prompt": "Select at least one device",
    "plot_error": "Something went wrong.\nRestart program to try again.",
    # Credentials
    "api_region_prompt": "Select your region",
    "china_dc": "China",
    "western_america_dc": "Western America",
    "eastern_america_dc": "Eastern America",
    "central_europe_dc": "Central Europe",
    "western_europe_dc": "Western Europe",
    "india_dc": "India",
    "set_credentials": "Set credentials",
    # Schedules
    "add_edit_schedule": "Add/edit schedule",
    "reloading_schedules": "Reloading schedules..",
    "add_schedule": "Add schedule",
    # Add/edit schedule
    "set_schedule_name": "1. Set schedule name:",
    "set_schedule_time": "2. Set time:",
    "set_schedule_weekdays": "3. Select weekdays:",
    "select_schedule_devices": "4. Select devices:",
    "select_schedule_action": "5. Select action:",
    "enter_action_value": "6. Enter value:",
    "save_schedule_changes": "Save changes",
    "select_switch_value": "6. Enter value for ON/OFF:",
    "on": "On",
    "off": "Off",
    "select_brightness_value": "6. Enter values for brightness and temperature:",
    "select_colour_value": "6. Enter values for colour and brightness:",
    # Smart mode
    "computing_smart_mode": "Calculating smart mode suggestions..",
    "smart_mode_off": "Smart mode is off.",
    "no_more_actions": "No more actions planned for today.",
    "brightness": "Brightness",
    "switch": "Switch",
    "temperature": "Temperature",
    # Toasts
    "success_toast_title": "Success",
    "success_toast_body_credentials": "Your Tuya credentials has been set and list of your devices has been updated.",
    "error_toast_title": "Failure",
    "error_toast_body": "A problem occured. Try later",
    "error_toast_body_credentials": "A problem occured. Check if the data you entered is correct and try again.",
    "success_toast_body_fetch_data": "Successfully fetched new devices and local keys.",
    # Help
    "tooltips_q": "What does this [thing] do?",
    "tooltips_a": "Hover the cursor over the item and wait. \nA tooltip will tell you what this particular \nelement is for.",
    "devices_offline_q": "All / some of my devices appear \nto be offline.",
    "devices_offline_a": "Try reloading. If it doesn't change anything, \ngo to settings (gear icon in the top right corner) \nand change 'number of attempts to connect \nto the device' to a higher number. If the problem \nstill persists, there may be a problem with your \nWi-Fi signal strength or bandwidth. Not all Tuya \ndevices seem to work with 5Ghz, so try changing \nit to 2.4Ghz in your router settings.",
    "countdown_execution_requirements_q": "Will the countdown still work \neven if I close the application / turn off \nmy PC?",
    "countdown_execution_requirements_a": "Yes, the countdown is saved in the device's \nmemory, so it will be executed regardless of \nthe application running or not. Wi-Fi connection \nalso isn't necessary here. ",
    "countdown_limit_q": "What's with the countdown limit?",
    "countdown_limit_a": "Most of Tuya devices accept countdowns \nup to 24 hours.",
    "analytics_plot_q": "What does the analytics plot represent?",
    "analytics_plot_a": "It shows you the number of commands sent to \ndevice/devices over the last 7 days. It also includes \nall the actions that were taken from any other \napplication, not only Aurora.",
    "schedule_error_q": "I get an error trying to \nadd/modify/delete schedule.",
    "schedule_error_a": "Try again later. There may be problems \nestablishing a connection with Tuya cloud.",
    "schedule_execution_requirements_q": "Will the schedule be executed \nif I close the application / turn off my PC?",
    "schedule_execution_requirements_a": "Yes, it is saved in Tuya Cloud, so the application \nisn't necessary, but device still needs to have \na stable Wi-Fi connection.",
    "smart_mode_q": "What if the suggestions made by \nthe smart mode are not accurate?",
    "smart_mode_a": "If you inspected smart mode suggestions \nand decided that some of them are mismatched, \nyou can delete them so they will not be executed.",
    "question_not_listed_q": "My question isn't listed here.",
    "question_not_listed_a_1": "Feel free to email me on",
    "question_not_listed_a_2": "or visit Aurora's repository",
    "author" : "Author:"
}

dictionary_pl = {
    # Navigation bar
    "devices": "URZĄDZENIA",
    "smart_mode": "ASYSTENT",
    "analytics": "STATYSTYKI",
    "schedules": "KALENDARZ",
    "help": "POMOC",
    # Device widget
    "white": "Białe",
    "colour": "Kolor",
    "countdown": "Odliczanie",
    "set_countdown": "Ustaw odliczanie",
    "cancel_countdown": "Anuluj odliczanie",
    "remaining_time": "Pozostały czas",
    # All devices
    "reload_in_progress": "Odświeżanie w toku...",
    "reload_completed": "Odśwież",
    # Settings
    "smart_mode_settings": "Tryb inteligentny",
    "language": "Język",
    "smart_mode_label": "Asystent wspomagania sterowaniem urządzeniami",
    "language_label": "Język interfejsu",
    "max_retry_label": "Liczba prób połączenia się z urządzeniem",
    "max_retry_0": "Najszybsze, ale mało skuteczne",
    "max_retry_3": "Najlepsze w większości sytuacji",
    "max_retry_5": "Najwolniejsze, ale najbardziej skuteczne",
    # Profile
    "api_key": "Klucz API",
    "api_secret": "Sekretny kod API",
    "api_region": "Region",
    "api_device_id": "ID urządzenia",
    "change_credentials_button": "Zmień konfigurację",
    "fetch_data_button": "Pobierz nowe urządzenia i klucze lokalne",
    # Action bar label titles
    "devices_title": "Urządzenia",
    "smart_mode_title": "Tryb inteligentny",
    "analytics_title": "Statystyki",
    "schedules_title": "Harmonogramy",
    "help_title": "Pomoc",
    "settings_title": "Ustawienia",
    "profile_title": "Profil",
    "credentials_title": "Parametry konfiguracji",
    # Tooltips
    "profile_tooltip": "Dane konta",
    "settings_tooltip": "Ustawienia",
    "hide_tooltip": "Ukryj okno",
    "exit_tooltip": "Zamknij program",
    "bulb_label_tooltip": "Nazwa urządzenia",
    "bulb_tooltip": "Włącz/Wyłącz",
    "brightness_tooltip": "Jasność",
    "temperature_tooltip": "Temperatura",
    "contrast_tooltip": "Kontrast",
    "colour_tooltip": "Kolor",
    "time_edit_tooltip": "Wprowadź czas",
    "countdown_accept_button_tooltip": "Przełącz stan urządzenia po upłynięciu wyznaczonego czasu",
    "reload_button_tooltip": "Spróbuj nawiązać nowe połączenie z urządzeniami",
    "device_button_tooltip": "Kliknij, aby otworzyć panel sterowania",
    "device_on_tooltip": "Urządzenie włączone. Kliknij, aby przełączyć",
    "device_off_tooltip": "Urządzenie wyłączone. Kliknij, aby przełączyć",
    "device_offline_tooltip": "Urządzenie w trybie offline",
    "analytics_devices_tooltip": "Wybierz urządzenia, które mają zostać uwzględnione w analizie",
    "select_all_tooltip": "Wybierz wszystkie urządzenia",
    "deselect_all_tooltip": "Odznacz wszystkie urządzenia",
    "analytics_plot_tooltip": "Ten wykres pokazuje, ile poleceń zostało wysłanych do urządzenia / urządzeń w danym dniu",
    "change_credentials_tooltip": "Wprowadź nowe dane uwierzytelniające, jeśli chcesz przełączyć projekt chmurowy",
    "fetch_data_tooltip": "Użyj tego, aby pobrać nowe dane, jeśli dodałeś nowe urządzenia do chmury / aplikacji.",
    "switch_action_tooltip": "Przełącznik",
    "bright_and_temp_action_tooltip": "Jasność i temperatura",
    "colour_action_tooltip": "Kolor",
    "switch_on_tooltip": "Przełącznik: WŁ.",
    "switch_off_tooltip": "Przełącznik: WYŁ.",
    "enable_disable_schedule_tooltip": "Włącz / wyłącz harmonogram",
    "edit_schedule_tooltip": "Edytuj harmonogram",
    "delete_schedule_tooltip": "Usuń harmonogram",
    # Days
    "monday": "Poniedziałek",
    "tuesday": "Wtorek",
    "wednesday": "Środa",
    "thursday": "Czwartek",
    "friday": "Piątek",
    "saturday": "Sobota",
    "sunday": "Niedziela",
    # Analytics
    "computing_analytics": "Obliczanie statystyk..",
    "devices_usage": "Użycie urządzeń (ostatnie 7 dni)",
    "select_device_prompt": "Wybierz przynajmniej jedno urządzenie",
    "plot_error": "Coś poszło nie tak\nZrestartuj program, aby ponowić próbę.",
    # Credentials
    "api_region_prompt": "Wybierz swój region",
    "china_dc": "Chiny",
    "western_america_dc": "Ameryka Zachodnia",
    "eastern_america_dc": "Ameryka Wschodnia",
    "central_europe_dc": "Europa Środkowa",
    "western_europe_dc": "Europa Zachodnia",
    "india_dc": "Indie",
    "set_credentials": "Ustaw dane uwierzytelniające",
    # Schedules
    "add_edit_schedule": "Dodaj/edytuj harmonogram",
    "reloading_schedules": "Ładowanie harmonogramów..",
    "add_schedule": "Dodaj harmonogram",
    # Add/edit schedule
    "set_schedule_name": "1. Ustaw nazwę harmonogramu:",
    "set_schedule_time": "2. Ustaw czas:",
    "set_schedule_weekdays": "3. Wybierz dni tygodnia:",
    "select_schedule_devices": "4. Wybierz urządzenia:",
    "select_schedule_action": "5. Wybierz operację:",
    "enter_action_value": "6. Wprowadź wartość:",
    "save_schedule_changes": "Zapisz zmiany",
    "select_switch_value": "6. Wprowadź wartość dla WŁ/WYŁ:",
    "on": "Wł.",
    "off": "Wył.",
    "select_brightness_value": "6. Wprowadź wartość jasności i temperatury:",
    "select_colour_value": "6. Wprowadź wartość koloru i jasności:",
    # Smart mode
    "computing_smart_mode": "Obliczanie sugestii trybu inteligentego..",
    "smart_mode_off": "Tryb inteligentny jest wyłączony.",
    "no_more_actions": "Na dziś nie zaplanowano więcej działań.",
    "brightness": "Jasność",
    "switch": "Przełącznik",
    "temperature": "Temperatura",
    # Toasts
    "success_toast_title": "Sukces",
    "success_toast_body_credentials": "Twoje dane uwierzytelniające Tuya zostały ustawione, a lista urządzeń została zaktualizowana.",
    "error_toast_title": "Błąd",
    "error_toast_body": "Wystąpił problem. Spróbuj później",
    "error_toast_body_credentials": "Wystąpił problem. Sprawdź, czy wprowadzone dane są poprawne i spróbuj ponownie.",
    "success_toast_body_fetch_data": "Pobrano nowe urządzenia i klucze lokalne.",
    # Help
    "tooltips_q": "Do czego [to] służy?",
    "tooltips_a": "Najedź kursorem na element i poczekaj. \nEtykieta narzędzia powie ci, do czego służy \ndany element.",
    "devices_offline_q": "Wszystkie / niektóre z moich urządzeń \nwydają się być niedostępne.",
    "devices_offline_a": "Spróbuj ponownie załadować urządzenia. \nJeśli nic to nie zmieni, przejdź do ustawień \n(ikona koła zębatego w prawym górnym rogu) \ni zmień „liczbę prób połączenia z urządzeniem” \nna wyższą. Jeśli problem nadal się utrzymuje, \nmoże to oznaczać problem z siłą sygnału \nWi-Fi lub przepustowością łącza. Wygląda na \nto, że nie wszystkie urządzenia Tuya działają z \nczęstotliwością 5 GHz, więc spróbuj zmienić ją \nna 2,4 GHz w ustawieniach routera.",
    "countdown_execution_requirements_q": "Czy odliczanie będzie nadal działać, \nnawet jeśli zamknę aplikację / wyłączę \nkomputer?",
    "countdown_execution_requirements_a": "Tak, odliczanie jest zapisywane w pamięci \nurządzenia, więc zostanie wykonane niezależnie \nod tego, czy aplikacja jest uruchomiona, czy nie. \nPołączenie Wi-Fi również nie jest tutaj konieczne.",
    "countdown_limit_q": "O co chodzi z limitem odliczania?",
    "countdown_limit_a": "Większość urządzeń Tuya akceptuje \nodliczanie do maksymalnie 24 godzin.",
    "analytics_plot_q": "Co przedstawia wykres statystyczny?",
    "analytics_plot_a": "Pokazuje liczbę poleceń wysłanych do \nurządzenia/urządzeń w ciągu ostatnich 7 dni. \nObejmuje również wszystkie działania, które \nzostały podjęte z dowolnej innej aplikacji, \nnie tylko z Aurory.",
    "schedule_error_q": "Pojawia się błąd podczas próby \ndodania/modyfikacji/usunięcia \nharmonogramu.",
    "schedule_error_a": "Spróbuj ponownie później. Mogą wystąpić \nproblemy z nawiązaniem połączenia z chmurą \nTuya.",
    "schedule_execution_requirements_q": "Czy harmonogram zostanie wykonany, \njeśli zamknę aplikację / wyłączę \nkomputer?",
    "schedule_execution_requirements_a": "Tak, jest on zapisywany w chmurze Tuya, \nwięc aplikacja nie jest konieczna, ale urządzenie \nnadal musi mieć stabilne połączenie Wi-Fi.",
    "smart_mode_q": "Co jeśli sugestie trybu inteligentnego \nnie są trafne?",
    "smart_mode_a": "Jeśli sprawdziłeś sugestie trybu inteligentnego \ni zdecydowałeś, że niektóre z nich są nietrafione, \nmożesz je usunąć, aby nie zostały wykonane.",
    "question_not_listed_q": "Mojego pytania nie ma na liście.",
    "question_not_listed_a_1": "Zapraszam do kontaktu mailowego:",
    "question_not_listed_a_2": "lub odwiedź repozytorium projektu Aurora:",
    "author" : "Autor:"
}
