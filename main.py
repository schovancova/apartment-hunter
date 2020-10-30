#!/usr/bin/env python3
import configparser
import os
from src.ulov_domov import UlovDomov
from src.notifier import send_email
from tinydb import TinyDB, Query
import logging
import time

if __name__ == "__main__":
    db_path = 'db/main.db'
    config = configparser.ConfigParser()
    config.read('configs/apartments.ini')
    open(db_path, 'a+')
    db = TinyDB(db_path)

    # UlovDomov
    ulov_domov = UlovDomov(**config._sections["ulov_domov"])
    Apartment = Query()

    logger = logging.getLogger('apartment_logger')
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting scraping")

    while True:
        apartments = ulov_domov.get_new_apartments()
        newest = apartments[0]['published_at']
        logging.info(f"New batch acquired, newest apartment is from {newest}")
        for ap in apartments:
            saved = db.search(Apartment.id == ap["id"])
            if not saved:
                logging.info("Sent an email with new apartment")
                subject, message = ulov_domov.get_email_message(ap)
                send_email(subject, message)
                ulov_domov.save_apartment_into_db(db, ap)
        logging.info("Finished inspection of apartment batch, sleep for 3 minutes")
        time.sleep(180)
