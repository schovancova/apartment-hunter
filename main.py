#!/usr/bin/env python3
"""Main script"""
import logging
import time
from src.sites.ulov_domov import UlovDomov
from src.sites.bez_realitky import BezRealitky
from src.utils.config_validator import validate_config
from src.utils.common import get_config, get_db, get_logger
from src.notifiers.mailer import send_email
from src.notifiers.pushbullet import send_push_message
from src.notifiers.slack import send_slack_message
import src.utils.constants as const


def main():
    """Main script"""
    config = get_config(const.CONFIG_PATH)
    validate_config(config)
    database = get_db(const.DB_PATH)
    logger = get_logger()
    ulov_domov = UlovDomov(**dict(config.items(const.ULOVDOMOV_NAME)))
    bez_realitky = BezRealitky(**dict(config.items(const.BEZREALITKY_NAME)))
    while True:
        if ulov_domov.active:
            for apartment in ulov_domov.get_new_apartments():
                logger.info(apartment.url)
                if not ulov_domov.is_in_db(database, apartment.id):
                    logging.info("Sent an email with new apartment")
                    subject, message = ulov_domov.get_email_message(apartment)
                    send_email(subject, message)
                    send_push_message(subject, message, apartment.url)
                    send_slack_message(subject, apartment.url)
                    ulov_domov.save_apartment_into_db(database, apartment.id)
            logging.info("Finished inspection of apartment batch")
        if bez_realitky.active:
            for apartment in bez_realitky.get_new_apartments():
                logger.info(apartment.url)
                if not bez_realitky.is_in_db(database, apartment.id):
                    logging.info("Sent an email with new apartment")
                    subject, message = bez_realitky.get_email_message(apartment)
                    send_email(subject, message)
                    send_push_message(subject, message, apartment.url)
                    send_slack_message(subject, apartment.url)
                    bez_realitky.save_apartment_into_db(database, apartment.id)
            logging.info("Finished inspection of apartment batch")
        time.sleep(180)


if __name__ == "__main__":
    main()
