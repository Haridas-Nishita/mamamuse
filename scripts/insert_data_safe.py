import os
from dotenv import load_dotenv
from supabase import create_client
import time

def execute_with_retry(supabase, sql, max_retries=3):
    """Execute SQL with retry logic"""
    for attempt in range(max_retries):
        try:
            result = supabase.raw(sql)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Max retries reached!")
                return False

def main():
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print("\nChecking configuration:")
    print(f"URL exists: {'Yes' if supabase_url else 'No'}")
    print(f"Key exists: {'Yes' if supabase_key else 'No'}")
    
    if not supabase_url or not supabase_key:
        print("\nError: Missing credentials in .env file!")
        print("Please ensure your .env file contains:")
        print("SUPABASE_URL=your_url_here")
        print("SUPABASE_KEY=your_key_here")
        return
    
    try:
        print("\nConnecting to Supabase...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection
        print("Testing connection...")
        test = supabase.table('user_info').select("*").limit(1).execute()
        print("Connection successful! ✅")
        
        print("\nReading SQL file...")
        with open('scripts/insert_data.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split SQL into individual statements
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        total_statements = len(statements)
        
        print(f"\nExecuting {total_statements} SQL statements...")
        success_count = 0
        
        for i, statement in enumerate(statements, 1):
            print(f"\nExecuting statement {i}/{total_statements}...")
            print(f"Statement preview: {statement[:100]}...")
            
            if execute_with_retry(supabase, statement):
                success_count += 1
                print(f"Statement {i} executed successfully ✅")
            else:
                print(f"Statement {i} failed ❌")
        
        print(f"\nExecution complete!")
        print(f"Successful statements: {success_count}/{total_statements}")
        
        # Verify data insertion
        print("\nVerifying data insertion...")
        tables = ['user_info', 'chats', 'community_posts', 'mood_log', 'post_supports', 'comment_replies']
        for table in tables:
            try:
                count = supabase.table(table).select("*", count='exact').execute()
                print(f"{table}: {len(count.data)} records")
            except Exception as e:
                print(f"{table}: Error - {str(e)}")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please verify your Supabase credentials and permissions.")

if __name__ == "__main__":
    main()
    print("\nPress Enter to exit...")
