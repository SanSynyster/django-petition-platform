from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Petitioner, Petition, Signature

# --------------------------------------
# User Registration View
# --------------------------------------
def register(request):
    """
    Handles user registration, including validation for unique email and BioID.
    """
    if request.method == 'POST':
        email = request.POST['email']
        full_name = request.POST.get('full_name', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        password = make_password(request.POST['password'])
        bio_id = request.POST.get('bio_id', '')

        # Validate unique email and BioID
        if Petitioner.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'myapp/register.html')
        if Petitioner.objects.filter(bio_id=bio_id).exists():
            messages.error(request, 'BioID already registered.')
            return render(request, 'myapp/register.html')

        # Create new petitioner
        Petitioner.objects.create(
            email=email,
            full_name=full_name,
            date_of_birth=date_of_birth,
            password=password,
            bio_id=bio_id
        )
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'myapp/register.html')


# --------------------------------------
# User Login View
# --------------------------------------
def login(request):
    """
    Authenticates the user and sets their session.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user
        try:
            user = Petitioner.objects.get(email=email)
        except Petitioner.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'myapp/login.html')

        if check_password(password, user.password):
            # Set session data
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            request.session['is_admin'] = (email == 'admin@petition.parliament.sr')  # Admin check
            messages.success(request, 'Login successful.')
            return redirect('admin_dashboard' if request.session['is_admin'] else 'dashboard')

        messages.error(request, 'Invalid email or password.')
    return render(request, 'myapp/login.html')


# --------------------------------------
# Petitioner Dashboard
# --------------------------------------
def dashboard(request):
    """
    Displays the user's petitions and open petitions with search functionality.
    """
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session['user_id']
    user_email = request.session['user_email']

    # Fetch petitions
    user_petitions = Petition.objects.filter(petitioner_id=user_id)
    open_petitions = Petition.objects.filter(status='open').exclude(petitioner_id=user_id)

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        user_petitions = user_petitions.filter(title__icontains=query)
        open_petitions = open_petitions.filter(title__icontains=query)

    return render(request, 'myapp/dashboard.html', {
        'email': user_email,
        'petitions': user_petitions,
        'open_petitions': open_petitions,
        'query': query,
    })


def create_petition(request):
    """
    Allows the user to create a new petition.
    """
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user_id = request.session['user_id']

        Petition.objects.create(
            title=title,
            content=content,
            petitioner_id=user_id
        )
        messages.success(request, 'Petition created successfully.')

    return redirect('dashboard')


def sign_petition(request):
    """
    Allows the user to sign a petition.
    """
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == 'POST':
        petition_id = request.POST['petition_id']
        user_id = request.session['user_id']

        # Check if already signed
        if Signature.objects.filter(petition_id=petition_id, petitioner_id=user_id).exists():
            messages.warning(request, 'You have already signed this petition.')
            return redirect('dashboard')

        # Sign petition
        Signature.objects.create(petition_id=petition_id, petitioner_id=user_id)
        petition = Petition.objects.get(id=petition_id)
        petition.signatures += 1
        petition.save()

        messages.success(request, 'Thank you for signing the petition!')
    return redirect('dashboard')


# --------------------------------------
# Admin Dashboard
# --------------------------------------
def admin_dashboard(request):
    """
    Displays the admin dashboard with all petitions, including analytics.
    """
    if not request.session.get('is_admin', False):
        return redirect('login')

    # Fetch all petitions
    petitions = Petition.objects.all()

    # Analytics
    total_petitions = petitions.count()
    total_open_petitions = petitions.filter(status='open').count()
    total_closed_petitions = petitions.filter(status='closed').count()

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        petitions = petitions.filter(title__icontains=query)

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        petitions = petitions.filter(status=status_filter)

    # Pagination
    paginator = Paginator(petitions, 10)  # Show 10 petitions per page
    page_number = request.GET.get('page')
    petitions_page = paginator.get_page(page_number)

    return render(request, 'myapp/admin_dashboard.html', {
        'petitions': petitions_page,
        'total_petitions': total_petitions,
        'total_open_petitions': total_open_petitions,
        'total_closed_petitions': total_closed_petitions,
        'query': query,
        'status_filter': status_filter,
    })


def close_petition(request):
    """
    Allows the admin to close a petition and provide a response.
    """
    if not request.session.get('is_admin', False):
        return redirect('login')

    if request.method == 'POST':
        petition_id = request.POST['petition_id']
        response = request.POST['response']

        petition = get_object_or_404(Petition, id=petition_id)
        petition.status = 'closed'
        petition.response = response
        petition.save()

        messages.success(request, 'Petition closed successfully.')
    return redirect('admin_dashboard')


# --------------------------------------
# User Logout View
# --------------------------------------
def logout(request):
    """
    Logs out the user by clearing their session.
    """
    request.session.flush()
    messages.info(request, 'You have been logged out.')
    return redirect('login')