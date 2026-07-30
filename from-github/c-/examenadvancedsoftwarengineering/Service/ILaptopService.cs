using Laptopreservation.Models;

namespace Laptopreservation.Services
{
    public interface ILaptopService
    {
        // Haal alle laptops op, gesorteerd op modelnaam
        List<Laptop> GetAllLaptopsSortedByModel();

        // Zoek laptops op (deel van) modelnaam, gesorteerd op modelnaam
        List<Laptop> GetLaptopsByModel(string model);
    }
}
