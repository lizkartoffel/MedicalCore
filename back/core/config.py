# SUPABASE_URL = "https://brvvwfdmpvknipogjbfh.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJydnZ3ZmRtcHZrbmlwb2dqYmZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2MDEzMzUsImV4cCI6MjA3NTE3NzMzNX0.NujQxI8iL2enHSGSPEwsqZru9XgrGKz19y1Usdcl3qo"
# back/core/config.py
import os
import secrets

# -----------------------
# SECURITY CONFIG
# -----------------------

# Use environment variable if available, otherwise generate a secure fallback
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

# JWT algorithm
ALGORITHM = "HS256"

# Token expiry duration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # you can change this if needed
