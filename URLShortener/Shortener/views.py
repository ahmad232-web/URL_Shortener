import random
import string

from django.shortcuts import render, redirect, get_object_or_404

from .models import ShortenedURL


# ─────────────────────────────────────────────────────────
#  HELPER FUNCTION
#  Generates a random code like "aB3xZ1" (6 characters).
#  We use this as the short part of the URL.
# ─────────────────────────────────────────────────────────

def generate_short_code(length=6):
    # string.ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # string.digits        = "0123456789"
    characters = string.ascii_letters + string.digits

    # Pick `length` random characters and join them into one string
    code = ''.join(random.choices(characters, k=length))

    return code


# ─────────────────────────────────────────────────────────
#  VIEW 1: Home Page
#  URL: /
#  This view handles TWO things:
#    GET  request → just show the empty form
#    POST request → user submitted a URL, shorten it
# ─────────────────────────────────────────────────────────

def home(request):

    # "short_url" will hold the result we show to the user
    short_url = None

    # "error" will hold any error message we want to show
    error = None

    # All previously shortened URLs (to show in the history table)
    all_urls = ShortenedURL.objects.all().order_by('-created_at')

    # ── Handle form submission (POST) ──
    if request.method == 'POST':

        # Get the URL the user typed in the form
        original_url = request.POST.get('original_url', '').strip()

        if not original_url:
            # User submitted an empty form
            error = "Please enter a URL before clicking Shorten."

        else:
            # Check if this URL was already shortened before
            existing = ShortenedURL.objects.filter(original_url=original_url).first()

            if existing:
                # Re-use the existing short code instead of creating a new one
                short_url = request.build_absolute_uri(f'/go/{existing.short_code}/')

            else:
                # Generate a unique short code
                # (keep trying until we find one not already in the database)
                short_code = generate_short_code()
                while ShortenedURL.objects.filter(short_code=short_code).exists():
                    short_code = generate_short_code()

                # Save it to the database
                new_entry = ShortenedURL(
                    original_url=original_url,
                    short_code=short_code,
                )
                new_entry.save()

                # Build the full short URL the user can copy
                short_url = request.build_absolute_uri(f'/go/{short_code}/')

            # Refresh the list after adding
            all_urls = ShortenedURL.objects.all().order_by('-created_at')

    # Send data to the HTML template
    context = {
        'short_url': short_url,    # the generated short link (or None)
        'error': error,            # any error message (or None)
        'all_urls': all_urls,      # list of all shortened URLs
    }

    return render(request, 'home.html', context)


# ─────────────────────────────────────────────────────────
#  VIEW 2: Redirect
#  URL: /go/<short_code>/
#  When someone visits a short link, this view:
#    1. Looks up the short_code in the database
#    2. Adds 1 to the click count
#    3. Redirects the user to the original long URL
# ─────────────────────────────────────────────────────────

def redirect_to_original(request, short_code):

    # Find the database entry with this short_code
    # If it doesn't exist, Django automatically shows a 404 error page
    url_entry = get_object_or_404(ShortenedURL, short_code=short_code)

    # Increase the click counter by 1
    url_entry.click_count += 1
    url_entry.save()

    # Send the user to the original long URL
    return redirect(url_entry.original_url)
