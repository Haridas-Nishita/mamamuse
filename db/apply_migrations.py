import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

def read_sql_file(file_path):
    """Read SQL file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def apply_migrations():
    """Apply database migrations."""
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase client
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        sys.exit(1)
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Get all migration files
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_dir):
        print(f"No migrations directory found at {migrations_dir}")
        return
    
    migration_files = sorted([f for f in os.listdir(migrations_dir) 
                            if f.endswith('.sql')])
    
    if not migration_files:
        print("No migration files found.")
        return
    
    # Create migrations table if it doesn't exist
    try:
        supabase.rpc('create_migrations_table').execute()
    except Exception as e:
        # Table might already exist, which is fine
        pass
    
    # Apply each migration
    for migration_file in migration_files:
        migration_name = os.path.splitext(migration_file)[0]
        
        # Check if migration was already applied
        result = supabase.table('applied_migrations')\
            .select('*')\
            .eq('name', migration_name)\
            .execute()
        
        if result.data and len(result.data) > 0:
            print(f"Skipping already applied migration: {migration_name}")
            continue
        
        # Read and execute the migration
        print(f"Applying migration: {migration_name}")
        migration_path = os.path.join(migrations_dir, migration_file)
        sql = read_sql_file(migration_path)
        
        try:
            # Split SQL into individual statements and execute them
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for statement in statements:
                if statement:  # Skip empty statements
                    supabase.rpc('execute_sql', {'query': statement}).execute()
            
            # Record the migration
            supabase.table('applied_migrations').insert({
                'name': migration_name,
                'applied_at': 'now()'
            }).execute()
            
            print(f"Successfully applied migration: {migration_name}")
            
        except Exception as e:
            print(f"Error applying migration {migration_name}: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    apply_migrations()
