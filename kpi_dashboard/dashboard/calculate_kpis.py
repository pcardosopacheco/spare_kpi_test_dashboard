import json
import numpy as np

def calculate_ridership_kpis(data):
    total_requested_boardings = len(data)
    completed_boardings = sum(1 for trip in data if trip.get('status') == 'completed')
    boarding_cancellations = sum(1 for trip in data if trip.get('status') == 'cancelled')
    boarding_cancellations_no_show = sum(1 for trip in data if trip.get('cancellationReason') == 'noShow')
    total_requests = len(set(trip.get('id') for trip in data if trip.get('id')))
    completed_requests = completed_boardings 
    request_cancellations = boarding_cancellations
    request_cancellations_no_show = boarding_cancellations_no_show

    avg_boardings_per_service_hr = completed_boardings / total_requested_boardings if total_requested_boardings else 0
    cancellation_percentage = (boarding_cancellations / total_requested_boardings) * 100 if total_requested_boardings else 0
    cancellation_percentage_no_show = (boarding_cancellations_no_show / total_requested_boardings) * 100 if total_requested_boardings else 0

    avg_requests_per_rider = total_requests / len(set(trip.get('riderId') for trip in data if trip.get('riderId'))) if len(set(trip.get('riderId') for trip in data if trip.get('riderId'))) else 0
    avg_travel_duration = np.mean([trip.get('tripDurationSeconds') for trip in data if trip.get('tripDurationSeconds') is not None]) / 60 if total_requested_boardings else 0
    avg_travel_distance = np.mean([trip.get('estimatedTravelDistanceM') for trip in data if trip.get('estimatedTravelDistanceM') is not None]) / 1000 if total_requested_boardings else 0
    wait_times = [trip.get('tripWaitSeconds') for trip in data if trip.get('tripWaitSeconds') is not None]
    mean_wait_time = np.mean(wait_times) / 60 if wait_times else 0
    median_wait_time = np.median(wait_times) / 60 if wait_times else 0

    admin_bookings = sum(1 for trip in data if trip.get('createdInterface') == 'adminInterface')
    mobile_app_bookings = sum(1 for trip in data if trip.get('createdInterface') == 'riderInterface')
    web_bookings = sum(1 for trip in data if trip.get('createdInterface') == 'riderWebInterface')
    ivr_bookings = sum(1 for trip in data if trip.get('createdInterface') == 'ivrInterface')

    total_bookings = admin_bookings + mobile_app_bookings + web_bookings + ivr_bookings

    bookings_from_admin_panel = admin_bookings 
    bookings_from_rider_mobile_app = mobile_app_bookings
    bookings_from_rider_web = web_bookings 
    bookings_from_ivr = ivr_bookings 
    avg_riders_per_request = np.mean([trip.get('numRidersAdult') for trip in data]) if total_requested_boardings else 0

    kpis = {
        "total_requested_boardings": total_requested_boardings,
        "completed_boardings": completed_boardings,
        "avg_boardings_per_service_hr": avg_boardings_per_service_hr,
        "boarding_cancellations": boarding_cancellations,
        "boarding_cancellations_no_show": boarding_cancellations_no_show,
        "cancellation_percentage": round(cancellation_percentage, 2),
        "cancellation_percentage_no_show": round(cancellation_percentage_no_show, 2),
        "total_requests": total_requests,
        "completed_requests": completed_requests,
        "no_drivers_available_requests": 0,  # Assuming there are no such requests in the data
        "request_cancellations": request_cancellations,
        "request_cancellations_no_show": request_cancellations_no_show,
        "avg_requests_per_rider": round(avg_requests_per_rider, 2),
        "avg_travel_duration": round(avg_travel_duration, 2),
        "avg_travel_distance": round(avg_travel_distance, 2),
        "mean_wait_time": round(mean_wait_time, 2),
        "median_wait_time": round(median_wait_time, 2),
        "bookings_from_admin_panel": round(bookings_from_admin_panel, 2),
        "bookings_from_rider_mobile_app": round(bookings_from_rider_mobile_app, 2),
        "bookings_from_rider_web": round(bookings_from_rider_web, 2),
        "flag_down_bookings": 0,  # Assuming there are no flag down bookings in the data
        "bookings_from_ivr": round(bookings_from_ivr, 2),
        "avg_riders_per_request": round(avg_riders_per_request, 2)
    }
    return kpis

if __name__ == "__main__":
    # Load the data from the cached JSON files
    with open('cache/ridership_data.json', 'r') as f:
        ridership_data = json.load(f)

    # Calculate and print KPIs
    if ridership_data:
        kpis = calculate_ridership_kpis(ridership_data)
        for key, value in kpis.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
    else:
        print("No ridership data found.")
