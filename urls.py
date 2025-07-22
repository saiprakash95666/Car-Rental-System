from django.urls import path
from Portal import views

urlpatterns = [
    path('', views.LoginPage, name='loginpage'),
    path('login/', views.Login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.Logout, name='logout'),
    path('SearchCars/', views.SearchCars, name='SearchCars'),
    path('Mycarlist/', views.Mycarlist, name='Mycarlist'),
    path('Favcarlist/', views.Favcarlist, name='Favcarlist'),
    path('Add_Favcar/<str:carid>', views.Add_Favcar, name='Add_Favcar'),
    # url for Cars
    path('Add_Car/', views.Add_Car, name='Add_Car'),
    
    path('Update_car_Page/<str:carid>', views.Update_car_Page, name='Update_car_Page'),
    path('update_car_submit/<str:carid>/', views.update_car_submit, name='update_car_submit'),

    path('Add_CarSubmit/', views.Add_CarSubmit, name='Add_CarSubmit'),
    path('CarData/', views.CarData, name='CarData'),
    path('IssueCars/', views.Issue_CarSubmit, name='IssueCars'),
    path('IssueCars_list/', views.IssueCars_list, name='IssueCars_list'),
    path('Update_CarStatus_Page/<str:id>', views.Update_CarStatus_Page, name='Update_CarStatus_Page'),
    path('Update_CarStatSubmit/<str:id>/', views.Update_CarStatSubmit, name='Update_CarStatSubmit'),
    # url for customer register
    path('Customer_Regiter/', views.Customer_Regiter, name='Customer_Regiter'),
    path('Customer_RegiterSubmit/', views.Customer_RegiterSubmit, name='Customer_RegiterSubmit'),

    path('index/', views.Index, name='index'),
    
    # # url for Staff
    # path('staffList/', views.StaffList, name='staffList'),
    # path('createStaff/', views.Create_Staff, name='createStaff'),
    # path('createStaffSubmit/', views.Create_StaffSubmit, name='createStaffSubmit'),
    # path('updateStaffpage/<str:userid>', views.Update_Staff_Page, name='updateStaffpage'),

    # path('updateStaffsubmit/<str:userid>/', views.Update_StaffSubmit, name='updateStaffsubmit'),
    # path('deleteUser/<str:userid>', views.Delete_User, name='deleteUser'),

]