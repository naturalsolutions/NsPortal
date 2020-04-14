from sqlalchemy import (
    engine_from_config
)
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import (
    sessionmaker,
    configure_mappers
)
from ns_portal.database.meta import (
    Main_Db_Base,
    Log_Db_Base
) # noqa

__all__ = [
    "Main_Db_Base",
    "Log_Db_Base"
]
'''
you should have this key in your *.ini

DBUSED           = MAIN_DB
MAIN_DB.UID      = username will access
MAIN_DB.PWD      = password for username
MAIN_DB.SERVER   = server adress
MAIN_DB.PORT     = server port
MAIN_DB.DATABASE = database name
'''


# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .main_db import * # noqa
from .security_db import * # noqa
from .log_db import * # noqa

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def includeme(config):
    myConfig = config.get_settings()

    dbPossible = getDBUsed(myConfig=myConfig)
    engines = createEngines(myConfig=myConfig, dbPossible=dbPossible)

    session_factory = get_session_factory(engines)
    config.registry['dbsession_factory'] = session_factory

    # for each new request we gonna add
    # dbsession attribute
    config.add_subscriber(
        'ns_portal.database.new_request',
        'pyramid.events.NewRequest'
    )


def checkConfigDBUsed(myConfig):
    if 'DBUSED' not in myConfig:
        raise KeyError('DBUSED key should be present in .ini')

    dbDefineInConfig = myConfig.get('DBUSED', None)
    if dbDefineInConfig is None or dbDefineInConfig == '':
        raise ValueError(
            'Expected string for DBUSED key got ({dbDefineInConfig}) '.format(dbDefineInConfig=dbDefineInConfig),
            'no values please define one db in *.ini'
            )


def getDBUsed(myConfig):

    checkConfigDBUsed(myConfig=myConfig)

    dbDefineInConfig = myConfig.get('DBUSED')
    return dbDefineInConfig.split(',')


def checkConfigURL(configOptions, databaseName):
    keysNeeded = [
        'DATABASE',
        'DIALECT',
        'ODBCDRIVER',
        'PORT',
        'PWD',
        'SERVER',
        'UID',
    ]
    for item in keysNeeded:
        concatKey = '.'.join([databaseName, item])
        if concatKey not in configOptions:
            raise KeyError('{!r} must be defined in *.ini'.format(concatKey))

        valueFind = configOptions.get(concatKey)
        if valueFind is None or valueFind == '':
            raise ValueError(
                'Expected string value for {!r}'.format(concatKey))


def buildConfigURLAccordingToDialect(myConfig, db):
    dialectConfigURL = {
        'drivername': myConfig.get(db + '.DIALECT'),
        'username': myConfig.get(db + '.UID'),
        'password': myConfig.get(db + '.PWD'),
        'host': myConfig.get(db + '.SERVER'),
        'port': myConfig.get(db + '.PORT'),
        'database': myConfig.get(db + '.DATABASE'),
        'query': dict(driver=myConfig.get(db + '.ODBCDRIVER'))
    }
    dialect = dialectConfigURL.get("drivername")
    # When connecting to a SQL Server named instance,
    # need instance name OR port number, not both.
    if 'mssql' in dialect:
        # So if named instance
        if '\\' in dialectConfigURL.get("host"):
            # remove port number
            del dialectConfigURL["port"]
    return dialectConfigURL


def buildURL(myConfig, db):
    """
    Will create connection string with URL
    method from sqlalchemy.engine.url with values set in *.ini config file

    ``myConfig``
        Dict created from *.ini config file.

    ``db``
        META name of db used could be MAIN_DB, SENSOR_DB, EXPORT_DB, LOG_DB.
    """
    checkConfigURL(myConfig, db)
    dictDialectConfigURL = buildConfigURLAccordingToDialect(myConfig, db)
    return URL(**dictDialectConfigURL)


def createEngines(myConfig, dbPossible):
    engines = {}
    for item in dbPossible:
        engines[item] = engine_from_config(
            configuration=myConfig,
            prefix='sqlalchemy.' + item + '.',
            url=buildURL(myConfig=myConfig, db=item),
            legacy_schema_aliasing=False,
            implicit_returning=False,
            use_scope_identity=False
        )
        mapAndBindEngineWithBaseWeUse(item, engines[item])
        '''
        that shouldn't be here but for now... dont have choice
        '''

    return engines


def mapAndBindEngineWithBaseWeUse(baseName, engineToBind):
    '''
    dunno if it's the good way
    but (maybe it's just for dev and not for production )
    take a coffee and read carefully...
    if we stop execution of script here
    and we looks in globals()
    the class Main_Db_Base is imported and defined
    so we can bind metadata with engine directly
    '''

    # print("et le global ? ? ? ?")
    print("Binding Engine for {baseName}_Base".format(baseName=baseName))
    eval(str(baseName)+'_Base').metadata.bind = engineToBind
    # will drop all model and recreate it
    # if you need data test youshould restore juste after
    # eval( str(baseName)+'_BASE' ).metadata.drop_all(engineToBind)
    # create models only if table don't exist yet!!
    print("Create ALL for {baseName}_Base".format(baseName=baseName))
    eval(str(baseName)+'_Base').metadata.create_all(engineToBind)
    print("Reflectdatabase {baseName}_Base".format(baseName=baseName))
    eval(str(baseName)+'_Base').metadata.reflect(
                                                views=True,
                                                extend_existing=False
                                                )  # scan database


def get_session_factory(engines):
    factory = sessionmaker(autoflush=True)

    # class on fly
    # yeah i know that's not cool
    # engine classes name are dynamical that's all
    engineClassesDict = {}
    for item in engines:
        engineClassesDict[eval(str(item)+'_Base')] = engines[item]

    factory.configure(binds=engineClassesDict)
    return factory


def get_session(request):
    session = request.registry.get('dbsession_factory')()
    session.begin_nested()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
            session.close()
        else:
            try:
                session.commit()
            except Exception as e:
                print_exc()
                session.rollback()
                request.response.status_code = 500
            finally:
                session.close()

    request.add_finished_callback(cleanup)

    return session


def new_request(event):
    request = event.request
    request.set_property(get_session, 'dbsession', reify=True)