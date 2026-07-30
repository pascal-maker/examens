using CTAndAI.CarReservationSystem.Services;
using CTAndAI.CarReservationSystem.Repositories;

namespace CTAndAI.CarReservationSystem
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // Initialize repositories and services
            var carRepository = new CarRepository(Constants.ConnectionString);
            var reservationRepository = new CarReservationRepository(Constants.ConnectionString);
            
            var carService = new CarService(carRepository);
            var reservationService = new CarReservationService(reservationRepository, carRepository);

            bool exit = false;
            while (!exit)
            {
                Console.Clear();
                Console.WriteLine("=== CAR RESERVATION SYSTEM ===");
                Console.WriteLine("1. Import cars from API");
                Console.WriteLine("2. Add Reservation");
                Console.WriteLine("3. Show Reservations");
                Console.WriteLine("4. Total Cost of Reservations");
                Console.WriteLine("5. Update Reservation");
                Console.WriteLine("6. Export reservations to CSV");
                Console.WriteLine("0. Exit");
                Console.Write("Enter your choice: ");

                var choice = Console.ReadLine();

                try
                {
                    switch (choice)
                    {
                        case "1":
                            await ImportCarsFromApi(carService);
                            break;
                        case "2":
                            AddReservation(reservationService, carService);
                            break;
                        case "3":
                            ShowReservations(reservationService);
                            break;
                        case "4":
                            ShowTotalCost(reservationService);
                            break;
                        case "5":
                            UpdateReservation(reservationService, carService);
                            break;
                        case "6":
                            ExportToCsv(reservationService);
                            break;
                        case "0":
                            exit = true;
                            Console.WriteLine("Goodbye!");
                            break;
                        default:
                            Console.WriteLine("Invalid choice. Press any key to continue...");
                            Console.ReadKey();
                            break;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                    Console.WriteLine("Press any key to continue...");
                    Console.ReadKey();
                }
            }
        }

        static async Task ImportCarsFromApi(ICarService carService)
        {
            Console.WriteLine("Importing cars from API...");
            var cars = await carService.ImportCarsFromApiAsync();
            Console.WriteLine($"Successfully imported {cars.Count} cars from API.");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

        static void AddReservation(ICarReservationService reservationService, ICarService carService)
        {
            Console.Write("Enter customer name: ");
            var customerName = Console.ReadLine();

            Console.Write("Enter duration in days: ");
            if (!int.TryParse(Console.ReadLine(), out int duration) || duration <= 0)
            {
                Console.WriteLine("Invalid duration. Must be a positive number.");
                Console.WriteLine("Press any key to continue...");
                Console.ReadKey();
                return;
            }

            Console.Write("Do you need an electric car? (y/n): ");
            var electricInput = Console.ReadLine()?.ToLower();
            var electricRequired = electricInput == "y" || electricInput == "yes";

            var cars = electricRequired ? carService.GetElectricCars() : carService.GetAllCars();
            
            if (!cars.Any())
            {
                Console.WriteLine("No cars available.");
                Console.WriteLine("Press any key to continue...");
                Console.ReadKey();
                return;
            }

            Console.WriteLine("\nAvailable cars:");
            foreach (var car in cars)
            {
                Console.WriteLine($"{car.Id}: {car.Brand} {car.Model} ({car.Year}) - ${car.PricePerDay}/day - Electric: {(car.Electric ? "Yes" : "No")}");
            }

            Console.Write("Enter car ID: ");
            if (!int.TryParse(Console.ReadLine(), out int carId))
            {
                Console.WriteLine("Invalid car ID.");
                Console.WriteLine("Press any key to continue...");
                Console.ReadKey();
                return;
            }

            reservationService.AddReservation(customerName, duration, electricRequired, carId);
            Console.WriteLine("Reservation added successfully!");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

        static void ShowReservations(ICarReservationService reservationService)
        {
            var reservations = reservationService.GetAllReservations();
            
            if (!reservations.Any())
            {
                Console.WriteLine("No reservations found.");
            }
            else
            {
                Console.WriteLine("\nCurrent Reservations:");
                Console.WriteLine("ID | Customer | Duration | Cost | Electric Required");
                Console.WriteLine("---|----------|----------|------|------------------");
                foreach (var reservation in reservations)
                {
                    Console.WriteLine($"{reservation.Id} | {reservation.CustomerName} | {reservation.Duration} days | ${reservation.Cost} | {(reservation.ElectricRequired ? "Yes" : "No")}");
                }
            }
            
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

        static void ShowTotalCost(ICarReservationService reservationService)
        {
            var totalCost = reservationService.GetTotalCost();
            Console.WriteLine($"Total cost of all reservations: ${totalCost}");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

        static void UpdateReservation(ICarReservationService reservationService, ICarService carService)
        {
            var reservations = reservationService.GetAllReservations();
            
            if (!reservations.Any())
            {
                Console.WriteLine("No reservations to update.");
                Console.WriteLine("Press any key to continue...");
                Console.ReadKey();
                return;
            }

            Console.WriteLine("\nCurrent Reservations:");
            foreach (var reservation in reservations)
            {
                Console.WriteLine($"{reservation.Id}: {reservation.CustomerName} - {reservation.Duration} days - ${reservation.Cost}");
            }

            Console.Write("Enter reservation ID to update: ");
            if (!int.TryParse(Console.ReadLine(), out int reservationId))
            {
                Console.WriteLine("Invalid reservation ID.");
                Console.WriteLine("Press any key to continue...");
                Console.ReadKey();
                return;
            }

            var existingReservation = reservationService.GetReservationById(reservationId);
            if (existingReservation == null)
            {
                Console.WriteLine("Reservation not found.");
                Console.WriteLine("Press any key to continue...");
                Console.ReadKey();
                return;
            }

            Console.Write($"Enter new customer name (current: {existingReservation.CustomerName}): ");
            var customerName = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(customerName))
                customerName = existingReservation.CustomerName;

            Console.Write($"Enter new duration in days (current: {existingReservation.Duration}): ");
            var durationInput = Console.ReadLine();
            int duration = existingReservation.Duration;
            if (!string.IsNullOrWhiteSpace(durationInput) && int.TryParse(durationInput, out int newDuration) && newDuration > 0)
                duration = newDuration;

            Console.Write($"Do you need an electric car? (y/n, current: {(existingReservation.ElectricRequired ? "y" : "n")}): ");
            var electricInput = Console.ReadLine()?.ToLower();
            var electricRequired = existingReservation.ElectricRequired;
            if (electricInput == "y" || electricInput == "yes")
                electricRequired = true;
            else if (electricInput == "n" || electricInput == "no")
                electricRequired = false;

            var cars = electricRequired ? carService.GetElectricCars() : carService.GetAllCars();
            Console.WriteLine("\nAvailable cars:");
            foreach (var car in cars)
            {
                Console.WriteLine($"{car.Id}: {car.Brand} {car.Model} ({car.Year}) - ${car.PricePerDay}/day");
            }

            Console.Write($"Enter new car ID (current: {existingReservation.CarId}): ");
            var carIdInput = Console.ReadLine();
            int carId = existingReservation.CarId;
            if (!string.IsNullOrWhiteSpace(carIdInput) && int.TryParse(carIdInput, out int newCarId))
                carId = newCarId;

            reservationService.UpdateReservation(reservationId, customerName, duration, electricRequired, carId);
            Console.WriteLine("Reservation updated successfully!");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

        static void ExportToCsv(ICarReservationService reservationService)
        {
            var fileName = $"reservations_{DateTime.Now:yyyyMMdd_HHmmss}.csv";
            reservationService.ExportReservationsToCsv(fileName);
            Console.WriteLine($"Reservations exported to {fileName}");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }
    }
}
