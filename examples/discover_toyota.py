from plugin_host import PluginHost

host = PluginHost()
print(host.discover("toyota.identify_vehicle", ".bin"))
