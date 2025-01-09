from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-petition/', views.create_petition, name='create_petition'),
    path('sign-petition/', views.sign_petition, name='sign_petition'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Add this
    path('close-petition/', views.close_petition, name='close_petition'),  # Add this
    path('logout/', views.logout, name='logout'),
]

#VALID_BIOIDS = [
#     "K1YL8VA2HG", "V30EPKZQI2", "QJXQOUPTH9", "CET8NUAE09", 
#     "BZW5WWDMUY", "7DMPYAZAP2", "O3WJFGR5WE", "GOYWJVDA8A", 
#     "VQKBGSE3EA", "340B1EOCMG", "D05HPPQNJ4", "SEIQTS1H16", 
#     "6EBQ28A62V", "E7D6YUPQ6J", "CG1I9SABLL", "2WYIM3QCK9",
#     "X16V7LFHR2", "30MY51J1CJ", "BPX8O0YB5L", "49YFTUA96K",
#     "DHKFIYHMAZ", "TLFDFY7RDG", "FH6260T08H", "AT66BX2FXM",
#     "V2JX0IC633", "LZK7P0X0LQ", "PGPVG5RF42", "JHDCXB62SA",
#     "1PUQV970LA", "C7IFP4VWIL", "H5C98XCENC", "FPALKDEL5T",
#     "O0V55ENOT0", "CCU1D7QXDT", "RYU8VSS4N5", "6X6I6TSUFG",
#     "2BIB99Z54V", "F3ATSRR5DQ", "TTK74SYYAN", "S22A588D75",
#     "QTLCWUS8NB", "ABQYUQCQS2", "1K3JTWHA05", "4HTOAI9YKO",
#     "88V3GKIVSF", "Y4FC3F9ZGS", "9JSXWO4LGH", "FINNMWJY0G",
#     "PD6XPNB80J", "8OLYIE2FRC"
# ]