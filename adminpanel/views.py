from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def admin_login(request):
    if request.user.is_authenticated:
        return redirect("admin_dashboard")
    mensaje = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            mensaje = "Usuario o contraseña incorrectos."
    return render(request, "adminpanel/login.html", {"mensaje": mensaje})


@login_required(login_url="/adminpanel/")
def admin_dashboard(request):
    return render(request, "adminpanel/dashboard.html")


@login_required(login_url="/adminpanel/")
def admin_empleados(request):
    return render(request, "adminpanel/empleados.html")


@login_required(login_url="/adminpanel/")
def admin_reportes(request):
    return render(request, "adminpanel/reportes.html")


def admin_logout(request):
    logout(request)
    return redirect("admin_login")
