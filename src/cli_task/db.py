import sqlite3
import logging
from pathlib import Path

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CONFIG_DIR = Path.home() / ".config" / "cli-task"
DB_PATH = CONFIG_DIR / "tasks.db"

def ensure_config_dir():
	"""
	Ensure the configuration directory exists.

	Raises:
		OSError: If the directory cannot be created.
	"""
	try:
		CONFIG_DIR.mkdir(parents=True, exist_ok=True)
		logger.info(f"Config directory ready at {CONFIG_DIR}")
	except Exception as e:
		logger.error(f"Failed to create config directory: {e}")
		raise

def init_db():
	"""
	Initialize the SQLite database and create the tasks table if it doesn't exist.

	Raises:
		sqlite3.Error: If SQL execution fails.
	"""
	ensure_config_dir()
	try:
		conn = sqlite3.connect(DB_PATH)
		conn.execute("PRAGMA foreign_keys = ON;")
		conn.execute("""
			CREATE TABLE IF NOT EXISTS tasks (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL,
				description TEXT,
				due_date TEXT,
				priority INTEGER,
				status TEXT DEFAULT 'pending',
				created_at TEXT DEFAULT CURRENT_TIMESTAMP,
				updated_at TEXT
			)
		""")
		conn.commit()
		conn.close()
		logger.info(f"Database initialized at {DB_PATH}")
	except sqlite3.Error as e:
		logger.error(f"SQLite error during init_db: {e}")
		raise

def get_db():
	"""
	Open and return a SQLite connection with foreign keys enabled.

	Returns:
		sqlite3.Connection: Open database connection.

	Raises:
		sqlite3.Error: If the database file cannot be opened.
	"""
	ensure_config_dir()
	try:
		conn = sqlite3.connect(DB_PATH)
		conn.execute("PRAGMA foreign_keys = ON;")
		return conn
	except sqlite3.Error as e:
		logger.error(f"Failed to open database: {e}")
		raise	 