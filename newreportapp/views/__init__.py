# newreportapp.views.__init__.py

from newreportapp.views.home_views import home_views
from newreportapp.views.user.user_register_views import register_user, verify_email, send_verification_email
from newreportapp.views.index_views import index
from newreportapp.views.user.user_login_views import user_login_view
from newreportapp.views.user.edit_user_profile_views import edit_user_profile_view
from newreportapp.views.posts.create_post_views import create_post_view
from newreportapp.views.posts.post_and_comments_likes_views import like_post, like_comment
from newreportapp.views.posts.post_delete_views import post_delete_views, restore_post
from newreportapp.views.decorators import administrator_required, login_forbidden
from newreportapp.views.user.change_password_views import change_password_view
from newreportapp.views.posts.comment_post_views import comment_post_view, delete_comment_view
from newreportapp.views.posts.inapropriate_post_views import mark_post_inappropriate
from newreportapp.views.posts.prohibited_post_views import mark_post_prohibited
from .report.header_report_views import header_report_view
from .user.user_attributes_to_report_views import user_attributes_to_report_view
# from .report.partial_section_report_views import section_report_view
from .report.list_report_views import list_reports
from .report.delete_report_views import delete_report
from .report.show_report_views import show_report
from .report.local_preservation_report_views import local_preservation_report_view
from .report.local_description_report_views import local_description_report_view
from .report.image_report_views import save_image_report
from .report.delete_image_views import delete_image_view
from .report.clues_and_traces_views import clues_and_traces_view
from .report.collected_items_views import collected_items_view
from .report.veicles_views import veicles_view
from .report.perinecroscopic_views import perinecroscopic_view
from .report.fingerprints_views import fingerprints_view
from .report.conclusion_views import conclusion_view
from .report.considerations_views import considerations_view
from .report.for_analysis_views import for_analysis_view
# from .report.load_image_data_views import load_image_data
