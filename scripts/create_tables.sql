-- Drop existing tables if they exist
DROP TABLE IF EXISTS comment_replies CASCADE;
DROP TABLE IF EXISTS post_supports CASCADE;
DROP TABLE IF EXISTS mood_log CASCADE;
DROP TABLE IF EXISTS community_posts CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS user_info CASCADE;

-- Create tables without auth dependencies and with TEXT ids
CREATE TABLE IF NOT EXISTS user_info (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER,
    week INTEGER
);

CREATE TABLE IF NOT EXISTS chats (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    timestamp TEXT,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

CREATE TABLE IF NOT EXISTS community_posts (
    id BIGSERIAL PRIMARY KEY,
    post_id TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

CREATE TABLE IF NOT EXISTS mood_log (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    mood_value INTEGER NOT NULL,
    timestamp TEXT,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

CREATE TABLE IF NOT EXISTS post_supports (
    id BIGSERIAL PRIMARY KEY,
    post_id TEXT NOT NULL,
    support_count INTEGER DEFAULT 0,
    FOREIGN KEY (post_id) REFERENCES community_posts(post_id)
);

CREATE TABLE IF NOT EXISTS comment_replies (
    id BIGSERIAL PRIMARY KEY,
    post_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT,
    FOREIGN KEY (post_id) REFERENCES community_posts(post_id),
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_info_user_id ON user_info(user_id);
CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id);
CREATE INDEX IF NOT EXISTS idx_community_posts_user_id ON community_posts(user_id);
CREATE INDEX IF NOT EXISTS idx_mood_log_user_id ON mood_log(user_id);
CREATE INDEX IF NOT EXISTS idx_post_supports_post_id ON post_supports(post_id);
CREATE INDEX IF NOT EXISTS idx_comment_replies_post_id ON comment_replies(post_id);
CREATE INDEX IF NOT EXISTS idx_comment_replies_user_id ON comment_replies(user_id);
