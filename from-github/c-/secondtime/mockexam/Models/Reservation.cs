namespace mockexam.Models
{
    public class Reservation
    {
        public int ReservationId { get; set; }

        public string Brand { get; set; } 
        public string Model { get; set; } 

        public string CustomerAdress { get; set; } 
        public string CustomerName { get; set; } 
        public string CustomerEmail { get; set; } 
        public string CustomerPhone { get; set; } 
        public decimal QuantityLaptop { get; set; }
        public decimal TotalPrice { get; set; }

        public override string ToString()
        {
            return $"Reservation ID {ReservationId}: {Brand} {Model}, Customer: {CustomerName}, Address: {CustomerAdress}, Email: {CustomerEmail}, Phone: {CustomerPhone}, Quantity: {QuantityLaptop}, Total Price: {TotalPrice:EUR}";
        }

        // Navigation property
    }
}