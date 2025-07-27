-- Set Priya's user info and preferences
UPDATE user_info 
SET 
    name = 'Priya',
    current_week = 8,
    login_streak = 45,
    total_logins = 52
WHERE user_id = 'a321ac09-0528-4753-a380-57887ad343d2';

-- Create chat entries for Priya
INSERT INTO chat_entries (user_id, message, is_bot, timestamp) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 'Hi! I''ve been feeling a bit overwhelmed lately with work.', false, '2025-07-24 10:15:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 'I understand that feeling of being overwhelmed. Let''s break down what''s causing this stress. Can you tell me more about your work situation?', true, '2025-07-24 10:15:30'),
('a321ac09-0528-4753-a380-57887ad343d2', 'Well, I have multiple deadlines coming up and I''m struggling to manage my time effectively.', false, '2025-07-24 10:16:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 'That''s a common challenge. Have you tried creating a priority list? We can work on time management strategies together.', true, '2025-07-24 10:16:30'),
('a321ac09-0528-4753-a380-57887ad343d2', 'That would be really helpful! I haven''t tried organizing my tasks that way.', false, '2025-07-24 10:17:00');

-- Create Priya's community posts
INSERT INTO community_posts (user_id, content, week_number, timestamp) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 'Just completed Week 7! The breathing exercises have really helped me stay centered during stressful moments at work. Anyone else finding them helpful?', 7, '2025-07-17 15:30:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 'Starting Week 8 with renewed energy! The journey so far has been transformative. Thank you everyone for your support!', 8, '2025-07-24 09:00:00');

-- Create mood logs for Priya (last 7 days)
INSERT INTO mood_log (user_id, mood_value, timestamp) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 4, '2025-07-24 08:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 3, '2025-07-23 08:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 4, '2025-07-22 08:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 5, '2025-07-21 08:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 2, '2025-07-20 08:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 4, '2025-07-19 08:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 3, '2025-07-18 08:00:00');

-- Add supports to Priya's posts
WITH priya_posts AS (
    SELECT post_id FROM community_posts 
    WHERE user_id = 'a321ac09-0528-4753-a380-57887ad343d2'
)
INSERT INTO post_supports (post_id, support_count)
SELECT post_id, floor(random() * 15 + 20)  -- 20-35 supports per post
FROM priya_posts;

-- Add comments on Priya's posts
WITH priya_posts AS (
    SELECT post_id FROM community_posts 
    WHERE user_id = 'a321ac09-0528-4753-a380-57887ad343d2'
)
INSERT INTO comments (post_id, user_id, content, timestamp)
SELECT 
    p.post_id,
    (SELECT user_id FROM user_info WHERE user_id != 'a321ac09-0528-4753-a380-57887ad343d2' ORDER BY random() LIMIT 1),
    CASE random()::int % 3
        WHEN 0 THEN 'This is so inspiring! Keep going strong!'
        WHEN 1 THEN 'The breathing exercises helped me too. Great to see your progress!'
        ELSE 'Thank you for sharing your journey. We''re all in this together!'
    END,
    timestamp - interval '1 hour' * (random() * 24)::int
FROM priya_posts p;

-- Add Priya's progress data
INSERT INTO progress_data (user_id, week_number, completed_exercises, timestamp) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 8, true, '2025-07-24 09:30:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 7, true, '2025-07-17 14:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 6, true, '2025-07-10 16:45:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 5, true, '2025-07-03 11:20:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 4, true, '2025-06-26 10:15:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 3, true, '2025-06-19 13:30:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 2, true, '2025-06-12 15:00:00'),
('a321ac09-0528-4753-a380-57887ad343d2', 1, true, '2025-06-05 09:45:00');
