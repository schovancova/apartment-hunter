#!/usr/bin/env python3
import configparser
import os
from src.ulov_domov import UlovDomov
from src.bez_realitky import BezRealitky
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

    #Bezrealitky
    bez_realitky = BezRealitky(**config._sections["bez_realitky"])

    logger = logging.getLogger('apartment_logger')
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Using filters {config._sections['ulov_domov']}")
    logging.info(f"Using filters {config._sections['bez_realitky']}")

    while True:
        if config["ulov_domov"]["active"] == "true":
            apartments = ulov_domov.get_new_apartments()
            newest = apartments[0].get('published_at')
            logging.info(f"New batch for UlovDomov acquired, newest apartment is from {newest}")
            for ap in apartments:
                saved = db.search(Apartment.id == ap["id"])
                if not saved:
                    logging.info("Sent an email with new apartment")
                    subject, message = ulov_domov.get_email_message(ap)
                    send_email(subject, message)
                    ulov_domov.save_apartment_into_db(db, ap)
            logging.info("Finished inspection of apartment batch")
        if config["bez_realitky"]["active"] == "true":
            apartments = bez_realitky.get_new_apartments()
            newest = apartments[0].get('timeOrder').get('date')
            logging.info(f"New batch for BezRealitky acquired, newest apartment is from {newest}")
            for ap in apartments:
                saved = db.search(Apartment.id == ap["id"])
                if not saved:
                    logging.info("Sent an email with new apartment")
                    subject, message = bez_realitky.get_email_message(ap)
                    send_email(subject, message)
                    bez_realitky.save_apartment_into_db(db, ap)
            logging.info("Finished inspection of apartment batch")

        time.sleep(180)
