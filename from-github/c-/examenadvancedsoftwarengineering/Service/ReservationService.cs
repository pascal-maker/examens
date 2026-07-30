// Import required namespaces for models and repositories
using Laptopreservation.Models;            // Toegang tot het Reservation-model
using Laptopreservation.Repositories;      // Toegang tot IReservationRepository

// Namespace for service implementations
namespace Laptopreservation.Services
{
    // Service-laag voor reservaties: bevat domeinlogica en roept de repository aan
    public class ReservationService : IReservationService
    {
        // Referentie naar de repository (data-toegangslaag)
        private readonly IReservationRepository _reservationRepo;

        // Constructor met dependency injection van de repository
        public ReservationService(IReservationRepository reservationRepo)
        {
            _reservationRepo = reservationRepo;    // bewaar dependency in veld
        }

        // Maak een nieuwe reservatie aan (logica kan hier; opslag via repository)
        public void AddReservation(Reservation reservation)
        {
            _reservationRepo.AddReservation(reservation); // delegatie naar repo
        }

        // Haal alle reservaties op (incl. items/laptops als repo dat zo laadt)
        public List<Reservation> GetAllReservations()
        {
            return _reservationRepo.GetAllReservations();  // delegatie naar repo
        }

        // Verwijder een reservatie op ID (repo gooit InvalidIdException indien fout)
        public void DeleteReservationById(int reservationId)
        {
            _reservationRepo.DeleteReservationById(reservationId); // delegatie
        }

        // Exporteer alle reservatie-headers naar CSV (bestandspad doorgeven)
        public void ExportReservationsToCsv(string filePath)
        {
            _reservationRepo.ExportReservationsToCsv(filePath);    // delegatie
        }

        // Haal één reservatie op via ID (kan null teruggeven als niet gevonden)
        public Reservation? GetById(int reservationId)
        {
            return _reservationRepo.GetById(reservationId);        // delegatie
        }
    }
}
