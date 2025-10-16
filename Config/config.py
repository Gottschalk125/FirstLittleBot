import os
import json

SYMBOL = "TSLA"
QTY = "1"
BuyMax = False
Buypercent = True
Percent = 0.05
BuyDifShares = False

MODE_MOMENTUM = True
MODE_MEAN_REVERSION = False

#Personal Informations
EMAILUSER=""

#no possibility to set following variables
STARTVALUE = 0


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


class RuntimeConfig:
    def __init__(self):
        # Standardwerte
        self.SYMBOL = ["TSLA"]
        self.QTY = [1]
        self.BuyMax = False
        self.Buypercent = True
        self.Percent = 0.05
        self.BuyDifShares = False

        # Strategie
        self.MODE_MOMENTUM = True
        self.MODE_MEAN_REVERSION = False

        # Persönliche Info
        self.EMAILUSER = ""
        self.STARTVALUE = 0  # Fix, nicht änderbar

        self.load()

    def as_dict(self):
        return self.__dict__

    def update(self, updates: dict):
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # nach jeder Änderung automatisch speichern

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.as_dict(), f, indent=4)

    def load(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)

# Eine einzige, globale Instanz
config = RuntimeConfig()
