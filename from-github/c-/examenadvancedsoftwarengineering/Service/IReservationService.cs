using Laptopreservation.Models;

namespace Laptopreservation.Services
{
    public interface IReservationService
    {
        void AddReservation(Reservation reservation);
        List<Reservation> GetAllReservations();
        void DeleteReservationById(int reservationId);
        void ExportReservationsToCsv(string filePath);
        Reservation? GetById(int reservationId);
    }
}
