// Import required namespaces for models and repositories
using System.Net.Http;                  // Voor HttpClient (webservice aanroepen)
using System.Text.Json;                 // Voor JSON (de)serialisatie
using Laptopreservation.Models;         // Toegang tot het Laptop model
using Laptopreservation.Repositories;   // Toegang tot ILaptopRepository interface

// Namespace for service implementations
namespace Laptopreservation.Services
{
    // Service-klasse die laptop-gerelateerde logica bevat (combineert webservice + DB)
    public class LaptopService : ILaptopService
    {
        // Referentie naar de repository (data-uit de DB)
        private readonly ILaptopRepository _laptopRepo;

        // Één gedeelde HttpClient voor de hele app (best practice: niet per call aanmaken)
        private static readonly HttpClient HttpClient = new HttpClient();

        // URL van de webservice die laptops levert (eerst proberen, anders fallback)
        private const string ServiceUrl = "https://examenexamplehowest-d0fxhdbjhra6czcp.northeurope-01.azurewebsites.net/laptops";

        // Constructor met dependency injection van de repository
        public LaptopService(ILaptopRepository laptopRepo)
        {
            _laptopRepo = laptopRepo;   // bewaar dependency in veld
        }

        // Haal alle laptops op, alfabetisch op Model
        public List<Laptop> GetAllLaptopsSortedByModel()
        {
            // Try webservice first as per assignment; fallback to DB if unavailable
            try
            {
                // Synchronous wait (console-app ok): download JSON van de webservice
                var json = HttpClient.GetStringAsync(ServiceUrl).GetAwaiter().GetResult();

                // Deserialize JSON naar List<Laptop>, case-insensitive op propertynamen
                var laptops = JsonSerializer.Deserialize<List<Laptop>>(json, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                }) ?? new List<Laptop>(); // null-guard: als deserialisatie null is, gebruik lege lijst

                // Sorteer op Model en retourneer
                return laptops.OrderBy(l => l.Model).ToList();
            }
            catch
            {
                // Als webservice faalt (geen internet/timeout/500), val terug op database
                return _laptopRepo.GetAllLaptopsSortedByModel();
            }
        }

        // Zoek laptops via (deel van) modelnaam — voor interactieve selectie in console
        public List<Laptop> GetLaptopsByModel(string model)
        {
            // Gebruik repository (DB) voor zoeken/filteren
            return _laptopRepo.GetLaptopsByModel(model);
        }
    }
}
