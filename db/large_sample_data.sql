-- Generate 200 chat entries (simulating daily interactions)
INSERT INTO chats (user_id, message, response, timestamp) 
WITH messages AS (
  SELECT unnest(ARRAY[
    'How are you feeling today?',
    'Can''t sleep well lately...',
    'Feeling anxious about work',
    'Had a tough therapy session',
    'Making progress with meditation',
    'Trying new coping strategies',
    'Feeling overwhelmed today',
    'Need some encouragement',
    'Started journaling today',
    'Having a good mental health day'
  ]) as message,
  unnest(ARRAY[
    'I understand. Let''s work through this together. What specific feelings are you experiencing?',
    'That sounds challenging. Have you tried any relaxation techniques before bed?',
    'Anxiety at work is common. Let''s break down what''s causing these feelings.',
    'It''s okay to feel emotional after therapy. Would you like to talk about it?',
    'That''s wonderful! How has meditation been helping you?',
    'Great initiative! Which strategies have been most effective for you?',
    'Let''s take it one step at a time. What''s the biggest concern right now?',
    'You''re doing better than you think. What small win can we celebrate today?',
    'Journaling is a great tool! How has it been helping you process thoughts?',
    'I''m glad you''re having a good day! What positive changes have you noticed?'
  ]) as response
)
SELECT 
  (SELECT user_id FROM user_info ORDER BY random() LIMIT 1),
  message,
  response,
  (TIMESTAMP '2025-07-24 00:00:00' - (random() * interval '60 days'))::text
FROM messages, generate_series(1, 20);
