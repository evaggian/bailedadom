import { supabase } from './supabaseClient';

// Function to set up the database tables
export async function setupTables() {
  // Define the SQL statement to create the 'registrations' table
  const createRegistrationsTable = `
    CREATE TABLE IF NOT EXISTS registrations (
      id serial PRIMARY KEY,
      user_id uuid REFERENCES auth.users (id) ON DELETE CASCADE,  -- Assuming you use Supabase Auth
      selected_blocks text[]  -- Array to store multiple selected blocks
    );
  `;

  // Execute the SQL command
  const { error } = await supabase.rpc('pg_execute_sql', {
    sql: createRegistrationsTable,
  });

  if (error) {
    console.error('Error creating tables:', error);
  } else {
    console.log('Tables created successfully');
  }
}
