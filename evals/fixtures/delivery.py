def initialize(db):
    db.executescript("""
        CREATE TABLE inventory (quantity INTEGER NOT NULL);
        INSERT INTO inventory VALUES (0);
        CREATE TABLE receipts (message_id TEXT PRIMARY KEY);
    """)


def apply_delivery(db, message_id, quantity):
    with db:
        db.execute("UPDATE inventory SET quantity = quantity + ?", (quantity,))
        db.execute("INSERT OR IGNORE INTO receipts VALUES (?)", (message_id,))
