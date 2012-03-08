"""
 Naam: bagconfig.py
 Omschrijving: (Gebaseerd op libBAGconfiguratie.py) Functies voor het lezen van BAG.conf en het verwerken van commandline argumenten
 Auteur(s): Matthijs van der Deijl, Stefan de Konink, Just van den Broecke, Milo van der Linden
"""

import sys
import os
import logging

try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser


class BAGConfig:
    logger = logging.getLogger('bagextractlog')
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # create formatter
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    def __init__(self, args):
        # Derive home dir from script location
        self.bagextract_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # Default config file
        config_file = os.path.realpath(self.bagextract_home + '/bagextract.conf')

        # Option: overrule config file with command line arg pointing to config file
        if args.config:
            config_file = args.config

        if not os.path.exists(config_file):
            self.logger.critical(str(config_file) + " niet gevonden")

        _configparser = ConfigParser()
        try:
            _configparser.read(config_file)
        except Exception:
            e = sys.exc_info()[1]
            self.logger.critical(str(config_file) + " \n\t" + str(e))

        try:
            # Zet parameters uit config bestand

            self.soort = _configparser.defaults()['soort']
            self.database = _configparser.defaults()['database']
            self.schema = _configparser.defaults()['schema']
            self.host = _configparser.defaults()['host']
            self.user = _configparser.defaults()['user']
            self.password = _configparser.defaults()['password']
            self.port = _configparser.defaults()['port']

        except Exception:
            e = sys.exc_info()[1]
            self.logger.critical(str(config_file) + " \n\t" + str(e))

        try:
            # Optioneel: overrulen met (commandline) args
            #if args.soort:
            #    self.soort = args.soort
            if args.extract:
                self.extract = args.extract
            if args.database:
                self.database = args.database
            if args.host:
                self.host = args.host
            if args.schema:
                self.schema = args.schema
            # default to public schema
            if not self.schema:
                self.schema = 'public'
            if args.username:
                self.user = args.username
            if args.port:
                self.port = args.port
            if args.no_password:
                # Gebruik geen wachtwoord voor de database verbinding
                self.password = None
            else:
                if args.password:
                    self.password = args.password

            # Assign Singleton (of heeft Python daar namespaces voor?) (Java achtergrond)
            BAGConfig.config = self
        except Exception:
            e = sys.exc_info()[1]
            self.logger.critical(" configuratiefout in " + str(config_file) + " " + str(e))

    def __repr__(self):
        return "<BAGConfig soort:%s database:%s schema: %s host:%s user:%s password:%s, port:%s>" % (self.soort, self.database, self.schema, self.host, self.user, self.password, self.port)
        
    def get_database(self):
        if self.soort == "postgres":
            from postgresdb import Database
            return Database(self.config)

        elif self.soort == "sqlite":
            from sqlitedb import Database
            return Database()
            
        else: #ga voorlopig uit van "postgres"
            from postgresdb import Database
            return Database()




