'''Info Header Start
Name : GeneralConfig_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''

def GetConfigSchema(configModule:"SchemaObjects", configComp:"JsonConfig") -> dict:
	positiveValue = configModule.ConfigValue(default = 4, validator = lambda value : value > 0)
	
	return {
		}
		
		
#def GetConfigData():
#	return a jsonString. Can be used to fetch API data or similiar.
#	return ""