#!/usr/bin/env python3
import configparser
import os
from src.sites.ulov_domov import UlovDomov
from src.sites.bez_realitky import BezRealitky
from src.objects.bez_realitky_apartment import BezRealitkyApartment
from src.objects.ulov_domov_apartment import UlovDomovApartment
from src.utils.notifier import send_email
from src.utils.config_validator import validate_config
from src.utils.common import get_config, get_db, get_logger
import src.utils.constants as const
import logging
import time

if __name__ == "__main__":
    config = get_config(const.CONFIG_PATH)
    validate_config(config)
    db = get_db(const.DB_PATH)
    logger = get_logger()

    ulov_domov = UlovDomov(**dict(config.items(const.ULOVDOMOV_NAME)))
    bez_realitky = BezRealitky(**dict(config.items(const.BEZREALITKY_NAME)))

    while True:
        if ulov_domov.active:
            for ap in ulov_domov.get_new_apartments():
                logger.info(ap.url)
                if not ulov_domov.is_in_db(db, ap.id):
                    logging.info("Sent an email with new apartment")
                    subject, message = ulov_domov.get_email_message(ap)
                    #send_email(subject, message)
                    #ulov_domov.save_apartment_into_db(db, ap.id)
            logging.info("Finished inspection of apartment batch")
        if bez_realitky.active:
            for ap in bez_realitky.get_new_apartments():
                logger.info(ap.url)
                if not bez_realitky.is_in_db(db, ap.id):
                    logging.info("Sent an email with new apartment")
                    subject, message = bez_realitky.get_email_message(ap)
                    #send_email(subject, message)
                    #bez_realitky.save_apartment_into_db(db, ap.id)
            logging.info("Finished inspection of apartment batch")

        time.sleep(180)
