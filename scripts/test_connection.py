import os
from dotenv import load_dotenv
from supabase import create_client

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print("\nChecking Supabase credentials:")
    print(f"URL exists: {'Yes' if supabase_url else 'No'}")
    print(f"Key exists: {'Yes' if supabase_key else 'No'}")
    
    if not supabase_url or not supabase_key:
        print("\nError: Missing credentials in .env file!")
        print("Please ensure your .env file contains:")
        print("SUPABASE_URL=your_url_here")
        print("SUPABASE_KEY=your_key_here")
        return False
    
    try:
        print("\nAttempting to connect to Supabase...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Try a simple query to verify connection
        print("Testing query...")
        result = supabase.table('user_info').select("*").limit(1).execute()
        
        print("\nConnection successful! ✅")
        print(f"Found {len(result.data)} records in user_info table")
        return True
        
    except Exception as e:
        print("\n❌ Connection failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
