# Настройка Yandex Cloud Logging
Этап 0. Установить необходимые библиотеки
Этап 1. В коде нужно добавить хендлер для записи в логов в journal
Этап 2. Запустить стримлит через systemcl
Этап 3. Настроить загрузку логов в Yandex Cloud Logging через fluent-bit

## Этап 0. Установить необходимые библиотеки

```
poetry install

...

sudo apt-get update
sudo apt-get install -y git build-essential pkg-config libsystemd-dev golang-go

```

## Этап 1. В коде нужно добавить хендлер для записи в логов в journal

Установить библиотеку systemd

1. В коде создать логгер с единым названием
2. journal.JournaldLogHandler - настроить формат вывода
3. Добавить хэндлер в логгер


## Этап 2. Запустить стримлит через systemd

1. Создаем файл /etc/systemd/system/hr-assistant.service
```
[Unit]
Description=HR Assistant
After=network.target

[Service]
ExecStart=<path_to_venv>/bin/streamlit run <path_to_ta>/resume_analyser/app.py --server.port=8501 --server.address=0.0.0.0
Environment=PYTHONPATH=<path_to_ta>
User=<user>
Group=<user-group>
KillMode=mixed
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

2. Запускаем сервис
```
sudo systemctl daemon-reload
sudo systemctl start hr-assistant
sudo systemctl status hr-assistant
```
Статус должен быть "active (running)"

3. Проверяем, что стримлит запущен
http://<ip>:8501

## Этап 3. Настроить загрузку логов в Yandex Cloud Logging через fluent-bit
1. Устанавливаем fluent-bit
```
wget -qO - https://packages.fluentbit.io/fluentbit.key | sudo apt-key add -
echo "deb https://packages.fluentbit.io/ubuntu/jammy jammy main" | sudo tee /etc/apt/sources.list.d/fluent-bit.list

sudo apt-get update
sudo apt-get install -y fluent-bit
```

Проверяем статус fluent-bit
```
sudo systemctl status fluent-bit
```

2. Устанавливаем плагин fluent-bit-plugin-yandex

# Обновляем и устанавливаем
sudo apt-get update
sudo apt-get install -y fluent-bit