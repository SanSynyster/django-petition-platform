from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Petitioner
from .models import Petition

# --------------------------------------
# User Registration View
# --------------------------------------
def register(request):
    """
    Handles the registration of a new petitioner. 
    Validates email and BioID for uniqueness, hashes the password, 
    and saves the petitioner to the database.
    """
    if request.method == 'POST':
        # Extract form data
        email = request.POST['email']
        full_name = request.POST.get('full_name', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        password = make_password(request.POST['password'])
        bio_id = request.POST.get('bio_id', '')

        # Validation: Check if email or BioID is already registered
        if Petitioner.objects.filter(email=email).exists():
            return render(request, 'myapp/register.html', {'error': 'Email already registered'})
        if Petitioner.objects.filter(bio_id=bio_id).exists():
            return render(request, 'myapp/register.html', {'error': 'BioID already registered'})

        # Save petitioner to the database
        Petitioner.objects.create(
            email=email,
            full_name=full_name,
            date_of_birth=date_of_birth,
            password=password,
            bio_id=bio_id
        )

        # Redirect to the login page after successful registration
        return redirect('login')

    # Render the registration page for GET requests
    return render(request, 'myapp/register.html')


# --------------------------------------
# User Login View
# --------------------------------------
def login(request):
    """
    Handles user login by authenticating email and password.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Validate email
        try:
            user = Petitioner.objects.get(email=email)
        except Petitioner.DoesNotExist:
            return render(request, 'myapp/login.html', {'error': 'Invalid email or password'})

        # Validate password
        if check_password(password, user.password):
            # Use Django's session framework to log in the user
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            return redirect('dashboard')  # Redirect to the petitioner's dashboard
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid email or password'})

    # Render the login page for GET requests
    return render(request, 'myapp/login.html')


# --------------------------------------
# Petitioner Dashboard View
# --------------------------------------
def dashboard(request):
    """
    Petitioner dashboard view with user's petitions and open petitions to sign.
    """
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect to login if not authenticated

    # Fetch the logged-in user's details
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')

    # Fetch petitions created by the user
    user_petitions = Petition.objects.filter(petitioner_id=user_id)

    # Fetch open petitions not created by the user
    open_petitions = Petition.objects.filter(status='open').exclude(petitioner_id=user_id)

    return render(request, 'myapp/dashboard.html', {
        'email': user_email,
        'petitions': user_petitions,
        'open_petitions': open_petitions,
    })

def create_petition(request):
    """
    Allows the logged-in user to create a new petition.
    """
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user_id = request.session.get('user_id')

        # Save the petition
        Petition.objects.create(
            title=title,
            content=content,
            petitioner_id=user_id
        )

    return redirect('dashboard')  # Redirect back to the dashboard

from .models import Signature

def sign_petition(request):
    """
    Allows the logged-in user to sign a petition.
    """
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        petition_id = request.POST.get('petition_id')
        user_id = request.session.get('user_id')

        # Check if the user has already signed the petition
        if Signature.objects.filter(petition_id=petition_id, petitioner_id=user_id).exists():
            return redirect('dashboard')  # Redirect back if already signed

        # Add a new signature
        Signature.objects.create(petition_id=petition_id, petitioner_id=user_id)

        # Increment the petition's signature count
        petition = Petition.objects.get(id=petition_id)
        petition.signatures += 1
        petition.save()

    return redirect('dashboard')  # Redirect back to the dashboard
# --------------------------------------
# User Logout View
# --------------------------------------
def logout(request):
    """
    Logs out the user by clearing the session.
    """
    request.session.flush()
    return redirect('login')  # Redirect to login page