Обеспечение работы нового сайта ================================ ## Необходимые пакеты:
* nginx
* Python 3.10
* virtualenv + pip 
* Git

## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com
## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domain.com

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username
└── site
    └── percival_TDD
        ├── [...]
        ├── static
        └── virtualenv