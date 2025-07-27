-- Generate 500 comments (active community engagement)
INSERT INTO comment_replies (post_id, user_id, content, timestamp)
WITH comment_contents AS (
  SELECT unnest(ARRAY[
    'This resonates so much! Keep going! 💪',
    'Thank you for sharing your journey! 💝',
    'We''re all here for you! 🤗',
    'So proud of your progress! 🌟',
    'This is exactly what I needed to hear today. 💫',
    'You''re doing amazing! Keep it up! ✨',
    'Such an inspiration to us all! 🌸',
    'One day at a time - you''ve got this! 💖',
    'Your strength is admirable! 🙏',
    'This community is better because of people like you! 🌱',
    'I can relate to this so much. Stay strong! 💕',
    'What a beautiful reflection. Thank you! ✨',
    'This journey isn''t easy, but you''re crushing it! 💪',
    'So much wisdom in your words! 🌟',
    'Keep sharing your light! We need it! 💝'
  ]) as content
)
SELECT 
  (SELECT post_id FROM community_posts ORDER BY random() LIMIT 1),
  (SELECT user_id FROM user_info ORDER BY random() LIMIT 1),
  content || ' Week ' || (SELECT week FROM user_info WHERE user_id = (SELECT user_id FROM user_info ORDER BY random() LIMIT 1)) || ' here.',
  (TIMESTAMP '2025-07-24 00:00:00' - (random() * interval '60 days'))::text
FROM comment_contents, generate_series(1, 33);
