CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE my_keyspace;

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY,
    content TEXT
);
