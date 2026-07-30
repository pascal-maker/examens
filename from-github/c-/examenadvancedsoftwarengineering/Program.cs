using Laptopreservation;                         // (Optioneel) Hoofdnamespace; alleen nodig als je types hier direct gebruikt
using Laptopreservation.Data;                    // Toegang tot AppDbContext (EF Core context)
using Laptopreservation.Models;                  // Modellen: Laptop, Reservation, ReservationItem
using Laptopreservation.Repositories;            // Repositories: LaptopRepository, ReservationRepository
using Laptopreservation.Services;                // Services: LaptopService, ReservationService
using Microsoft.EntityFrameworkCore;             // EF Core API (DbContextOptionsBuilder, UseMySql, Migrate, ...)

// Simple console menu for the exam assignment using services

var optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();                 // Maak een options-builder voor de DbContext
var connectionString = "server=localhost;database=examenadvancedsoftwarengineering;user=root;password=9370"; // Connectiestring (ontwikkelomgeving)
optionsBuilder.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)); // Configureer Pomelo MySQL provider met autodetect van serverversie

using var db = new AppDbContext(optionsBuilder.Options);                          // Instantieer DbContext met de geconfigureerde opties
db.Database.Migrate();                                                            // Voer migraties uit (maakt DB aan en past schema/seed toe)

// Repositories
var laptopRepo = new LaptopRepository(db);                                        // Concreet repo-object voor laptops (EF Core implementatie)
var reservationRepo = new ReservationRepository(db);                              // Concreet repo-object voor reservaties

// Services
var laptopService = new LaptopService(laptopRepo);                                // Service met logica + (webservice->fallback DB) voor laptops
var reservationService = new ReservationService(reservationRepo);                 // Service voor reservaties (centrale domeinlogica)

while (true)                                                                       // Oneindige lus voor het console-menu
{
    Console.WriteLine();                                                           // Lege regel voor leesbaarheid
    Console.WriteLine("Laptop Reservation System");                                // Titel
    Console.WriteLine("1. Display all laptops (sorted by model)");                 // Menu-optie 1
    Console.WriteLine("2. Create a new reservation");                              // Menu-optie 2
    Console.WriteLine("3. Display all reservations");                              // Menu-optie 3
    Console.WriteLine("4. Write reservations to file");                            // Menu-optie 4
    Console.WriteLine("5. Delete a reservation");                                  // Menu-optie 5
    Console.WriteLine("6. Exit");                                                  // Menu-optie 6
    Console.Write("Choose an option: ");                                           // Prompt gebruiker

    var input = Console.ReadLine();                                                // Lees keuze (string)
    Console.WriteLine();                                                           // Lege regel

    switch (input)                                                                 // Switch op gebruikerskeuze
    {
        case "1":
            // NOTE: Spec asks to load laptops from webservice; if not available, fallback to DB.
            // Currently using DB via service; web fetch can be added in the service with fallback.
            var laptops = laptopService.GetAllLaptopsSortedByModel();              // Haal laptops op (service probeert webservice en valt terug op DB)
            foreach (var l in laptops)                                             // Loop door de lijst
            {
                Console.WriteLine($"[{l.ID}] {l.Brand} {l.Model} - Price: {l.Price}"); // Print basisinfo (Price = aankoopprijs uit bron)
            }
            break;

        case "2":
            CreateReservationFlow(laptopService, reservationService);              // Start de flow om een nieuwe reservatie te maken
            break;

        case "3":
            var reservations = reservationService.GetAllReservations();            // Haal alle reservaties (incl. Items en Laptop via repo Include)
            foreach (var r in reservations)                                        // Loop door reservaties
            {
                Console.WriteLine($"Reservation {r.ReservationID} - {r.CustomerName} - {r.CustomerEmail}"); // Header van reservatie
                foreach (var item in r.Items)                                      // Loop door de items per reservatie
                {
                    Console.WriteLine($"  Laptop {item.LaptopID} x{item.Quantity} @ {item.UnitPrice} = {item.UnitPrice * item.Quantity}"); // Detailregel
                }
                Console.WriteLine($"  Total: {r.TotalPrice}");                     // Totaal van de reservatie
            }
            break;

        case "4":
            var fileName = $"reservations_{DateTime.Today:yyyyMMdd}.csv";          // Bestandsnaam met datum (examen-eis)
            reservationService.ExportReservationsToCsv(fileName);                  // Exporteer alleen reservatie-headers naar CSV (geen items)
            Console.WriteLine($"Exported to {fileName}");                          // Feedback aan gebruiker
            break;

        case "5":
            Console.Write("Enter reservation ID to delete: ");                     // Prompt voor ID
            if (int.TryParse(Console.ReadLine(), out var id))                      // Parse naar int met validatie
            {
                try
                {
                    reservationService.DeleteReservationById(id);                  // Verwijder via service (repo gooit InvalidIdException bij niet-gevonden)
                    Console.WriteLine("Deleted.");                                 // Succesmelding
                }
                catch (InvalidIdException ex)                                      // Specifieke eigen exceptie voor ongeldige ID
                {
                    Console.WriteLine($"Error: {ex.Message}");                     // Toon foutboodschap
                }
            }
            else
            {
                Console.WriteLine("Invalid number.");                               // Foutmelding bij parse failure
            }
            break;

        case "6":
            return;                                                                 // Verlaat de applicatie (breekt while-lus)

        default:
            Console.WriteLine("Invalid option.");                                   // Ongeldige menu-keuze
            break;
    }
}

static void CreateReservationFlow(ILaptopService laptopService, IReservationService reservationService) // Losse methode voor optie 2
{
    // Collect items (brand/model + quantity)
    var items = new List<ReservationItem>();                                        // Tijdelijke lijst van gekozen items
    while (true)                                                                    // Herhaal tot gebruiker stopt
    {
        Console.Write("Enter (part of) laptop model to search: ");                  // Prompt model-zoekterm
        var search = Console.ReadLine() ?? string.Empty;                            // Lees input (null-guard)
        var matches = laptopService.GetLaptopsByModel(search);                      // Zoek laptops op (deel van) model in DB
        if (matches.Count == 0)                                                     // Geen resultaten?
        {
            Console.WriteLine("No laptops found.");                                 // Meld het
            continue;                                                               // Opnieuw vragen
        }
        foreach (var l in matches)                                                  // Toon gevonden laptops
        {
            Console.WriteLine($"[{l.ID}] {l.Brand} {l.Model} (purchase price: {l.Price})"); // Print ID/merk/model/bronprijs
        }
        Console.Write("Choose laptop ID: ");                                        // Prompt voor ID-keuze
        if (!int.TryParse(Console.ReadLine(), out var laptopId))                    // Valideer integer
        {
            Console.WriteLine("Invalid ID.");                                       // Foutmelding
            continue;                                                               // Terug naar begin van while
        }
        var chosen = matches.FirstOrDefault(l => l.ID == laptopId);                 // Check of gekozen ID in de lijst zit
        if (chosen == null)                                                         // Niet gevonden?
        {
            Console.WriteLine("ID not in list.");                                   // Meld het
            continue;                                                               // Opnieuw
        }
        Console.Write("Quantity: ");                                                // Prompt voor aantal
        if (!int.TryParse(Console.ReadLine(), out var qty) || qty <= 0)             // Valideer hoeveelheid > 0
        {
            Console.WriteLine("Invalid quantity.");                                 // Foutmelding
            continue;                                                               // Opnieuw
        }
        items.Add(new ReservationItem { LaptopID = chosen.ID, Quantity = qty });    // Voeg item (zonder UnitPrice) toe; prijs wordt later berekend

        Console.Write("Add another laptop? (y/n): ");                               // Vraag of er nog een item bij moet
        var more = (Console.ReadLine() ?? "n").Trim().ToLowerInvariant();           // Normaliseer input
        if (more != "y") break;                                                     // Stoppen als niet 'y'
    }

    // Customer details
    Console.Write("Customer name: ");                                               // Prompt naam
    var name = Console.ReadLine() ?? string.Empty;                                  // Lees naam
    Console.Write("Customer address: ");                                            // Prompt adres
    var address = Console.ReadLine() ?? string.Empty;                               // Lees adres
    Console.Write("Customer email: ");                                              // Prompt email
    var email = Console.ReadLine() ?? string.Empty;                                 // Lees email
    Console.Write("Customer phone: ");                                              // Prompt telefoon
    var phone = Console.ReadLine() ?? string.Empty;                                 // Lees telefoon

    // Compose reservation; totals computed in repository AddReservation via service
    var reservation = new Reservation                                                // Maak het Reservation-object
    {
        CustomerName = name,                                                         // Zet klantnaam
        CustomerAddress = address,                                                   // Zet adres
        CustomerEmail = email,                                                       // Zet email
        CustomerPhone = phone,                                                       // Zet telefoon
        Items = items                                                                // Koppel gekozen items
    };

    // Confirm
    Console.Write("Confirm reservation? (y/n): ");                                   // Vraag bevestiging
    var confirm = (Console.ReadLine() ?? "n").Trim().ToLowerInvariant();             // Normaliseer input
    if (confirm == "y")                                                              // Bevestigd?
    {
        reservationService.AddReservation(reservation);                              // Sla op; repo berekent UnitPrice en TotalPrice en bewaart
        Console.WriteLine($"Created reservation with ID {reservation.ReservationID}, total {reservation.TotalPrice}"); // Toon resultaat (ID na SaveChanges)
    }
    else
    {
        Console.WriteLine("Cancelled.");                                             // Geannuleerd door gebruiker
    }
}
