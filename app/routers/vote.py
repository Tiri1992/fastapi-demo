"""Handles the path operators /votes"""
from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
)
from .. import (
    schema,
    database,
    models,
    oauth2,
)
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Two checks:
    # Check1 -> Post that user wants to upvote exists (post_id)
    # Check2 -> Post that user wants to upvote hasn't already been upvoted by the current user.

    # First validate post exists
    post_exists = db.query(models.Post).filter(
        models.Post.id == vote.post_id).first()

    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                              vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already upvoted on post {vote.post_id}")
        # Checks complete, we build a record to persist the vote for current_user.id
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {
            "message": "successfully added vote."
        }
    else:
        if not found_vote:
            # The is no vote to delete
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist by user {current_user.id}")
        # Delete
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {
            "message": f"successfully deleted vote from post {vote.post_id}"
        }
