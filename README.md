# NetBox Compact RackSpace Plugin

Ультра-компактная матрица заполненности всех стоек для NetBox v4.7.x в стиле RackSpace из СУБД RackTables.
Исключает горизонтальный скролл, показывает заполненность юнитов в пиксельном режиме (светло-зеленый — свободно, темно-зеленый — занято).

## Установка

1. Добавьте в `plugin_requirements.txt` вашего netbox-docker:
   `git+https://github.com`
2. Включите плагин в `configuration/plugins.py`:
   `PLUGINS = ['netbox_compact_rackspace']`

