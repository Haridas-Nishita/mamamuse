-- Generate mood logs (daily entries for each user over 60 days)
INSERT INTO mood_log (user_id, mood_value, timestamp)
SELECT 
  user_id,
  floor(random() * 3 + 3)::integer,  -- Random mood between 3-5 (generally positive)
  (TIMESTAMP '2025-07-24 00:00:00' - (generate_series || ' days')::interval)::text
FROM user_info, generate_series(0, 59)  -- 60 days of mood logs
WHERE random() < 0.8;  -- 80% chance of logging mood each day

-- Add some variation with lower moods (ensuring realistic patterns)
INSERT INTO mood_log (user_id, mood_value, timestamp)
SELECT 
  user_id,
  floor(random() * 2 + 1)::integer,  -- Random mood between 1-2 (challenging days)
  (TIMESTAMP '2025-07-24 00:00:00' - (generate_series || ' days')::interval)::text
FROM user_info, generate_series(0, 59)  -- 60 days of mood logs
WHERE random() < 0.2;  -- 20% chance of having a challenging day
