import os
from dotenv import load_dotenv
from supabase import create_client
import time
from datetime import datetime, timedelta
import uuid

def main():
    # Load environment variables
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print("\nChecking configuration...")
    if not all([supabase_url, supabase_key]):
        print("Error: Missing credentials!")
        return
        
    try:
        print("Connecting to Supabase...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection
        test = supabase.table('user_info').select("*").limit(1).execute()
        print("Connection successful! ✅")
        
        # Create tables using native Supabase methods
        print("\nCreating tables...")
        
        tables = [
            ("user_info", [
                {"name": "id", "type": "bigint", "identity": True},
                {"name": "user_id", "type": "uuid"},
                {"name": "name", "type": "text"},
                {"name": "age", "type": "integer"},
                {"name": "week", "type": "integer"}
            ]),
            ("chats", [
                {"name": "id", "type": "bigint", "identity": True},
                {"name": "user_id", "type": "uuid"},
                {"name": "message", "type": "text"},
                {"name": "response", "type": "text"},
                {"name": "timestamp", "type": "text"}
            ]),
            ("community_posts", [
                {"name": "id", "type": "bigint", "identity": True},
                {"name": "post_id", "type": "text"},
                {"name": "user_id", "type": "uuid"},
                {"name": "content", "type": "text"},
                {"name": "timestamp", "type": "text"}
            ]),
            ("mood_log", [
                {"name": "id", "type": "bigint", "identity": True},
                {"name": "user_id", "type": "uuid"},
                {"name": "mood_value", "type": "integer"},
                {"name": "timestamp", "type": "text"}
            ]),
            ("post_supports", [
                {"name": "id", "type": "bigint", "identity": True},
                {"name": "post_id", "type": "text"},
                {"name": "support_count", "type": "integer"}
            ]),
            ("comment_replies", [
                {"name": "id", "type": "bigint", "identity": True},
                {"name": "post_id", "type": "text"},
                {"name": "user_id", "type": "uuid"},
                {"name": "content", "type": "text"},
                {"name": "timestamp", "type": "text"}
            ])
        ]
        
        for table_name, columns in tables:
            try:
                print(f"\nCreating table: {table_name}")
                response = supabase.table(table_name).select("*").limit(1).execute()
                print(f"Table {table_name} already exists ✓")
            except Exception as e:
                if "relation" in str(e) and "does not exist" in str(e):
                    print(f"Creating new table: {table_name}")
                    # Note: Table creation is handled through Supabase dashboard
                    # We'll just report that it needs to be created
                    print(f"Please create table {table_name} via Supabase dashboard with these columns:")
                    for col in columns:
                        print(f"  - {col['name']}: {col['type']}")
        
        # Insert sample data
        print("\nInserting sample data...")
        
        # Sample user IDs
        user_ids = [
            uuid.uuid4(),
            uuid.uuid4(),
            uuid.uuid4()
        ]
        
        # Insert users
        for i, user_id in enumerate(user_ids):
            try:
                data = {
                    "user_id": str(user_id),
                    "name": f"User {i+1}",
                    "age": 25 + i,
                    "week": i + 1
                }
                supabase.table("user_info").insert(data).execute()
                print(f"Added user: User {i+1}")
            except Exception as e:
                print(f"Error adding user {i+1}: {str(e)}")
        
        # Insert posts
        for i in range(5):
            try:
                post_id = f"post{i+1}"
                data = {
                    "post_id": post_id,
                    "user_id": str(user_ids[i % len(user_ids)]),
                    "content": f"This is a sample post {i+1}",
                    "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
                }
                supabase.table("community_posts").insert(data).execute()
                print(f"Added post: {post_id}")
                
                # Add support count
                support_data = {
                    "post_id": post_id,
                    "support_count": i + 1
                }
                supabase.table("post_supports").insert(support_data).execute()
                print(f"Added support count for: {post_id}")
                
                # Add comments
                for j in range(2):
                    comment_data = {
                        "post_id": post_id,
                        "user_id": str(user_ids[(i + j) % len(user_ids)]),
                        "content": f"Comment {j+1} on post {i+1}",
                        "timestamp": (datetime.now() - timedelta(minutes=j)).isoformat()
                    }
                    supabase.table("comment_replies").insert(comment_data).execute()
                    print(f"Added comment {j+1} to post: {post_id}")
            except Exception as e:
                print(f"Error with post {i+1}: {str(e)}")
        
        # Insert chat messages
        for i in range(5):
            try:
                data = {
                    "user_id": str(user_ids[i % len(user_ids)]),
                    "message": f"User message {i+1}",
                    "response": f"Bot response {i+1}",
                    "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
                }
                supabase.table("chats").insert(data).execute()
                print(f"Added chat message {i+1}")
            except Exception as e:
                print(f"Error adding chat {i+1}: {str(e)}")
        
        # Insert mood logs
        for i in range(5):
            try:
                data = {
                    "user_id": str(user_ids[i % len(user_ids)]),
                    "mood_value": (i % 5) + 1,
                    "timestamp": (datetime.now() - timedelta(days=i)).isoformat()
                }
                supabase.table("mood_log").insert(data).execute()
                print(f"Added mood log {i+1}")
            except Exception as e:
                print(f"Error adding mood log {i+1}: {str(e)}")
        
        print("\nVerifying data...")
        tables = ['user_info', 'chats', 'community_posts', 'mood_log', 'post_supports', 'comment_replies']
        for table in tables:
            try:
                result = supabase.table(table).select("*", count='exact').execute()
                print(f"{table}: {len(result.data)} records")
            except Exception as e:
                print(f"{table}: Error - {str(e)}")
                
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
