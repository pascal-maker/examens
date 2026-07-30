using mockexam.Models; // Needed so we can use the Reservation model

namespace mockexam.Repositories
{
    // This interface defines the contract for a Reservation repository.
    // Any class that implements this interface must provide implementations
    // for the following methods to handle Reservation data operations.
    public interface IReservationRepository
    {
        // Get all reservations from the data source
        IEnumerable<Reservation> GetAll();

        // Get a single reservation by its ID
        Reservation GetReservationById(int reservationid);

        // Add a new reservation to the data source
        void AddReservation(Reservation reservation);

        // Update an existing reservation in the data source
        void UpdateReservation(Reservation reservation);

        // Delete a reservation by its ID
        void DeleteReservation(int reservationid);
    }
}
// This interface is used to define the methods that a Reservation repository must implement.