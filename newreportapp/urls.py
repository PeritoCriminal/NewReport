from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (change_password_view, 
                    edit_user_profile_view, 
                    like_comment, like_post, 
                    register_user, post_delete_views, 
                    user_login_view, home_views, 
                    create_post_view, comment_post_view, 
                    delete_comment_view,
                    mark_post_inappropriate,
                    mark_post_prohibited,
                    restore_post,
                    header_report_view,
                    user_attributes_to_report_view,
                    index,
                    list_reports,
                    delete_report,
                    show_report,
                    local_preservation_report_view,
                    local_description_report_view,
                    clues_and_traces_view,
                    collected_items_view,
                    veicles_view,
                    perinecroscopic_view,
                    fingerprints_view,
                    conclusion_view,
                    considerations_view,
                    save_image_report,
                    delete_image_view,
                    # load_image_data,
                    verify_email,
                    )

urlpatterns = [
    # URLs de redefinição de senha com templates personalizados
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), 
        name='password_reset'
    ),
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
        name='password_reset_complete'
    ),
    #path('password_change/', change_password_view, name='password_change'),  # Usando a view personalizada
    path('account/password_change/', change_password_view, name='password_change'),
    # URLs relacionadas à conta do usuário
    path('account/register/', register_user, name='register'),
    path('account/login/', user_login_view, name='login'),
    path('', home_views, name='home'),
    path('index', index, name='index'),
    
    # path('post/<int:post_id>/like/', post_and_comments_likes_views.post_like, name='post_like'),
    path('post/<int:post_id>/delete/', post_delete_views, name='post_delete'),  # Rota para deletar
    path('post/<int:post_id>/restore/', restore_post, name='restore_post'),

    
    path('comment/<int:comment_id>/delete/', delete_comment_view, name='delete_comment'),

    # path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    # path('msg_to_newcomer')

    path('account/edit_user_profile/', edit_user_profile_view, name='edit_user_profile'),
    path('user-attributes/new/', user_attributes_to_report_view, name='user_attributes_create'),
    path('user-attributes/edit/<int:pk>/', user_attributes_to_report_view, name='user_attributes_edit'),

    path('create_post', create_post_view, name='create_post'),
    path('create_post/<int:post_id>/', create_post_view, name='create_post'),
    path('post/<int:post_id>/comment/', comment_post_view, name='comment_post_view'),
    path('post/<int:post_id>/mark_inappropriate/', mark_post_inappropriate, name='mark_post_inappropriate'),
    path('post/<int:post_id>/mark_prohibited/', mark_post_prohibited, name='mark_post_prohibited'),

    # REPORTS
    path('report/header-report/', header_report_view, name='create_header_report'),
    path('report/header-report/<int:report_id>/', header_report_view, name='edit_header_report'),
    path('report/list_report/', list_reports, name='list_reports'),
    path('report/show_report/<int:pk>/', show_report, name='show_report'),
    path('delete-report/<int:report_id>/', delete_report, name='delete_report'),
    path('save_image_report/', save_image_report, name='save_image_report'),
    path('delete-image/<int:pk>/', delete_image_view, name='delete_image'),
    # path('load-image-data/', load_image_data, name='load_image_data'),

    # path('report/image_report/<int:section_pk>', image_report_view, name='add_image_report'),
    # path('report/<int:section_pk>/image/<int:pk>/edit/', image_report_view, name='edit_image_report'),


    # Rotas novas para os relatórios
    path('report/preservation_report/<int:header_report_id>/', local_preservation_report_view, name='create_preservation_report'),
    path('report/description_report/<int:header_report_id>/', local_description_report_view, name='create_description_report'),
    path('report/clues_and_traces_report/<int:header_report_id>/', clues_and_traces_view, name='create_clues_and_traces_report'),
    path('report/collected_items_report/<int:header_report_id>/', collected_items_view, name='create_collected_items_report'),
    path('report/perinecroscopc_report/<int:header_report_id>/', perinecroscopic_view, name='create_perinecroscopic_report'),
    path('report/veicles_report/<int:header_report_id>/', veicles_view, name='create_veicles_report'),
    path('report/fingerprint_report/<int:header_report_id>/', fingerprints_view, name='create_fingerprint_report'),
    path('report/conclusion_report/<int:header_report_id>/', conclusion_view, name='create_conclusion_report'),
    path('report/considerations_report/<int:header_report_id>/', considerations_view, name='create_considerations_report'),

    # Rotas para edição de relatórios
    #path('report/preservation_report/<int:header_report_id>/<int:id>/', local_preservation_report_view, name='edit_preservation_report'),
    #path('report/description_report/<int:header_report_id>/<int:id>/', local_description_report_view, name='edit_description_report'),
    #path('report/edit_clues_and_traces_report/<int:header_report_id>/<int:id>/', clues_and_traces_view, name='edit_clues_and_traces_report'),
    #path('report/edit_collected_items_report/<int:header_report_id>/<int:id>/', collected_items_view, name = 'edit_collected_items_report'),
    #path('report/edit_perinecroscopic_report/<int:header_report_id>/<int:id>/', perinecroscopic_view, name='edit_perinecroscopic_report'),

    # SECTIONS
    # Rota para exibir o formulário da seção em diferentes templates
    # path('section-report/<int:header_report_id>/template1/', section_report_view, {'template_name': 'report/template1.html'}, name='section_report_template1'),
    # path('section-report/<int:header_report_id>/template2/', section_report_view, {'template_name': 'report/template2.html'}, name='section_report_template2'),
    
    # Rota para editar uma seção específica em template1
    # path('section-report/<int:id>/<int:header_report_id>/template1/', section_report_view, {'template_name': 'report/template1.html'}, name='edit_section_report_template1'),
    
    # Rota para editar uma seção específica em template2
    # path('section-report/<int:id>/<int:header_report_id>/template2/', section_report_view, {'template_name': 'report/template2.html'}, name='edit_section_report_template2'),

]

