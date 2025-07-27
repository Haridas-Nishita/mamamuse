-- Function to get community posts with all required metadata
CREATE OR REPLACE FUNCTION get_community_posts_with_metadata(
    limit_count INTEGER DEFAULT 10,
    offset_count INTEGER DEFAULT 0
)
RETURNS TABLE (
    post_id UUID,
    user_id UUID,
    content TEXT,
    timestamp TIMESTAMPTZ,
    user_info JSONB,
    post_supports JSONB[],
    comments JSONB[]
) AS $$
BEGIN
    RETURN QUERY
    WITH post_data AS (
        SELECT 
            p.post_id,
            p.user_id,
            p.content,
            p.timestamp,
            jsonb_build_object(
                'name', u.name,
                'week', u.week
            ) as user_info,
            (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'support_count', COALESCE(ps.support_count, 0)
                    )
                )
                FROM post_supports ps
                WHERE ps.post_id = p.post_id
            ) as post_supports,
            (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'comment_id', c.comment_id,
                        'user_id', c.user_id,
                        'content', c.content,
                        'timestamp', c.timestamp,
                        'user_info', jsonb_build_object(
                            'name', cu.name
                        )
                    )
                    ORDER BY c.timestamp ASC
                )
                FROM comments c
                LEFT JOIN user_info cu ON c.user_id = cu.user_id
                WHERE c.post_id = p.post_id
            ) as comments
        FROM 
            community_posts p
            LEFT JOIN user_info u ON p.user_id = u.user_id
        ORDER BY 
            p.timestamp DESC
        LIMIT 
            limit_count
        OFFSET 
            offset_count
    )
    SELECT 
        pd.post_id,
        pd.user_id,
        pd.content,
        pd.timestamp,
        pd.user_info,
        COALESCE(pd.post_supports, ARRAY[NULL]::jsonb[]) as post_supports,
        COALESCE(pd.comments, ARRAY[]::jsonb[]) as comments
    FROM 
        post_data pd;
END;
$$ LANGUAGE plpgsql;
