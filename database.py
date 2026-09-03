import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials not found. Check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_interview(user_id, job_role, interview_type, domain, score):
    try:
        response = supabase.table("interviews").insert({
            "user_id": user_id,
            "job_role": job_role,
            "interview_type": interview_type,
            "domain": domain,
            "score": score
        }).execute()
        return response
    except Exception as e:
        print("DATABASE ERROR:", e)
        raise


def get_user_interviews(user_id):
    try:
        response = (
            supabase
            .table("interviews")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data
    except Exception as e:
        print("DATABASE ERROR:", e)
        return []