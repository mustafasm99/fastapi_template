from fastapi import APIRouter
from .auth.login_route import router as login_router
from .auth.user_roll import router as user_rolls_router

router = APIRouter()


router.include_router(login_router , prefix="/auth" , tags=["auth"])
router.include_router(user_rolls_router , prefix="/roll" , tags=["roll"])