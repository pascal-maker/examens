using mockexam.Models;
using mockexam.Repositories;
using System.Collections.Generic;
namespace mockexam.Service
{
    public interface IReservationService
    {
        IEnumerable<Reservation> GetAll();
        /// Methods for Reservation
        Reservation GetReservationById(int reservationid);
        /// methpd to get reservtion by id
        void AddReservation(Reservation reservation);
        /// Method to add a new reservation
        void UpdateReservation(Reservation reservation);
        /// Method to update an existing reservation
        void DeleteReservation(int reservationid);
        /// Method to delete a reservation by its ID
        
        
    }
}