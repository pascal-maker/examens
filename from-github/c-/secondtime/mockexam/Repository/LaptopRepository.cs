using mockexam.Data;       // Needed to access AppDbContext (EF Core database context)
using mockexam.Models;     // Needed to use the Laptop model
using Microsoft.EntityFrameworkCore; // Provides EF Core functionality (e.g., querying, ToList, FirstOrDefault)

namespace mockexam.Repositories
{
    // This class implements the ILaptopRepository interface
    // It is responsible for interacting with the database to manage Laptop data
    public class LaptopRepository : ILaptopRepository
    {
        // Private field to store the database context
        private readonly AppDbContext _context;

        // Constructor injection: EF Core will pass AppDbContext when creating this repository
        public LaptopRepository(AppDbContext context)
        {
            _context = context;
        }

        // Retrieves all laptops from the database and returns them as a List
        public List<Laptop> GetAllLaptops()
        {
            return _context.Laptops.ToList(); // Executes a SQL SELECT * FROM Laptops
        }

        // Retrieves a single laptop by its Id
        public Laptop GetLaptopById(int id)
        {
            // Searches for the first laptop with the matching Id
            // If no match is found, throws an exception
            return _context.Laptops.FirstOrDefault(l => l.Id == id) 
                   ?? throw new InvalidOperationException("Laptop not found.");
        }
    }
}
// This class implements the ILaptopRepository interface to manage Laptop data in the database.