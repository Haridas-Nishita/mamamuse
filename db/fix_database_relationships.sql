-- Add foreign key relationship between community_posts and user_info
ALTER TABLE community_posts
ADD CONSTRAINT fk_community_posts_user
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
ON DELETE CASCADE;

-- Add foreign key relationship for comments
ALTER TABLE comments
ADD CONSTRAINT fk_comments_user
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
ON DELETE CASCADE;

-- Add foreign key relationship for post_supports
ALTER TABLE post_supports
ADD CONSTRAINT fk_post_supports_post
FOREIGN KEY (post_id) REFERENCES community_posts(post_id)
ON DELETE CASCADE;
