-- ============================================================
-- SUPABASE SCHEMA: Message Board for Control Tower
-- Run this in Supabase SQL Editor (Dashboard → SQL Editor → New query)
-- ============================================================

-- 1. Messages table
CREATE TABLE IF NOT EXISTS messages (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  q_num      INTEGER NOT NULL,
  sender     TEXT NOT NULL CHECK (sender IN ('pmp', 'inventor')),
  text       TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  read_by    TEXT[] DEFAULT '{}'::TEXT[] NOT NULL
);

-- Index for quick per-question queries
CREATE INDEX IF NOT EXISTS idx_messages_q_num ON messages (q_num, created_at);

-- 2. Enable Row-Level Security
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Allow anyone with the anon key to read all messages
CREATE POLICY "Anyone can read messages"
  ON messages FOR SELECT
  USING (true);

-- Allow anyone with the anon key to insert messages
CREATE POLICY "Anyone can insert messages"
  ON messages FOR INSERT
  WITH CHECK (true);

-- Allow anyone with the anon key to update messages (for read receipts)
CREATE POLICY "Anyone can update messages"
  ON messages FOR UPDATE
  USING (true);

-- Allow anyone with the anon key to delete messages (for archiving)
CREATE POLICY "Anyone can delete messages"
  ON messages FOR DELETE
  USING (true);

-- 3. Function: atomically mark a message as read by a role
CREATE OR REPLACE FUNCTION mark_read(msg_id UUID, reader TEXT)
RETURNS VOID AS $$
BEGIN
  UPDATE messages
  SET read_by = array_append(read_by, reader)
  WHERE id = msg_id
    AND NOT (read_by @> ARRAY[reader]);
END;
$$ LANGUAGE plpgsql;

-- 4. Enable Realtime for the messages table
ALTER PUBLICATION supabase_realtime ADD TABLE messages;
