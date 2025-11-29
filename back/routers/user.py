"""this module handles user profile updates and retrieval using Supabase."""


# def update_premium_status(user: User):
#     """Automatically set premium if user is a distributor with active subscription."""
#     if user.role == "distributor" and user.subscription_active:
#         user.is_premium = True
#     else:
#         user.is_premium = False