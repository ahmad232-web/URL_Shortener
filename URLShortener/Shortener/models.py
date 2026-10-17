from django.db import models


# ─────────────────────────────────────────────
#  This model stores ONE shortened URL entry.
#  Think of it like a row in a spreadsheet:
#    original_url  → the long URL the user pasted
#    short_code    → the 6-letter code we generated (e.g. "aB3xZ1")
#    created_at    → when it was created
#    click_count   → how many times it was visited
# ─────────────────────────────────────────────

class ShortenedURL(models.Model):

    # The full, long URL entered by the user
    original_url = models.URLField(max_length=2000)

    # A short random code like "aB3xZ1" – must be unique for every entry
    short_code = models.CharField(max_length=10, unique=True)

    # Automatically saved when the record is first created
    created_at = models.DateTimeField(auto_now_add=True)

    # Starts at 0, increases by 1 every time someone visits the short link
    click_count = models.IntegerField(default=0)

    # This controls how the object is shown in the Django admin panel
    def __str__(self):
        return f"{self.short_code}  →  {self.original_url}"
