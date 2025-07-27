import os
from supabase import create_client
from dotenv import load_dotenv

def execute_sql(supabase, sql):
    try:
        result = supabase.raw(sql)
        print("SQL executed successfully!")
        return result
    except Exception as e:
        print(f"Error executing SQL: {str(e)}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Initialize Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Create post_supports table
    create_post_supports = """
    CREATE TABLE IF NOT EXISTS post_supports (
        id SERIAL PRIMARY KEY,
        post_id TEXT REFERENCES community_posts(post_id),
        support_count INTEGER DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_post_supports_post_id ON post_supports(post_id);
    """
    
    # Create comment_replies table
    create_comment_replies = """
    CREATE TABLE IF NOT EXISTS comment_replies (
        id SERIAL PRIMARY KEY,
        post_id TEXT REFERENCES community_posts(post_id),
        user_id UUID REFERENCES auth.users(id),
        content TEXT,
        timestamp TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_comment_replies_post_id ON comment_replies(post_id);
    CREATE INDEX IF NOT EXISTS idx_comment_replies_user_id ON comment_replies(user_id);
    """
    
    # Execute table creation
    execute_sql(supabase, create_post_supports)
    execute_sql(supabase, create_comment_replies)
    
    # Insert sample post supports
    insert_supports = """
    INSERT INTO post_supports (post_id, support_count)
    SELECT p.post_id, FLOOR(RANDOM() * 50)
    FROM community_posts p
    WHERE NOT EXISTS (
        SELECT 1 FROM post_supports ps WHERE ps.post_id = p.post_id
    );
    """
    execute_sql(supabase, insert_supports)
    
    # Insert sample comments
    comments_data = [
        ("Sending you positive vibes! 💖", "Have you tried meditation? It helped me a lot!"),
        ("Thanks for sharing! I had the same experience.", "Here's what worked for me: regular exercise and rest"),
        ("Stay strong mama! You're doing great!", "My doctor recommended prenatal yoga for this"),
        ("This is so relatable!", "I found that ginger tea really helps with morning sickness"),
        ("You're not alone in this! 🌸", "Consider joining a local pregnancy support group"),
        ("This phase will pass! 💝", "Regular walks helped me manage this"),
        ("Totally understand what you're going through!", "Deep breathing exercises were a game-changer for me"),
        ("Thank you for being so open!", "Have you tried the pregnancy pillow? It's amazing!"),
        ("We're all here for you! ✨", "Talking to a doula really helped me with this"),
        ("Such an important topic!", "Regular checkups and communication with your doctor are key")
    ]
    
    for content_pair in comments_data:
        insert_comments = f"""
        INSERT INTO comment_replies (post_id, user_id, content, timestamp)
        SELECT 
            p.post_id,
            u.user_id,
            CASE WHEN RANDOM() < 0.5 THEN '{content_pair[0]}' ELSE '{content_pair[1]}' END,
            NOW() - (RANDOM() * INTERVAL '30 days')
        FROM 
            community_posts p
            CROSS JOIN (
                SELECT user_id FROM user_info ORDER BY RANDOM() LIMIT 1
            ) u
        WHERE NOT EXISTS (
            SELECT 1 FROM comment_replies cr 
            WHERE cr.post_id = p.post_id AND cr.content IN ('{content_pair[0]}', '{content_pair[1]}')
        )
        ORDER BY RANDOM()
        LIMIT 5;
        """
        execute_sql(supabase, insert_comments)

if __name__ == "__main__":
    main()
