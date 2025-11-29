# from sqlmodel import Field
# from typing import Optional, List
# from fastapi import HTTPException, status
# from fastapi import APIRouter, Depends
# from sqlmodel import Session, select
# from models import Review, ReviewCreate, User, Product

# router = APIRouter( prefix="/reviews", tags=["reviews"] )

# @router.post("/", response_model=Review)
# def create_review(data: ReviewCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
#     """Create a new review for a product."""
#     product = session.get(Product, data.product_id)
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#     review = Review(**data.dict(), user_id=user.id)
#     session.add(review)
#     session.commit()
#     session.refresh(review)
#     return review

# @router.get("/product/{product_id}", response_model=List[Review])
# def get_reviews_for_product(product_id: int, session: Session = Depends(get_session)):  

#     """Retrieve all reviews for a specific product."""
#     product = session.get(Product, product_id)
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#     reviews = session.exec(select(Review).where(Review.product_id == product_id)).all()
#     return reviews

# @router.put("/{review_id}", response_model=Review)
# def update_review(review_id: int, data: ReviewCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
#     """Update an existing review."""
#     review = session.get(Review, review_id)
#     if not review:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

#     if review.user_id != user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this review")

#     for key, value in data.model_dump().items():
#         setattr(review, key, value)

#     session.add(review)
#     session.commit()
#     session.refresh(review)
#     return review



# @router.delete("/{review_id}")
# def delete_review(review_id: int, user: User = Depends(get_current_user), session:  Session = Depends(get_session)):
#     """Delete a review."""
#     review = session.get(Review, review_id)
#     if not review:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

#     if review.user_id != user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this review")

#     session.delete(review)
#     session.commit()
#     return {"message": "Review deleted successfully"}

