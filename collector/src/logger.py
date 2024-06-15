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
        Configuration for FUZE logging system
"""

import os
import logging

DEBUG = os.getenv("DEBUG", "true")

class Logger:
    """
    Logging system for FUZE
    """
    def __init__(self):
        self.level = logging.DEBUG if DEBUG else logging.INFO

    def set_logging(self):
        logger = logging.getLogger()
        logger.setLevel(self.level)
