import os
from dotenv import load_dotenv
from supabase import create_client
import time
import json

def execute_query(supabase, sql, max_retries=3):
    """Execute SQL with retry logic using proper Supabase methods"""
    for attempt in range(max_retries):
        try:
            # Use the rpc method for executing raw SQL
            result = supabase.rpc('execute_sql', {'query': sql}).execute()
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

        # First create the SQL function to execute raw SQL if it doesn't exist
        create_function_sql = """
        create or replace function execute_sql(query text)
        returns void
        language plpgsql
        security definer
        as $$
        begin
          execute query;
        end;
        $$;
        """
        
        print("\nCreating SQL execution function...")
        try:
            supabase.rpc('execute_sql', {'query': create_function_sql}).execute()
            print("SQL execution function created successfully ✅")
        except Exception as e:
            print(f"Error creating function (might already exist): {str(e)}")
        
        for i, statement in enumerate(statements, 1):
            print(f"\nExecuting statement {i}/{total_statements}...")
            print(f"Statement preview: {statement[:100]}...")
            
            if execute_query(supabase, statement):
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
                result = supabase.table(table).select("*", count='exact').execute()
                print(f"{table}: {len(result.data)} records")
            except Exception as e:
                print(f"{table}: Error - {str(e)}")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please verify your Supabase credentials and permissions.")

if __name__ == "__main__":
    main()
    print("\nPress Enter to exit...")
