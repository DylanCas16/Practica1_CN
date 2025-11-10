import psycopg2
import psycopg2.extras
import json
from typing import List, Optional
from models.ticket import Ticket
import os

class PostgresDatabase:
    
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        self.connection.autocommit = True
        self.initialize()
    
    def initialize(self):
        """Crea la tabla tickets si no existe"""
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id VARCHAR(36) PRIMARY KEY,
                    client_id VARCHAR(9) NOT NULL,
                    event_name VARCHAR(100) NOT NULL,
                    client_name VARCHAR(64) NOT NULL,
                    ticket_type VARCHAR(10) DEFAULT 'NORMAL' CHECK (ticket_type IN ('NORMAL','VIP','SUPERVIP')),
                    comments TEXT,
                    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_date DATE
                );
            """)

    def create_ticket(self, ticket: Ticket) -> Ticket:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            try:
                sql = """
                    INSERT INTO tickets (ticket_id, client_id, event_name, client_name, ticket_type, comments, purchase_date, event_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *;
                """
                cur.execute(sql, (
                    ticket.ticket_id,
                    ticket.client_id,
                    ticket.event_name,
                    ticket.client_name,
                    ticket.ticket_type,
                    ticket.comments,
                    ticket.purchase_date,
                    ticket.event_date
                ))
                self.connection.commit()
                return ticket
            except Exception as e:
                self.connection.rollback()
                raise

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM tickets WHERE ticket_id = %s", (ticket_id,))
            row = cur.fetchone()
            return Ticket(**row) if row else None

    def get_all_tickets(self) -> List[Ticket]:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM tickets ORDER BY purchase_date DESC")
            rows = cur.fetchall()
            return [Ticket(**row) for row in rows]

    def update_ticket(self, ticket_id: str, ticket: Ticket) -> Optional[Ticket]:
        ticket.update_timestamp()
        with self.connection.cursor() as cur:
            sql = """
                UPDATE tickets
                SET client_id = %s,
                    client_name = %s,
                    ticket_type = %s,
                    comments = %s,
                    purchase_date = %s
                WHERE ticket_id = %s
                RETURNING *;
            """
            cur.execute(sql, (
                ticket.client_id,
                ticket.client_name,
                ticket.ticket_type,
                ticket.comments,
                ticket.purchase_date,
                ticket_id
            ))
            row = cur.fetchone()
            return Ticket(**row) if row else None

    def delete_ticket(self, ticket_id: str) -> bool:
        with self.connection.cursor() as cur:
            cur.execute("DELETE FROM tickets WHERE ticket_id = %s", (ticket_id,))
            return cur.rowcount > 0