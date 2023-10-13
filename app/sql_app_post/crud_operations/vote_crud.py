from fastapi import HTTPException
from starlette import status

from app.sql_app_post import models


def create_vote(db, vote, user_id):
	qu = db.query(models.Post).filter(models.Post.post_id == vote.post_id).first()
	if not qu:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
	vote_query = db.query(models.Vote).filter(
		models.Vote.post_id == vote.post_id and models.Vote.user_id == user_id)
	print("vote_query", vote_query)
	found_vote = vote_query.first()
	if vote.vote_dir == 1:
		if found_vote:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted this post")
		new_vote = models.Vote(post_id=vote.post_id, user_id=user_id)
		db.add(new_vote)
		db.commit()
		db.refresh(new_vote)
		return {"message": "vote created successfully"}
	else:
		if not found_vote:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have not voted this post")
		vote_query.delete(synchronize_session=False)
		db.commit()
		return {"message": "vote deleted successfully"}
