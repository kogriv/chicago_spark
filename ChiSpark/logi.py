import logging
from enviserv.mylog import MyLogger, MyLoggerSuper, find_logging_objects


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
#cnlog = MyLogger(name='ch', create_level='INFO', enable_logging=True)
cnlog = MyLoggerSuper(name='ch', create_level='INFO', enable_logging=True)


print('WARN test message -- print')
cnlog.mylev(30, 'WARN test message from mylog')
logger.warning('WARN test message from logger')
print('INFO test message -- print')
cnlog.mylev(20, 'INFO test message from mylog')
logger.info('INFO test message from logger')
print('DEBUG test message -- print')
cnlog.mylev(10, 'DEBUG test message from mylog')
logger.debug('DEBUG test message from logger')

print("*******************************************************************************************")
print("*** logger objects: ***********************************************************************")
find_logging_objects()