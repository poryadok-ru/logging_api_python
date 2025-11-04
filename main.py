from log import Log
from datetime import datetime

logger = Log(token="f95e9305-107e-4967-ad3f-c65c70e8930a")

def main():
    logger.info("Приложение запущено")
    
    start_time = datetime.now()
    
    try:
        logger.debug("Выполнение основной логики...")
        
        logger.info("Обработка данных...")
        
        logger.warning("Некоторые данные отсутствуют")
        
        end_time = datetime.now()
        
        logger.finish_success(
            period_from=start_time,
            period_to=end_time,
            host="my-server",
            duration_seconds=(end_time - start_time).total_seconds()
        )
        
    except Exception as e:
        end_time = datetime.now()
        
        logger.error(f"Произошла ошибка: {e}")
        
        logger.finish_error(
            period_from=start_time,
            period_to=end_time,
            host="my-server",
            error=str(e)
        )

if __name__ == "__main__":
    main()
