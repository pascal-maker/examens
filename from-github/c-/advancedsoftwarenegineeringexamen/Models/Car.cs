namespace CTAndAI.CarReservationSystem.Models
{
    public class Car
    {
        public int Id { get; set; }
        public string Brand { get; set; }
        public string Model { get; set; }
        public int Year { get; set; }
        public decimal PricePerDay { get; set; }
        public bool Electric { get; set; }
        public string LicensePlate { get; set; }
    }
}
    