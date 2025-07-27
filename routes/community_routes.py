from flask import Blueprint, session, redirect, url_for, render_template, flash
from datetime import datetime
from config import supabase

bp = Blueprint('community', __name__)

community_bp = Blueprint('community', __name__)

@community_bp.route('/community')
def community():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    try:
        # Get user info first
        user_info = supabase.table("user_info").select("*").eq("user_id", session["user_id"]).execute()
        if not user_info.data:
            return redirect(url_for("first_login"))

        # Get community posts with user information using a join query
        posts = supabase.table("community_posts")\
            .select("*, user_info(name)")\
            .order("timestamp", desc=True)\
            .execute()

        # Get post supports
        supports = supabase.table("post_supports").select("*").execute()
        supports_dict = {s["post_id"]: s["support_count"] for s in supports.data}

        # Get comments with user information
        comments = supabase.table("comments")\
            .select("*, user_info(name)")\
            .order("timestamp", asc=True)\
            .execute()
        
        comments_by_post = {}
        for comment in comments.data:
            post_id = comment["post_id"]
            if post_id not in comments_by_post:
                comments_by_post[post_id] = []
            comments_by_post[post_id].append(comment)

        return render_template(
            "community.html",
            posts=posts.data,
            supports=supports_dict,
            comments=comments_by_post,
            current_user_id=session["user_id"]
        )
    
    except Exception as e:
        print(f"Error loading community page: {str(e)}")
        flash("Unable to load community posts at this time. Please try again later.", "error")
        return redirect(url_for("home"))
