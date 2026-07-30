using mockexam.Service;          // Service layer (business logic)
using mockexam.Data;             // EF Core DbContext
using Microsoft.EntityFrameworkCore; // EF Core configuration (UseMySQL, DbContextOptionsBuilder)
using mockexam.Repositories;     // Repositories (data access)
using mockexam.Models;           // Entity models like Laptop, Reservation
using System.Net.Http;           // HttpClient for calling the external web service

namespace mockexamSystem
{
    class Program
    {
        // Entry point of the console app. Marked async because we await HTTP calls.
        static async Task Main(string[] args)
        {
            // Build EF Core options to connect to the MySQL database "mockexam"
            var options = new DbContextOptionsBuilder<AppDbContext>()
                // Configure database provider + connection string
                .UseMySQL("server=localhost;database=mockexam;user=root;password=9370")
                .Options;

            // Create a DbContext instance (lifetime bound to the using scope)
            using var context = new AppDbContext(options);

            // Instantiate repositories that know how to talk to the database
            var laptopRepo = new LaptopRepository(context);
            var reservationRepo = new ReservationRepository(context);

            // Create services that implement business logic and delegate to repositories
            var laptopService = new LaptopService(laptopRepo);
            var reservationService = new ReservationService(reservationRepo);

            // Simple loop to keep showing the menu until the user chooses to exit
            bool exit = false;
            while (!exit)
            {
                // Display menu options
                Console.WriteLine("1. Import Laptops from CSV");
                Console.WriteLine("2. Add a Laptop");
                Console.WriteLine("3. View Reservation");
                Console.WriteLine("4. Export Reservations to CSV");
                Console.WriteLine("5. Delete Reservation");
                Console.WriteLine("6. Exit");
                Console.Write("Choose an option: ");

                // Read the user's menu selection
                var choice = Console.ReadLine();

                switch (choice)
                {
                    // 1) Import laptops via HTTP (from external webservice) and show them
                    case "1":
                    {
                        // HttpClient for calling the external laptops endpoint
                        using var client = new HttpClient();

                        // Call the web service (GET laptops)
                        var response = await client.GetAsync("https://examenexamplehowest-d0fxhdbjhra6czcp.northeurope-01.azurewebsites.net/laptops");

                        // Check if HTTP status code indicates success (2xx)
                        if (response.IsSuccessStatusCode)
                        {
                            // Read raw JSON
                            var json = await response.Content.ReadAsStringAsync();

                            // Configure JSON options (case-insensitive property matching)
                            var jsonOptions = new System.Text.Json.JsonSerializerOptions
                            {
                                PropertyNameCaseInsensitive = true
                            };

                            // Deserialize JSON into a list of Laptop objects
                            var importedLaptops = System.Text.Json.JsonSerializer.Deserialize<List<Laptop>>(json, jsonOptions);

                            // Print laptops to the console ordered by Model
                            foreach (var laptop in importedLaptops.OrderBy(l => l.Model))
                            {
                                Console.WriteLine(laptop);
                            }
                        }
                        else
                        {
                            // Inform the user if the web service request failed
                            Console.WriteLine("Webservice returned an error.");
                        }

                        // Leave the switch-case
                        break;
                    }

                    // 2) Add a laptop reservation by collecting input and calculating total
                    case "2":
                    {
                        // Collect laptop brand
                        Console.Write("Enter laptop brand: ");
                        string brand = Console.ReadLine() ?? "";

                        // Collect laptop model
                        Console.Write("Enter laptop model: ");
                        string model = Console.ReadLine() ?? "";

                        // Collect quantity and parse it to int
                        Console.Write("Quantity: ");
                        int quantity = int.Parse(Console.ReadLine() ?? "1"); // NOTE: will throw if input invalid

                        // Collect customer info
                        Console.Write("Customer name: ");
                        string name = Console.ReadLine() ?? "";

                        Console.Write("Address: ");
                        string address = Console.ReadLine() ?? "";

                        Console.Write("Email: ");
                        string email = Console.ReadLine() ?? "";

                        Console.Write("Phone: ");
                        int phone = int.Parse(Console.ReadLine() ?? "0"); // NOTE: will throw if input invalid

                        // Try to find the unit price from the loaded laptops; if not found, default to 1000
                        var unitPrice = laptopService.GetAllLaptops()
                            .FirstOrDefault(l => l.Brand == brand && l.Model == model)?.Price ?? 1000;

                        // Compute total price
                        int total = unitPrice * quantity;

                        // Confirm with user before saving the reservation
                        Console.WriteLine($"Total price: {total} EUR. Confirm? (y/n): ");
                        if (Console.ReadLine()?.ToLower() == "y")
                        {
                            // Create a new reservation object with collected data
                            reservationService.AddReservation(new Reservation
                            {
                                Brand = brand,
                                Model = model,
                                CustomerAdress = address,
                                CustomerName = name,
                                CustomerEmail = email,
                                CustomerPhone = phone.ToString(),
                                QuantityLaptop = quantity,
                                TotalPrice = total
                            });

                            Console.WriteLine("Reservation saved.");
                        }

                        break;
                    }

                    // 3) View all reservations (list to console)
                    case "3":
                    {
                        foreach (var r in reservationService.GetAll())
                            Console.WriteLine(r);
                        break;
                    }

                    // 4) Export all reservations to a CSV file named by current date
                    case "4":
                    {
                        // File name like reservations_20250813.csv
                        var fileName = $"reservations_{DateTime.Now:yyyyMMdd}.csv";

                        // CSV header line
                        var lines = new List<string>
                        {
                            "ReservationId,Brand,Model,Quantity,TotalPrice,CustomerName,CustomerAddress,CustomerEmail,CustomerPhone"
                        };

                        // Map each reservation to a line of CSV
                        lines.AddRange(
                            reservationService.GetAll().Select(r =>
                                // NOTE: Check column order vs data fields carefully
                                $"{r.ReservationId},{r.Brand},{r.Model},{r.QuantityLaptop},{r.TotalPrice},{r.CustomerName},{r.CustomerAdress},{r.CustomerEmail},{r.CustomerPhone}"
                            )
                        );

                        // Write all lines to the CSV file
                        File.WriteAllLines(fileName, lines);

                        Console.WriteLine($"Exported to {fileName}");
                        break;
                    }

                    // 5) Delete a reservation by ID
                    case "5":
                    {
                        try
                        {
                            // Ask user which reservation to delete
                            Console.Write("Enter reservation ID to delete: ");
                            int id = int.Parse(Console.ReadLine() ?? "0"); // NOTE: will throw if input invalid

                            // Optional: fetch to confirm it exists (will throw or return object depending on impl)
                            var reservation = reservationService.GetReservationById(id);

                            // Perform deletion
                            reservationService.DeleteReservation(id);

                            Console.WriteLine("Reservation deleted.");
                        }
                        catch (Exception ex)
                        {
                            // Display any error (e.g., invalid input, reservation not found)
                            Console.WriteLine($" Error deleting reservation: {ex.Message}");
                        }

                        break;
                    }

                    // 6) Exit the application
                    case "6":
                    {
                        exit = true;
                        break;
                    }

                    // Anything else is invalid
                    default:
                    {
                        Console.WriteLine("Invalid choice");
                        break;
                    }
                }
            }
        }
    }
}
