import gc
import logging
import textwrap


class MyLogger(logging.Logger):
    def __init__(self, name, create_level='INFO', enable_logging=True):
        super().__init__(name, create_level)
        self.enable_logging = enable_logging

    def mylev(self, msg_level, message, *args, **kwargs):
        if self.enable_logging:
            self.log(msg_level, message, *args, **kwargs)

    def set_logging_enabled(self, enable_logging):
        self.enable_logging = enable_logging
    


def check_loggers():
    """
    ldict = logging.Logger.manager.loggerDict
    print('log_dict:')
    print(ldict)
    for logger_name, logger in logging.Logger.manager.loggerDict.items():
        print(f"Logger Name: {logger_name}, Module: {logger.name}")
        logger.critical(f"Logger Name: {logger_name}, Module: {logger.name}")
    """
    pass
    """
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        print(str(handler))
        if isinstance(handler, logging.StreamHandler):
            continue
        for logger_name, logger in handler.loggerDict.items():
            print(f"Logger Name: {logger_name}, Module: {logger.name}")
    """

def find_logging_objects():
    logging_objects = []
    for obj in gc.get_objects():
        if isinstance(obj, logging.Logger):
            logging_objects.append(obj)
    print(f"{'Logger Name':<20}{'Logger Level':<15}{'Handlers':<10}{'Filters':<10}{'Is Disabled':<15}{'Propagate':<10}{'Module':<20}")
    for logger in logging_objects:
        logger_name = logger.name
        logger_level = logging.getLevelName(logger.level)
        handlers_count = len(logger.handlers)
        filters_count = len(logger.filters)
        is_disabled = logger.disabled
        propagate = logger.propagate
        module_name = logger.__module__

        formatted_logger_name = textwrap.shorten(logger_name, width=18, placeholder="...")
        formatted_module_name = textwrap.shorten(module_name, width=18, placeholder="...")
        print(f"{formatted_logger_name:<20}{logger_level:<15}{handlers_count:<10}{filters_count:<10}{is_disabled:<15}{propagate:<10}{formatted_module_name:<20}")



def main(my_logger_name='test_name',
         my_logger_level_creating=30,
         my_logger_level_messaging=30,
         enable_logging=True, msg='empty_msg'):
    
    logging.basicConfig(level='DEBUG')

    # Создадим стандартный логгер
    logger = logging.getLogger()

    logger.info('*****************************************************')
    logger.info('Создаем экземпляр MyLogger с заданным уровнем и состоянием логирования')
    logger.info(f'MyLogger object creating level: {my_logger_level_creating}')
    logger.info(f'MyLogger object messaging level: {my_logger_level_messaging}')
    my_logger = MyLogger(my_logger_name,
                         my_logger_level_creating, enable_logging)

    logger.info('*****************************************************')
    logger.info('Checking all loggers')
    # my_logger.check_loggers()
    # check_loggers()
    find_logging_objects()
    # Выведем содержимое loggerDict после создания логгеров
    # print("loggerDict after creating loggers:")
    # print(logging.Logger.manager.loggerDict)

    logger.info('*****************************************************')
    logger.info('Используем метод mylev для логирования')
    # msg = 'This is a DEBUG level message using mylev.'
    my_logger.mylev(my_logger_level_messaging, msg)

    logger.info('*****************************************************')
    logger.info('Отключаем логирование')
    my_logger.set_logging_enabled(False)
    my_logger.mylev(my_logger_level_messaging, 'This message will not be logged.')

    logger.info('*****************************************************')
    logger.info('Включаем логирование')
    my_logger.set_logging_enabled(True)
    my_logger.mylev(my_logger_level_messaging,
                    f'This is an {my_logger_level_messaging} level message and it will be logged.')

if __name__ == '__main__':
    name = 'test_logger'
    my_logger_level_creating = 30
    my_logger_level_messaging = 30
    enable_logging = True
    msg = 'TESTING MESSAGE'
    main(name,my_logger_level_creating,my_logger_level_messaging,enable_logging,msg)