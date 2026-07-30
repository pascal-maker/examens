// Importeren van de models namespace zodat we de Reservation klasse kunnen gebruiken
using Laptopreservation.Models;

// Namespace voor alle repository-klassen/interfaces (data-toegang laag)
namespace Laptopreservation.Repositories
{
    // Interface (contract) voor een ReservationRepository
    // Deze definieert welke methodes elke concrete repository moet hebben
    public interface IReservationRepository
    {
        // Voeg een nieuwe reservatie toe aan de database
        // Wordt gebruikt wanneer de gebruiker een reservatie maakt via het menu
        void AddReservation(Reservation reservation);

        // Haal alle reservaties op uit de database
        // Wordt gebruikt in menu-optie "Display All Reservations"
        List<Reservation> GetAllReservations();

        // Verwijder een reservatie op basis van het ReservationID
        // Wordt gebruikt in menu-optie "Delete a Reservation"
        void DeleteReservationById(int reservationId);

        // Exporteer alle reservaties naar een CSV-bestand
        // Wordt gebruikt in menu-optie "Write Reservations to a File"
        // Het bestandspad wordt meegegeven (inclusief bestandsnaam met datum)
        void ExportReservationsToCsv(string filePath);

        // Haal één specifieke reservatie op via zijn ID
        // Retourneert null (?) als de ID ongeldig is of niet bestaat
        Reservation? GetById(int reservationId);
    }
}
