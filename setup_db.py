from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Create tables
def setup_database():
    # Create user_info table
    supabase.table("user_info").delete().execute()  # Clear existing data
    supabase.postgrest.rpc('create_table_if_not_exists', {
        'table_name': 'user_info',
        'definition': '''
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES auth.users(id),
            name TEXT,
            age INTEGER,
            week INTEGER
        '''
    }).execute()

    # Create chats table
    supabase.table("chats").delete().execute()
    supabase.postgrest.rpc('create_table_if_not_exists', {
        'table_name': 'chats',
        'definition': '''
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES auth.users(id),
            message TEXT,
            response TEXT,
            timestamp TEXT
        '''
    }).execute()

    # Create community_posts table
    supabase.table("community_posts").delete().execute()
    supabase.postgrest.rpc('create_table_if_not_exists', {
        'table_name': 'community_posts',
        'definition': '''
            id SERIAL PRIMARY KEY,
            post_id TEXT,
            user_id UUID REFERENCES auth.users(id),
            content TEXT,
            timestamp TEXT
        '''
    }).execute()

    # Create mood_log table
    supabase.table("mood_log").delete().execute()
    supabase.postgrest.rpc('create_table_if_not_exists', {
        'table_name': 'mood_log',
        'definition': '''
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES auth.users(id),
            mood_value INTEGER,
            timestamp TEXT
        '''
    }).execute()

# Insert sample data
def insert_sample_data():
    # Sample users (these UUIDs should match your actual test users in Supabase Auth)
    users = [
        {"user_id": "uuid1", "name": "Priya Sharma", "age": 28, "week": 12},
        {"user_id": "uuid2", "name": "Sofia Lopez", "age": 32, "week": 18},
        {"user_id": "uuid3", "name": "Anonymous", "age": 25, "week": 20},
        {"user_id": "uuid4", "name": "Aisha Khan", "age": 30, "week": 14},
        {"user_id": "uuid5", "name": "Maria Garcia", "age": 27, "week": 22},
    ]
    
    supabase.table("user_info").insert(users).execute()

    # Sample chats
    chats = [
        {"user_id": "uuid1", "message": "I'm feeling anxious about my upcoming scan", "response": "It's completely normal to feel anxious. Remember to breathe deeply and focus on the excitement of seeing your little one! Would you like to talk more about what's specifically worrying you? 🌸", "timestamp": "2025-07-24T10:00:00"},
        {"user_id": "uuid2", "message": "¿Qué alimentos debo evitar durante el embarazo?", "response": "Es importante evitar: pescados con alto contenido de mercurio, carnes crudas, huevos crudos, quesos sin pasteurizar. ¿Te gustaría una lista más detallada de alimentos seguros? 🥗", "timestamp": "2025-07-24T11:00:00"},
        {"user_id": "uuid3", "message": "मुझे गर्भावस्था में मतली हो रही है", "response": "सुबह की मतली सामान्य है। अदरक की चाय पीने से राहत मिल सकती है। क्या आप अपनी दिनचर्या के बारे में बात करना चाहेंगी? 🫖", "timestamp": "2025-07-24T12:00:00"}
    ]
    
    supabase.table("chats").insert(chats).execute()

    # Sample community posts
    posts = [
        {"post_id": "post1", "user_id": "uuid1", "content": "What's your favorite pregnancy snack? Mine is yogurt with honey! 🍯", "timestamp": "2025-07-24T09:00:00"},
        {"post_id": "post2", "user_id": "uuid2", "content": "Just felt my baby kick for the first time! Such an amazing feeling 💕", "timestamp": "2025-07-24T10:30:00"},
        {"post_id": "post3", "user_id": "uuid3", "content": "Any tips for sleeping better during the third trimester?", "timestamp": "2025-07-24T11:45:00"}
    ]
    
    supabase.table("community_posts").insert(posts).execute()

    # Sample mood logs
    moods = [
        {"user_id": "uuid1", "mood_value": 8, "timestamp": "2025-07-24T08:00:00"},
        {"user_id": "uuid1", "mood_value": 7, "timestamp": "2025-07-24T14:00:00"},
        {"user_id": "uuid2", "mood_value": 9, "timestamp": "2025-07-24T09:00:00"},
        {"user_id": "uuid3", "mood_value": 6, "timestamp": "2025-07-24T10:00:00"}
    ]
    
    supabase.table("mood_log").insert(moods).execute()

if __name__ == "__main__":
    print("Setting up database...")
    setup_database()
    print("Inserting sample data...")
    insert_sample_data()
    print("Database setup complete!")
