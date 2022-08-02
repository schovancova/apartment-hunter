#!/usr/bin/env python3
"""Main script"""
import logging
import time
import traceback

from src.sites.sreality import Sreality
from src.utils.notifier import Notifier
from src.sites.ulov_domov import UlovDomov
from src.sites.bez_realitky import BezRealitky
from src.validation.config_validator import validate_config
from src.utils.common import get_config, get_db, get_logger, determine_frequency
from src.validation.definitions import SITES_VALIDATORS
import src.utils.constants as const


def main():
    """Main script"""
    config = get_config(const.CONFIG_PATH)
    validate_config(config, definition=SITES_VALIDATORS)
    database = get_db()
    logger = get_logger()

    general_config = dict(config.items('general'))
    ulovdomov_config = dict(config.items(const.ULOVDOMOV_NAME))
    bezrealitky_config = dict(config.items(const.BEZREALITKY_NAME))
    sreality_config = dict(config.items(const.SREALITY_NAME))
    sites = [site for site in [
        UlovDomov(**(ulovdomov_config | general_config)),
        BezRealitky(**(bezrealitky_config | general_config)),
        Sreality(**(sreality_config | general_config))] if site.enabled]

    notifier = Notifier()
    while True:
        for site in sites:
            try:
                for apartment in site.get_new_apartments():
                    logger.info(apartment.url)
                    if not site.is_in_db(database, apartment.id):
                        subject, message = site.get_email_message(apartment)
                        notifier.notify_all(subject, message, apartment.url)
                        logging.info(f"New apartment found {apartment.url}")
                        site.save_apartment_into_db(database, apartment.id, apartment.url)
            except Exception as ex:
                notifier.notify_all(f"It dropped for site *{site.site}*", traceback.format_exc(), "Boohoo. Will be retrying soon")
        freq = determine_frequency()
        time.sleep(freq)


if __name__ == "__main__":
    main()
