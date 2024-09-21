import { supabase } from './db/supabaseClient';


const supabaseUrl = REACT_APP_SUPABASE_URL;  // Supabase project URL
const supabaseAnonKey = REACT_APP_SUPABASE_ANON_KEY;                 // Public API key from Supabase dashboard

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
