-- Insert sample chats
INSERT INTO chats (user_id, message, response, timestamp) VALUES
    ('a321ac09-0528-4753-a380-57887ad343d2', 'How are you feeling today?', 'I''m feeling a bit anxious, but I''m trying to stay positive.', '2025-07-24T10:00:00'),
    ('a1cc2f47-9844-40d2-b62a-4f1172f438fa', 'What coping strategies have you tried?', 'Deep breathing has been really helpful for me.', '2025-07-24T11:00:00'),
    ('e9b42583-9216-405d-a96f-70c31357f5c4', 'Tell me about your day.', 'It was challenging, but I managed to practice self-care.', '2025-07-24T12:00:00');

-- Insert sample community posts
INSERT INTO community_posts (post_id, user_id, content, timestamp) VALUES
    ('post1', 'a321ac09-0528-4753-a380-57887ad343d2', 'Starting this journey feels both exciting and scary. Anyone else feeling the same?', '2025-07-24T09:00:00'),
    ('post2', '750b15d5-b4fc-44e8-9717-cab6a428b957', 'Had a breakthrough in therapy today! Remember, small progress is still progress! 💪', '2025-07-24T10:30:00'),
    ('post3', 'e9bb84c4-87fa-4959-9c99-524a8aff0c64', 'Feeling down today. Could use some virtual hugs from this amazing community. 🫂', '2025-07-24T11:45:00'),
    ('post4', '8f0c35cb-927e-4aec-82f1-f7cb4f80ff42', 'Just wanted to say how grateful I am for this safe space. You all are amazing! 💝', '2025-07-24T13:15:00'),
    ('post5', '4f5ca5b0-a4bb-4dda-ba7f-016876d83ea7', 'Learning to be kind to myself is hard but worth it. Keep going everyone!', '2025-07-24T14:30:00');

-- Insert post support counts
INSERT INTO post_supports (post_id, support_count) VALUES
    ('post1', 15),
    ('post2', 12),
    ('post3', 18),
    ('post4', 9),
    ('post5', 6);

-- Insert sample comments
INSERT INTO comment_replies (post_id, user_id, content, timestamp) VALUES
    ('post1', 'c8fa9e65-377a-40c1-a304-79fe0d9b50e7', 'I totally understand how you feel! Stay strong! 💪', '2025-07-24T09:15:00'),
    ('post1', '58ef6ccc-2609-442b-b731-cf3f42ce058f', 'We''re all in this together! Keep going! 🌟', '2025-07-24T09:30:00'),
    ('post2', '8fe4edbb-fb6c-4ab4-86dd-7b6bb2855a0c', 'So proud of you! Every step counts! 🎉', '2025-07-24T10:45:00'),
    ('post2', 'ebcbcefe-e854-4748-bf1c-2ef00776dc86', 'This is inspiring! Thank you for sharing! 💝', '2025-07-24T11:00:00'),
    ('post3', '76c5d126-f096-43b2-943a-93902d8711e0', 'Sending you virtual hugs! Remember, tomorrow is a new day! 🤗', '2025-07-24T12:00:00'),
    ('post3', '3c8beac9-8b51-4296-a67f-a1100a3a1ebf', 'Here whenever you need support! 💕', '2025-07-24T12:15:00'),
    ('post4', '5865b3ef-d056-44d6-8776-c332f0f486a8', 'We''re grateful for you too! 💖', '2025-07-24T13:30:00'),
    ('post4', '0c42b386-243b-44f8-afac-596099c31a1e', 'This community is amazing because of people like you! ✨', '2025-07-24T13:45:00'),
    ('post5', 'a321ac09-0528-4753-a380-57887ad343d2', 'Self-compassion is a journey. You''re doing great! 🌱', '2025-07-24T14:45:00'),
    ('post5', 'e9b42583-9216-405d-a96f-70c31357f5c4', 'Such an important reminder. Thank you! 💫', '2025-07-24T15:00:00');

-- Insert mood logs
INSERT INTO mood_log (user_id, mood_value, timestamp) VALUES
    ('a321ac09-0528-4753-a380-57887ad343d2', 4, '2025-07-24T08:00:00'),
    ('a321ac09-0528-4753-a380-57887ad343d2', 3, '2025-07-23T08:00:00'),
    ('a321ac09-0528-4753-a380-57887ad343d2', 5, '2025-07-22T08:00:00'),
    ('8f0c35cb-927e-4aec-82f1-f7cb4f80ff42', 3, '2025-07-24T09:00:00'),
    ('8f0c35cb-927e-4aec-82f1-f7cb4f80ff42', 4, '2025-07-23T09:00:00'),
    ('8f0c35cb-927e-4aec-82f1-f7cb4f80ff42', 4, '2025-07-22T09:00:00'),
    ('4f5ca5b0-a4bb-4dda-ba7f-016876d83ea7', 2, '2025-07-24T10:00:00'),
    ('4f5ca5b0-a4bb-4dda-ba7f-016876d83ea7', 3, '2025-07-23T10:00:00'),
    ('4f5ca5b0-a4bb-4dda-ba7f-016876d83ea7', 4, '2025-07-22T10:00:00');
