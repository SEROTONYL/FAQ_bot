from .start import router as start_router
from .menu import router as menu_router
from .booking import router as booking_router
from .faq import router as faq_router
from .admin import router as admin_router

__all__ = [
    "start_router",
    "menu_router",
    "booking_router",
    "faq_router",
    "admin_router",
]
