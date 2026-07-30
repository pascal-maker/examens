using mockexam.Models;        // Needed to use the Reservation model
using mockexam.Repositories;  // Needed for the IReservationRepository interface

namespace mockexam.Service
{
    // This service implements IReservationService
    // It acts as a middle layer between controllers/UI and the repository
    // Its job is to handle business logic related to reservations
    public class ReservationService : IReservationService
    {
        // Private field to store the repository
        // readonly means it can only be set in the constructor
        private readonly IReservationRepository _reservationRepository;

        // Constructor - receives a reservation repository instance via dependency injection
        public ReservationService(IReservationRepository reservationRepository)
        {
            _reservationRepository = reservationRepository;
        }

        // Retrieve all reservations from the repository
        public IEnumerable<Reservation> GetAll()
        {
            return _reservationRepository.GetAll();
        }

        // Retrieve a single reservation by its ID
        public Reservation GetReservationById(int reservationid)
        {
            return _reservationRepository.GetReservationById(reservationid);
        }

        // Add a new reservation
        public void AddReservation(Reservation reservation)
        {
            _reservationRepository.AddReservation(reservation);
        }

        // Update an existing reservation
        public void UpdateReservation(Reservation reservation)
        {
            _reservationRepository.UpdateReservation(reservation);
        }

        // Delete a reservation by its ID
        public void DeleteReservation(int reservationid)
        {
            _reservationRepository.DeleteReservation(reservationid);
        }
    }
}
// This class implements the IReservationService interface to manage Reservation data.