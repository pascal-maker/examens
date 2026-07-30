namespace Laptopreservation.Models
{
    // Deze klasse stelt één regel/onderdeel ("item") van een reservatie voor
    public class ReservationItem
    {
        // Unieke identifier voor dit reservatie-item (Primary Key in de database)
        public int ReservationItemID { get; set; }

        // Foreign Key: verwijst naar de reservatie waar dit item bij hoort
        public int ReservationID { get; set; }

        // Navigatie-eigenschap: maakt de koppeling naar de Reservation object zelf
        public Reservation Reservation { get; set; }

        // Foreign Key: verwijst naar de gekozen laptop
        public int LaptopID { get; set; }

        // Navigatie-eigenschap: maakt de koppeling naar het Laptop object zelf
        public Laptop Laptop { get; set; }

        // Hoeveel stuks van deze laptop de klant heeft gekozen
        public int Quantity { get; set; }

        // Prijs per stuk van deze laptop (komt meestal uit Laptop.Price / 100 volgens de opdracht)
        public decimal UnitPrice { get; set; }
    }
}
