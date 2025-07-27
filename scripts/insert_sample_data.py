import os
from dotenv import load_dotenv
from supabase import create_client
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
        
        # Sample user IDs (using fixed UUIDs for consistency)
        user_ids = [
            "a3298f6b-9890-4ef7-9b12-71a4e2432804",  # User 1
            "b4387c5d-8901-4de6-8a23-82b5e3543915",  # User 2
            "c5476d4e-7812-4cd5-7b34-93c6e4654a26"   # User 3
        ]
        
        # Insert users
        print("\nInserting users...")
        user_names = ["Sarah", "Michael", "Emma"]
        for i, (user_id, name) in enumerate(zip(user_ids, user_names)):
            try:
                data = {
                    "user_id": user_id,
                    "name": name,
                    "age": 25 + i,
                    "week": i + 1
                }
                supabase.table("user_info").insert(data).execute()
                print(f"Added user: {name}")
            except Exception as e:
                print(f"Error adding user {name}: {str(e)}")
        
        # Insert posts
        print("\nInserting community posts...")
        posts = [
            "Starting this journey feels both exciting and scary. Anyone else feeling the same?",
            "Had a breakthrough in therapy today! Remember, small progress is still progress! 💪",
            "Feeling down today. Could use some virtual hugs from this amazing community. 🫂",
            "Just wanted to say how grateful I am for this safe space. You all are amazing! 💝",
            "Learning to be kind to myself is hard but worth it. Keep going everyone!"
        ]
        
        for i, content in enumerate(posts):
            try:
                post_id = f"post{i+1}"
                data = {
                    "post_id": post_id,
                    "user_id": user_ids[i % len(user_ids)],
                    "content": content,
                    "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
                }
                supabase.table("community_posts").insert(data).execute()
                print(f"Added post: {post_id}")
                
                # Add support count
                support_data = {
                    "post_id": post_id,
                    "support_count": (i + 2) * 3  # Random-ish support counts
                }
                supabase.table("post_supports").insert(support_data).execute()
                print(f"Added support count for: {post_id}")
                
                # Add comments
                comments = [
                    "I totally understand how you feel! Stay strong! 💪",
                    "Thank you for sharing this. It really resonates with me.",
                    "We're all in this together! Keep going! 🌟"
                ]
                
                for j, comment_text in enumerate(comments[:2]):
                    comment_data = {
                        "post_id": post_id,
                        "user_id": user_ids[(i + j + 1) % len(user_ids)],
                        "content": comment_text,
                        "timestamp": (datetime.now() - timedelta(minutes=j*30)).isoformat()
                    }
                    supabase.table("comment_replies").insert(comment_data).execute()
                    print(f"Added comment {j+1} to post: {post_id}")
            except Exception as e:
                print(f"Error with post {i+1}: {str(e)}")
        
        # Insert chat messages
        print("\nInserting chat messages...")
        messages = [
            ("How are you feeling today?", "I'm feeling a bit anxious, but I'm trying to stay positive."),
            ("What coping strategies have you tried?", "Deep breathing has been really helpful for me."),
            ("Tell me about your day.", "It was challenging, but I managed to practice self-care."),
            ("What's on your mind?", "I'm worried about work, but talking helps."),
            ("How can I support you today?", "Just listening means a lot. Thank you.")
        ]
        
        for i, (msg, response) in enumerate(messages):
            try:
                data = {
                    "user_id": user_ids[i % len(user_ids)],
                    "message": msg,
                    "response": response,
                    "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
                }
                supabase.table("chats").insert(data).execute()
                print(f"Added chat message {i+1}")
            except Exception as e:
                print(f"Error adding chat {i+1}: {str(e)}")
        
        # Insert mood logs
        print("\nInserting mood logs...")
        for i in range(15):  # More mood logs for better tracking
            try:
                data = {
                    "user_id": user_ids[i % len(user_ids)],
                    "mood_value": ((i % 5) + 3) % 5 + 1,  # Values between 1-5
                    "timestamp": (datetime.now() - timedelta(days=i//3)).isoformat()
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
    print("\nDone! Press Enter to exit...")
