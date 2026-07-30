namespace CTAndAI.CarReservationSystem.Models
{
    public class CarReservation
    {
        public int Id { get; set; }
        public int CarId { get; set; }
        public string CustomerName { get; set; }
        public int Duration { get; set; }
        public decimal Cost { get; set; }
        public bool ElectricRequired { get; set; }
    }
}
