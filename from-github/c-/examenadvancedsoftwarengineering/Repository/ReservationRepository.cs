// Import required namespaces for Entity Framework Core and data access
using Laptopreservation.Data;          // Toegang tot AppDbContext (EF Core context)
using Laptopreservation.Models;        // Modellen: Reservation, ReservationItem, Laptop
using Microsoft.EntityFrameworkCore;   // EF Core extensies (Include, ThenInclude, AsNoTracking, ...)

namespace Laptopreservation.Repositories
{
    // Concrete implementatie van IReservationRepository (data-toegang voor reservaties)
    public class ReservationRepository : IReservationRepository
    {
        // EF Core DbContext - via DI geïnjecteerd
        private readonly AppDbContext _context;

        // Constructor - bewaart de context in een readonly veld
        public ReservationRepository(AppDbContext context)
        {
            _context = context;
        }

        // Haal ALLE reservaties op, inclusief hun items en bijhorende laptops (eager loading)
        public List<Reservation> GetAllReservations()
        {
            return _context.Reservations
                .Include(r => r.Items)           // laad Reservation.Items mee
                .ThenInclude(i => i.Laptop)      // en daarbinnen ook de gelinkte Laptop
                .ToList();                        // voer de query uit en materialiseer naar List
        }

        // Haal één reservatie op via ID, inclusief items en laptops; null als niet gevonden
        public Reservation? GetById(int reservationId)
        {
            return _context.Reservations
                .Include(r => r.Items)           // laad Items mee
                .ThenInclude(i => i.Laptop)      // en de Laptop per item
                .FirstOrDefault(r => r.ReservationID == reservationId); // filter op PK
        }

        // Voeg een nieuwe reservatie toe (incl. berekening prijzen volgens formule)
        public void AddReservation(Reservation reservation)
        {
            // Bereken totalen volgens formule: UnitPrice = Laptop.Price / 100
            foreach (var item in reservation.Items)
            {
                // Zoek bijhorende laptop; First() gooit exception als niet gevonden
                var laptop = _context.Laptops.First(l => l.ID == item.LaptopID);
                // Prijs per stuk volgens examenregel (let op decimal 'm')
                item.UnitPrice = laptop.Price / 100m;
            }
            // Totale prijs = som(UnitPrice * Quantity) over alle items
            reservation.TotalPrice = reservation.Items.Sum(i => i.UnitPrice * i.Quantity);

            // Markeer reservatie (en gekoppelde items) als te inserten
            _context.Reservations.Add(reservation);
            // Schrijf wijzigingen naar de database
            _context.SaveChanges();
        }

        // Verwijder reservatie op ID; gooi InvalidIdException bij ongeldig ID
        public void DeleteReservationById(int reservationId)
        {
            // Zoek entiteit; null indien niet gevonden
            var entity = _context.Reservations.FirstOrDefault(r => r.ReservationID == reservationId);
            if (entity == null)
            {
                // Eigen exception (vereist aparte klasse InvalidIdException)
                throw new InvalidIdException($"Reservation with ID {reservationId} not found");
            }
            // Markeer voor delete (Items worden via cascade delete mee verwijderd als zo geconfigureerd)
            _context.Reservations.Remove(entity);
            // Persist delete
            _context.SaveChanges();
        }

        // Exporteer alle reservaties (header records) naar CSV (zonder items)
        public void ExportReservationsToCsv(string filePath)
        {
            // Read-only query voor performance (geen tracking/proxy)
            var reservations = _context.Reservations.AsNoTracking().ToList();
            // Maak/overschrijf bestand op opgegeven pad
            using var writer = new StreamWriter(filePath);
            // CSV-kop (kolomnamen)
            writer.WriteLine("ReservationID,TotalPrice,CustomerName,CustomerAddress,CustomerEmail,CustomerPhone");
            // Schrijf elke reservatie als CSV-regel
            foreach (var r in reservations)
            {
                writer.WriteLine(
                    $"{r.ReservationID}," +
                    $"{r.TotalPrice}," + // (zie tip: InvariantCulture)
                    $"{Escape(r.CustomerName)}," +
                    $"{Escape(r.CustomerAddress)}," +
                    $"{Escape(r.CustomerEmail)}," +
                    $"{Escape(r.CustomerPhone)}"
                );
            }
        }

        // Helper om CSV-velden te escapen: quotes verdubbelen en veld in quotes zetten bij ',' of '"'
        private static string Escape(string? input)
        {
            input ??= string.Empty;                         // null-safe
            if (input.Contains(',') || input.Contains('"')) // CSV-gevoelige tekens?
            {
                return '"' + input.Replace("\"", "\"\"") + '"'; // omhul met "..." en "" → "
            }
            return input;                                   // anders ongewijzigd
        }
    }
}
