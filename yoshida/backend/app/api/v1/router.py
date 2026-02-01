from fastapi import APIRouter
from .endpoints.eligibility import router as eligibility_router

router = APIRouter()
router.include_router(eligibility_router, tags=["eligibility"])
