# -*- coding: utf-8 -*-
"""
This file imports the parameters values defined in the config/parameters.json file
"""
import json

class Parameters():
    def __init__(self):
        self.paramFilePath = "config/"
        self.paramFileName = "parameters.json"
        self.settings = {}
        self.defaultValues = {}
        self.ReadParameters()

    def __str__(self):
        return str(f'Settings : {self.settings}\nDefault values: {self.defaultValues}')

    def ReadParameters(self):
        print(f'Reading parameters from config file {self.paramFilePath + self.paramFileName} :')
        try:
            with open(self.paramFilePath + self.paramFileName, 'r') as file:
                data = json.load(file)
                self.settings = {}
                self.defaultValues = {}

                for setting in data['settings']:
                    if setting['name'] is not None:
                        if setting['name'] in self.settings.keys():
                            print(f'Setting {setting["name"]} is duplicated in '
                                  f'{self.paramFilePath}{self.paramFileName}, value will be overwritten.')
                        else:
                            self.settings[setting['name']] = setting['value']

                for defaultValue in data['default_values']:
                    if defaultValue['name'] is not None:
                        if defaultValue['name'] in self.defaultValues.keys():
                            print(f'Default value {defaultValue["name"]} is duplicated in '
                                  f'{self.paramFilePath}{self.paramFileName}, value will be overwritten.')
                        else:
                            self.defaultValues[defaultValue['name']] = defaultValue['value']
        except Exception as exc:
            print(f'ERROR - An error occurred during parameters loading : {exc}')
            raise RuntimeError from exc

    def getSettings(self):
        return self.settings

    def getDefaultValues(self):
        return self.defaultValues


if __name__ == "__main__":
    # test instance of the Parameters class
    instance = Parameters()
    print(instance)
    print(instance.getDefaultValues().get('days_list')[1])
    print(instance.getDefaultValues().get('help_message'))
