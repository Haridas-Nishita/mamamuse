-- Create post_supports table
CREATE TABLE IF NOT EXISTS post_supports (
    id SERIAL PRIMARY KEY,
    post_id TEXT REFERENCES community_posts(post_id),
    support_count INTEGER DEFAULT 0
);

-- Create comment_replies table
CREATE TABLE IF NOT EXISTS comment_replies (
    id SERIAL PRIMARY KEY,
    post_id TEXT REFERENCES community_posts(post_id),
    user_id UUID REFERENCES auth.users(id),
    content TEXT,
    timestamp TEXT
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_post_supports_post_id ON post_supports(post_id);
CREATE INDEX IF NOT EXISTS idx_comment_replies_post_id ON comment_replies(post_id);
CREATE INDEX IF NOT EXISTS idx_comment_replies_user_id ON comment_replies(user_id);

-- Insert some sample data for post supports
INSERT INTO post_supports (post_id, support_count)
SELECT post_id, 0
FROM community_posts
WHERE post_id NOT IN (SELECT post_id FROM post_supports);
