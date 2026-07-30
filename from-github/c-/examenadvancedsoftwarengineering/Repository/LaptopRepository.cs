// Import required namespaces for Entity Framework Core and data access
using Laptopreservation.Data;      // Toegang tot AppDbContext (EF Core database context)
using Laptopreservation.Models;    // Toegang tot de Laptop-klasse
using Microsoft.EntityFrameworkCore; // Extra EF Core functionaliteit (bv. LINQ methodes)

// Namespace voor repository implementaties
namespace Laptopreservation.Repositories
{
    // Concrete implementatie van het ILaptopRepository interface
    public class LaptopRepository : ILaptopRepository
    {
        // Privéveld dat de DbContext vasthoudt om queries uit te voeren
        private readonly AppDbContext _context;

        // Constructor: AppDbContext wordt via dependency injection meegegeven
        // Hierdoor hoeft de repository zelf geen connectiestring of DbContext aan te maken
        public LaptopRepository(AppDbContext context)
        {
            _context = context;
        }

        // Methode om alle laptops op te halen, alfabetisch gesorteerd op Model
        public List<Laptop> GetAllLaptopsSortedByModel()
        {
            // Query: selecteer alle laptops uit de database
            // Sorteer ze op de 'Model' kolom
            // Zet het resultaat om in een List<Laptop>
            return _context.Laptops
                .OrderBy(l => l.Model)
                .ToList();
        }

        // Methode om laptops te zoeken op modelnaam (of een deel ervan)
        // Handig bij reservatie aanmaken → gebruiker typt bv. "XPS" en vindt "XPS 13"
        public List<Laptop> GetLaptopsByModel(string model)
        {
            // Trim spaties weg, en voorkom null door string.Empty te gebruiken
            model = model?.Trim() ?? string.Empty;

            // Query: zoek laptops waarvan het Model de zoekstring bevat
            // Gebruik Contains (case-sensitive of case-insensitive hangt van DB collation af)
            // Sorteer resultaat opnieuw op Model
            return _context.Laptops
                .Where(l => l.Model.Contains(model))
                .OrderBy(l => l.Model)
                .ToList();
        }
    }
}
