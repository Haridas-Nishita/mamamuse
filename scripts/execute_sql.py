import os
from dotenv import load_dotenv
from supabase import create_client

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase client
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return
    
    supabase = create_client(supabase_url, supabase_key)
    
    print("Reading SQL file...")
    with open('scripts/insert_data.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Split SQL into individual statements
    statements = sql.split(';')
    
    print("Executing SQL statements...")
    for statement in statements:
        if statement.strip():
            try:
                print(f"\nExecuting: {statement[:100]}...")  # Print first 100 chars of statement
                result = supabase.raw(statement)
                print("Success!")
            except Exception as e:
                print(f"Error executing statement: {str(e)}")
    
    print("\nData insertion complete!")

if __name__ == "__main__":
    main()
