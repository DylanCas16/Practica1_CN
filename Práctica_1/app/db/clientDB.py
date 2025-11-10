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
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id VARCHAR(36) PRIMARY KEY,
                    client_id VARCHAR(9) NOT NULL,
                    event_name VARCHAR(64) NOT NULL,
                    client_name VARCHAR(64) NOT NULL,
                    ticket_type VARCHAR(16) DEFAULT 'NORMAL' CHECK (ticket_type IN ('NORMAL','VIP','SUPERVIP')),
                    comments TEXT
                );
            """)

    def create_ticket(self, ticket: Ticket) -> Ticket:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = """
                INSERT INTO tickets (ticket_id, client_id, event_name, 
                client_name, ticket_type, comments)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                ticket.ticket_id,
                ticket.client_id,
                ticket.event_name,
                ticket.client_name,
                ticket.ticket_type,
                ticket.comments
            ))
        return ticket
            

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM tickets WHERE ticket_id = %s", (ticket_id,))
            result = cursor.fetchone()
            if result:
                return Ticket(**result)
        return None

    def get_all_tickets(self) -> List[Ticket]:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM tickets")
            results = cursor.fetchall()
            tickets = []
            for row in results:
                tickets.append(Ticket(**row))
            return tickets

    def update_ticket(self, ticket_id: str, ticket: Ticket) -> Optional[Ticket]:
        with self.connection.cursor() as cursor:
            sql = """
                UPDATE tickets
                SET client_id = %s,
                    client_name = %s,
                    ticket_type = %s,
                    comments = %s
                WHERE ticket_id = %s
            """
            cursor.execute(sql, (
                ticket.client_id,
                ticket.client_name,
                ticket.ticket_type,
                ticket.comments,
                ticket_id
            ))
            if cursor.rowcount > 0:
                return self.get_ticket(ticket_id)
        return None

    def delete_ticket(self, ticket_id: str) -> bool:
        with self.connection.cursor() as cur:
            cur.execute("DELETE FROM tickets WHERE ticket_id = %s", (ticket_id,))
            return cur.rowcount > 0