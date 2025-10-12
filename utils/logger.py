import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Codes ANSI pour les couleurs console
COLORS = {
    "INFO": "\033[1;32m",  # Vert
    "WARNING": "\033[1;33m",  # Jaune
    "ERROR": "\033[1;31m",  # Rouge
    "CRITICAL": "\033[1;41m",  # Rouge avec fond
    "RESET": "\033[0m"
}

# Emojis associés aux niveaux
EMOJIS = {
    "INFO": "✅",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "🔥"
}


class ColorFormatter(logging.Formatter):
    """Formatter console avec couleurs + infos de contexte (fichier, fonction, ligne)."""

    def format(self, record):
        level = record.levelname
        emoji = EMOJIS.get(level, "")
        color = COLORS.get(level, "")
        reset = COLORS["RESET"]

        # === Format différent selon le niveau ===
        if level == "INFO":
            # Format simple (sans fichier/ligne)
            log_fmt = f"{emoji} [%(levelname)s] - %(message)s"
        elif level in ["WARNING", "ERROR", "CRITICAL"]:
            # Format détaillé avec fichier, fonction et ligne
            log_fmt = (
                f"{emoji} [%(levelname)s] "
                f"[%(filename)s: %(funcName)s(%(lineno)d)] - %(message)s"
            )
        else:
            log_fmt = f"[%(levelname)s] - %(message)s"

        # Appliquer le format
        formatter = logging.Formatter(log_fmt)
        log_msg = formatter.format(record)

        # === Coloration du texte ===
        if level == "INFO":
            # Colorer uniquement le tag [INFO]
            log_msg = log_msg.replace("[INFO]", f"{COLORS['INFO']}[INFO]{COLORS['RESET']}")
        elif level in ["WARNING", "ERROR", "CRITICAL"]:
            # Colorer toute la ligne
            log_msg = f"{color}{log_msg}{reset}"

        return log_msg


class Logger:
    def __init__(self, log_file="app.log"):
        # === AJOUT : dossier logs à la racine ===
        base_dir = Path.cwd()
        logs_dir = base_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        # === Chemin complet du fichier log ===
        log_path = logs_dir / log_file
        log_file = str(log_path)

        # === Initialisation du logger ===
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        # Nettoyer les handlers existants pour éviter les doublons
        if self.logger.handlers:
            for h in list(self.logger.handlers):
                self.logger.removeHandler(h)

        # Formatter fichier pour INFO & CRITICAL (sans fichier/ligne)
        file_formatter_simple = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(funcName)s(%(lineno)d)] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Formatter fichier pour WARNING & ERROR (avec fichier/ligne)
        file_formatter_full = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s in %(funcName)s(%(lineno)d)] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        class InfoCritFilter(logging.Filter):
            def filter(self, record):
                return record.levelno in (logging.INFO, logging.CRITICAL)

        class WarnErrorFilter(logging.Filter):
            def filter(self, record):
                return record.levelno in (logging.WARNING, logging.ERROR)

        # Handler fichier pour INFO & CRITICAL
        self.file_handler_simple = RotatingFileHandler(
            log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        self.file_handler_simple.setLevel(logging.INFO)
        self.file_handler_simple.addFilter(InfoCritFilter())
        self.file_handler_simple.setFormatter(file_formatter_simple)
        self.logger.addHandler(self.file_handler_simple)

        # Handler fichier pour WARNING/ERROR
        self.file_handler_full = RotatingFileHandler(
            log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        self.file_handler_full.setLevel(logging.WARNING)
        self.file_handler_full.addFilter(WarnErrorFilter())
        self.file_handler_full.setFormatter(file_formatter_full)
        self.logger.addHandler(self.file_handler_full)

        # Handler console coloré
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(ColorFormatter())
        self.logger.addHandler(console_handler)

    # Wrappers avec stack-level pour pointer sur ton code (et non logger.py)
    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, stacklevel=2, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, stacklevel=2, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, stacklevel=2, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, stacklevel=2, **kwargs)

    def separator(self):
        """Ajoute une ligne de séparation uniquement dans le fichier de LOG."""
        if self.file_handler_simple:
            self.file_handler_simple.stream.write("-" * 80 + "\n")
            self.file_handler_simple.flush()
