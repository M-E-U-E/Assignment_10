from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Hotel, Summary, PropertyRating
from .forms import HotelForm

# List all hotels
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, "hotel_list.html", {"hotels": hotels})

# View details of a specific hotel
def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    summaries = hotel.summaries.all()  # Get summaries for the hotel
    ratings = hotel.ratings.all()  # Get ratings for the hotel
    return render(request, "hotel_detail.html", {
        "hotel": hotel,
        "summaries": summaries,
        "ratings": ratings,
    })

# Add a new hotel
def hotel_add(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = HotelForm()
    return render(request, "hotel_form.html", {"form": form})

# Edit an existing hotel
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == "POST":
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = HotelForm(instance=hotel)
    return render(request, "hotel_form.html", {"form": form})

# Delete a hotel
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel.delete()
    return HttpResponseRedirect("/")

# Add a summary for a specific hotel
def add_summary(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == "POST":
        summary_text = request.POST.get("summary")
        if summary_text:
            Summary.objects.create(hotel=hotel, summary=summary_text)
            return HttpResponseRedirect(f"/hotel/{hotel.pk}/")
    return render(request, "add_summary.html", {"hotel": hotel})

# Add a rating for a specific hotel
def add_rating(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        if rating and review:
            PropertyRating.objects.create(hotel=hotel, rating=float(rating), review=review)
            return HttpResponseRedirect(f"/hotel/{hotel.pk}/")
    return render(request, "add_rating.html", {"hotel": hotel})
