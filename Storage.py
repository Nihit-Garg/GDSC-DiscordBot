import json
import os
import logging

logger = logging.getLogger('discord')

def ensure_data_directory():
    """Ensure the data directory exists"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            logger.info("Created data directory")
    except Exception as e:
        logger.error(f"Error creating data directory: {e}")
        raise

def save_json(filepath: str, data: dict):
    """Save data to a JSON file"""
    try:
        ensure_data_directory()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logger.error(f"Error saving to {filepath}: {e}")
        raise

def load_json(filepath: str) -> dict:
    """Load data from a JSON file"""
    try:
        ensure_data_directory()
        if not os.path.exists(filepath):
            logger.info(f"File {filepath} does not exist, returning empty dict")
            return {}
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return {}