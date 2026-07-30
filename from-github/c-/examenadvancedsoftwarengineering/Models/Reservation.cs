namespace Laptopreservation.Models
{
    // De Reservation klasse stelt één volledige reservatie voor (gemaakt door een klant)
    public class Reservation
    {
        // Unieke ID van de reservatie (Primary Key in de database)
        public int ReservationID { get; set; }

        // Totale prijs van de reservatie (som van alle ReservationItems)
        public decimal TotalPrice { get; set; }

        // Naam van de klant die de reservatie maakt
        public string CustomerName { get; set; }

        // Adres van de klant
        public string CustomerAddress { get; set; }

        // E-mailadres van de klant
        public string CustomerEmail { get; set; }

        // Telefoonnummer van de klant
        public string CustomerPhone { get; set; }

        // Lijst van alle laptops die in deze reservatie zitten
        // Dit is een "one-to-many" relatie: één reservatie kan meerdere ReservationItems bevatten
        public List<ReservationItem> Items { get; set; } = new();
    }
}
