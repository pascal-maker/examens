// Importeert de namespace waar de Laptop-klasse gedefinieerd is
using Laptopreservation.Models;

// Plaatst de interface in de Repositories-namespace (logische laag voor data-toegang)
namespace Laptopreservation.Repositories
{
    // Definieert een contract voor een Laptop-repository (implementatie volgt in een concrete klasse)
    public interface ILaptopRepository
    {
        // Haalt alle laptops op en geeft ze terug gesorteerd op het Model-veld (A-Z).
        // Gebruik: voor menu-optie "Toon alle laptops alfabetisch op model".
        List<Laptop> GetAllLaptopsSortedByModel();

        // Haalt laptops op die overeenkomen met (of lijken op) een opgegeven modelnaam.
        // Handig voor selectie bij het maken van een reservatie (filteren op model).
        List<Laptop> GetLaptopsByModel(string model);
    }
}
