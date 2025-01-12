from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Petitioner, Petition, Signature

# List of valid BioIDs (fill this list with valid BioIDs)
VALID_BIOIDS = [
    "K1YL8VA2HG", "V30EPKZQI2", "QJXQOUPTH9", "CET8NUAE09", 
    "BZW5WWDMUY", "7DMPYAZAP2", "O3WJFGR5WE", "GOYWJVDA8A", 
    "VQKBGSE3EA", "340B1EOCMG", "D05HPPQNJ4", "SEIQTS1H16", 
    "6EBQ28A62V", "E7D6YUPQ6J", "CG1I9SABLL", "2WYIM3QCK9",
    "X16V7LFHR2", "30MY51J1CJ", "BPX8O0YB5L", "49YFTUA96K",
    "DHKFIYHMAZ", "TLFDFY7RDG", "FH6260T08H", "AT66BX2FXM",
    "V2JX0IC633", "LZK7P0X0LQ", "PGPVG5RF42", "JHDCXB62SA",
    "1PUQV970LA", "C7IFP4VWIL", "H5C98XCENC", "FPALKDEL5T",
    "O0V55ENOT0", "CCU1D7QXDT", "RYU8VSS4N5", "6X6I6TSUFG",
    "2BIB99Z54V", "F3ATSRR5DQ", "TTK74SYYAN", "S22A588D75",
    "QTLCWUS8NB", "ABQYUQCQS2", "1K3JTWHA05", "4HTOAI9YKO",
    "88V3GKIVSF", "Y4FC3F9ZGS", "9JSXWO4LGH", "FINNMWJY0G",
    "PD6XPNB80J", "8OLYIE2FRC"
]
# --------------------------------------
# User Registration View
# --------------------------------------
from django.http import JsonResponse

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

        # Validate BioID
        valid_bioids = [
            # Add your valid BioIDs here
        ]
        if bio_id not in valid_bioids:
            # If it's an Ajax request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid BioID. Please enter a valid BioID.'})
            else:
                messages.error(request, 'Invalid BioID. Please enter a valid BioID.')
                return render(request, 'myapp/register.html')

        # Check if BioID or email is already in use
        if Petitioner.objects.filter(bio_id=bio_id).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'This BioID has already been registered.'})
            else:
                messages.error(request, 'This BioID has already been registered.')
                return render(request, 'myapp/register.html')

        if Petitioner.objects.filter(email=email).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'This email has already been registered.'})
            else:
                messages.error(request, 'This email has already been registered.')
                return render(request, 'myapp/register.html')

        # Save the petitioner
        Petitioner.objects.create(
            email=email,
            full_name=full_name,
            date_of_birth=date_of_birth,
            password=password,
            bio_id=bio_id
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Registration successful. Please log in.'})
        else:
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

# --------------------------------------
# Create Petition View
# --------------------------------------
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

# --------------------------------------
# Sign Petition View
# --------------------------------------
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
# Admin Dashboard View
# --------------------------------------
def admin_dashboard(request):
    """
    Displays the admin dashboard with all petitions, analytics, and pagination.
    """
    if not request.session.get('is_admin', False):
        return redirect('login')

    petitions = Petition.objects.all()

    total_petitions = petitions.count()
    total_open_petitions = petitions.filter(status='open').count()
    total_closed_petitions = petitions.filter(status='closed').count()

    query = request.GET.get('q', '')
    if query:
        petitions = petitions.filter(title__icontains=query)

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


# --------------------------------------
# Close Petition View
# --------------------------------------
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

