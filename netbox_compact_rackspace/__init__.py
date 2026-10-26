from netbox.plugins import PluginConfig

class NetBoxCompactRackSpaceConfig(PluginConfig):
    name = 'netbox_compact_rackspace'
    verbose_name = 'Компактный RackSpace'
    description = 'Отображение всех стоек в виде компактной матрицы утилизации'
    version = '0.1'
    base_url = 'compact-rackspace'
    default_settings = {}

config = NetBoxCompactRackSpaceConfig
