-- First, ensure we have the basic tables
CREATE TABLE IF NOT EXISTS public.user_info (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    name TEXT,
    age INTEGER,
    week INTEGER
);

CREATE TABLE IF NOT EXISTS public.chats (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    message TEXT,
    response TEXT,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS public.community_posts (
    id SERIAL PRIMARY KEY,
    post_id TEXT,
    user_id UUID REFERENCES auth.users(id),
    content TEXT,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS public.mood_log (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    mood_value INTEGER,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS public.post_supports (
    id SERIAL PRIMARY KEY,
    post_id TEXT REFERENCES community_posts(post_id),
    support_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.comment_replies (
    id SERIAL PRIMARY KEY,
    post_id TEXT REFERENCES community_posts(post_id),
    user_id UUID REFERENCES auth.users(id),
    content TEXT,
    timestamp TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_info_user_id ON user_info(user_id);
CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id);
CREATE INDEX IF NOT EXISTS idx_community_posts_user_id ON community_posts(user_id);
CREATE INDEX IF NOT EXISTS idx_mood_log_user_id ON mood_log(user_id);
CREATE INDEX IF NOT EXISTS idx_post_supports_post_id ON post_supports(post_id);
CREATE INDEX IF NOT EXISTS idx_comment_replies_post_id ON comment_replies(post_id);
CREATE INDEX IF NOT EXISTS idx_comment_replies_user_id ON comment_replies(user_id);

-- Insert sample users if they don't exist
INSERT INTO public.user_info (user_id, name, age, week) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 'Priya Sharma', 28, 12),
('a1cc2f47-9844-40d2-b62a-4f1172f438fa', 'Sofia Lopez', 32, 18),
('0c42b386-243b-44f8-afac-596099c31a1e', 'Anonymous', 25, 20),
('ebcbcefe-e854-4748-bf1c-2ef00776dc86', 'Aisha Khan', 30, 14),
('5865b3ef-d056-44d6-8776-c332f0f486a8', 'Maria Garcia', 27, 22)
ON CONFLICT (id) DO NOTHING;

-- Insert sample chats
INSERT INTO public.chats (user_id, message, response, timestamp) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 'Feeling anxious about my upcoming scan', 'I understand your anxiety about the scan. Remember that these checkups are routine and help ensure both you and your baby are doing well. Would you like to talk more about what specifically worries you? 💕', '2025-07-24T10:00:00Z'),
('a1cc2f47-9844-40d2-b62a-4f1172f438fa', 'Having trouble sleeping lately', 'Sleep challenges are very common during pregnancy. Have you tried using a pregnancy pillow? Also, maintaining a consistent bedtime routine can help. Would you like some specific relaxation techniques? 🌙', '2025-07-24T11:00:00Z'),
('0c42b386-243b-44f8-afac-596099c31a1e', 'Need advice about morning sickness', 'Morning sickness can be really challenging. Some moms find relief with ginger tea or small, frequent meals. The Mayo Clinic has some great tips: [link]. How severe are your symptoms? 🫖', '2025-07-24T12:00:00Z')
ON CONFLICT (id) DO NOTHING;

-- Insert sample posts
INSERT INTO public.community_posts (post_id, user_id, content, timestamp) VALUES
('post1', 'a321ac09-0528-4753-a380-57887ad343d2', 'Anyone else experiencing crazy food cravings? 😅', '2025-07-24T09:00:00Z'),
('post2', 'a1cc2f47-9844-40d2-b62a-4f1172f438fa', 'Just felt my baby kick for the first time! 💖', '2025-07-24T10:00:00Z'),
('post3', '0c42b386-243b-44f8-afac-596099c31a1e', 'Any recommendations for pregnancy-safe exercises?', '2025-07-24T11:00:00Z')
ON CONFLICT (id) DO NOTHING;

-- Insert sample mood logs
INSERT INTO public.mood_log (user_id, mood_value, timestamp) VALUES
('a321ac09-0528-4753-a380-57887ad343d2', 8, '2025-07-24T09:00:00Z'),
('a1cc2f47-9844-40d2-b62a-4f1172f438fa', 7, '2025-07-24T10:00:00Z'),
('0c42b386-243b-44f8-afac-596099c31a1e', 9, '2025-07-24T11:00:00Z')
ON CONFLICT (id) DO NOTHING;

-- Insert post supports
INSERT INTO public.post_supports (post_id, support_count) VALUES
('post1', 5),
('post2', 8),
('post3', 3)
ON CONFLICT (id) DO NOTHING;

-- Insert sample comments
INSERT INTO public.comment_replies (post_id, user_id, content, timestamp) VALUES
('post1', 'a1cc2f47-9844-40d2-b62a-4f1172f438fa', 'Yes! I've been craving pickles with ice cream! 😋', '2025-07-24T09:30:00Z'),
('post2', 'a321ac09-0528-4753-a380-57887ad343d2', 'Such a magical moment! ✨', '2025-07-24T10:30:00Z'),
('post3', '5865b3ef-d056-44d6-8776-c332f0f486a8', 'Prenatal yoga has been amazing for me! 🧘‍♀️', '2025-07-24T11:30:00Z')
ON CONFLICT (id) DO NOTHING;

-- Generate more sample data programmatically
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1
    FROM numbers
    WHERE n < 30
)
INSERT INTO public.community_posts (post_id, user_id, content, timestamp)
SELECT 
    'post' || (n + 10)::text,
    (ARRAY['a321ac09-0528-4753-a380-57887ad343d2', 'a1cc2f47-9844-40d2-b62a-4f1172f438fa', '0c42b386-243b-44f8-afac-596099c31a1e'])[1 + mod(n, 3)]::uuid,
    CASE mod(n, 5)
        WHEN 0 THEN 'Anyone have tips for dealing with pregnancy fatigue? 😴'
        WHEN 1 THEN 'Started decorating the nursery today! 🎨'
        WHEN 2 THEN 'What prenatal vitamins are you taking? 💊'
        WHEN 3 THEN 'Had my checkup today - baby is growing perfectly! 🌱'
        ELSE 'Looking for recommendations for pregnancy books 📚'
    END,
    (NOW() - (n || ' hours')::interval)::text
FROM numbers
ON CONFLICT DO NOTHING;
