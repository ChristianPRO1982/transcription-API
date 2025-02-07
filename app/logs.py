from datetime import datetime, timedelta
import logging
import os



def init_log()->bool:
    try:
        DEBUG = os.getenv("DEBUG")
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        os.makedirs('./logs/', exist_ok=True)
        log_filename = f"./logs/{date_str}.log"

        if DEBUG == '1':
            print("§§§§§§§§§§§§§§§§§§§§§§")
            print("§§§§§ DEBUG MODE §§§§§")
            print("§§§§§§§§§§§§§§§§§§§§§§")
            logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.getLogger("azure").setLevel(logging.INFO)
        else:
            logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.getLogger("azure").setLevel(logging.CRITICAL)
        
        cleanup_log()
        return True
    
    except Exception as e:
        print(f"Error in logging.py init_log(): {e}")
        return False


def cleanup_log():
    retention_days = int(os.getenv('LOG_RETENTION_DAYS', '30'))
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    for log_file in os.listdir('./logs/'):
        log_path = os.path.join('./logs/', log_file)
        if os.path.isfile(log_path):
            try:
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(log_path))
                if file_mod_time < cutoff_date:
                    os.remove(log_path)
                    logging_msg(f"Suppression de {log_file}", 'DEBUG')
                else:
                    logging_msg(f"{log_file} n'a pas été supprimé", 'DEBUG')

            except Exception as e:
                logging_msg(f"Erreur lors de la suppression de {log_file}: {e}", 'WARNING')


def logging_msg(msg, type='INFO')->bool:
    try:
        logger = logging.getLogger(__name__)
        # print(logging.getLevelName(logger.getEffectiveLevel()))

        type = type.upper()

        if type == 'INFO':
            logger.info(msg)
        elif type == 'DEBUG':
            logger.debug(msg)
        elif type == 'ERROR':
            logger.error(msg)
        elif type == 'WARNING':
            logger.warning(msg)
        elif type == 'CRITICAL':
            logger.critical(msg)
        else:
            raise ValueError("Invalid log type")

        if type != 'DEBUG':
            print(f"[{type}] {msg}")

        return True

    except Exception as e:
        print(f"Error in logging.py logging_msg(): {e}")
        return False