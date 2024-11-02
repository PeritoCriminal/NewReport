# newreportapp.views.__init__.py
from .home_views import home_views
from .user_register_views import register_user
from .index_views import index
from .user_login_views import user_login_view
from .edit_user_profile_views import edit_user_profile_view
from .create_post_views import create_post_view
from .post_likes_views import post_like
from .post_delete_views import post_delete_views
from .decorators import administrator_required, login_forbidden
from .change_password_views import change_password_view
from .comment_post_views import comment_post_view
