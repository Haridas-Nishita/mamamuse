-- Generate post supports (ensuring each post has engagement)
INSERT INTO post_supports (post_id, support_count)
SELECT 
  post_id,
  floor(random() * 30 + 5)::integer  -- Random number between 5 and 35 supports
FROM community_posts;
