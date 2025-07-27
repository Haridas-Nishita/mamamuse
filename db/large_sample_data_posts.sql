-- Generate 300 community posts (simulating regular user engagement)
INSERT INTO community_posts (post_id, user_id, content, timestamp)
WITH post_contents AS (
  SELECT unnest(ARRAY[
    'Starting to see real progress in my journey. Small steps matter! 💫',
    'Feeling grateful for this supportive community. You all make such a difference! 💝',
    'Had a breakthrough in therapy today. Keep pushing forward everyone! 🌟',
    'Some days are harder than others, but we''re in this together. 🤗',
    'Learning to be kind to myself. It''s a process but worth it. 💪',
    'Celebrating small victories today. Every step counts! ✨',
    'Discovered new coping strategies that really help. Happy to share! 🌸',
    'Remember: you''re stronger than you think. Keep going! 💖',
    'Grateful for another day of growth and healing. 🙏',
    'Taking it one day at a time. Progress isn''t always linear. 🌱'
  ]) as content
)
SELECT 
  'post' || generate_series || '_' || floor(random() * 1000)::text,
  (SELECT user_id FROM user_info ORDER BY random() LIMIT 1),
  content || ' Week ' || (SELECT week FROM user_info WHERE user_id = (SELECT user_id FROM user_info ORDER BY random() LIMIT 1)) || ' update.',
  (TIMESTAMP '2025-07-24 00:00:00' - (random() * interval '60 days'))::text
FROM post_contents, generate_series(1, 30);
