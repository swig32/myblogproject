from members.models import Member

def member_stats(request):
    # This returns the total count of members in the database
    return {
        'total_fans': Member.objects.count(),
        'latest_members': Member.objects.all().order_by('-id')[:3]  # Gets the 3 newest fans
    }
