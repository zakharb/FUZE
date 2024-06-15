"""
    FUZE
    AI Ruleness SIEM for OT/ICS
    Copyright (C) Zakhar Bernhardt 2022

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Description:
        The starting point to start the FUZE
"""

import logging
import asyncio
from config import Config
from logger import Logger
from modules.core import Core

if __name__ == "__main__":
    logger = Logger()
    logger.set_logging()
    logging.info("[*] FUZE Copyright (C) 2022 Zakhar Bernhardt")
    logging.info("""
        ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░ 
        ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░        
        ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓██▓▒░░▒▓█▓▒░        
        ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██▓▒░  ░▒▓██████▓▒░   
        ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██▓▒░    ░▒▓█▓▒░        
        ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
        ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
    \n""")
    logging.info(f'[+] Logging level: {logger.level}')
    logging.info('[*] Reading configuration')
    config = Config()
    config.read()
    logging.info('[+] Loaded configuration:')
    logging.info(f'[+] Collectors: {len(config.collector)}')
    logging.info(f'[+] Normalizer rules: {len(config.normalizer)}')
    logging.info(f'[+] Fuzer rules: {len(config.fuzer)}')
    logging.info('[*] Starting all modules for FUZE')
    core = Core(collector=config.collector, 
                normalizer=config.normalizer, 
                fuzer=config.fuzer)
    asyncio.run(core.start())

