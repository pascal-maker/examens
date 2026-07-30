using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Laptopreservation.Models;
using Laptopreservation.Data;
using Pomelo.EntityFrameworkCore.MySql.Infrastructure;


// Verwijst naar de namespace van de modellen (Laptop, Reservation, ReservationItem)
namespace Laptopreservation.Data
{
    // AppDbContext is de klasse die de verbinding met de database beheert via Entity Framework Core
    public class AppDbContext : DbContext
    {
        // DbSet property - vertegenwoordigt de 'Reservations' tabel in de database
        public DbSet<Reservation> Reservations { get; set; }

        // DbSet property - vertegenwoordigt de 'ReservationItems' tabel in de database (koppelt reservaties aan laptops)
        public DbSet<ReservationItem> ReservationItems { get; set; }

        // DbSet property - vertegenwoordigt de 'Laptops' tabel in de database
        public DbSet<Laptop> Laptops { get; set; }

        // Constructor van AppDbContext - ontvangt opties (zoals connectiestring) en geeft ze door aan de DbContext
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        // OnModelCreating methode - wordt aangeroepen door Entity Framework Core
        // om het database model en relaties te configureren
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Bel eerst de standaard Entity Framework configuratie aan
            base.OnModelCreating(modelBuilder);

            // ===============================
            // RELATIES TUSSEN DE TABELLEN
            // ===============================

            // Configureer de relatie: één Reservation heeft meerdere ReservationItems
            modelBuilder.Entity<ReservationItem>()
                .HasOne(ri => ri.Reservation)        // ReservationItem heeft één Reservation
                .WithMany(r => r.Items)              // Reservation heeft veel ReservationItems
                .HasForeignKey(ri => ri.ReservationID) // Gebruik ReservationID als foreign key
                .OnDelete(DeleteBehavior.Cascade);   // Als een Reservation verwijderd wordt, verwijder ook zijn Items

            // Configureer de relatie: één Laptop kan in meerdere ReservationItems gebruikt worden
            modelBuilder.Entity<ReservationItem>()
                .HasOne(ri => ri.Laptop)             // ReservationItem heeft één Laptop
                .WithMany()                          // Laptop heeft GEEN lijst van ReservationItems (unidirectioneel)
                .HasForeignKey(ri => ri.LaptopID)    // Gebruik LaptopID als foreign key
                .OnDelete(DeleteBehavior.Restrict);  // Als een Laptop verwijderd wordt: blokkeer verwijdering (omdat reservatie afhankelijk is)

            // ===============================
            // DATA SEEDING - laptops
            // ===============================

            // Voeg voorbeeld laptops toe (wordt in database geplaatst bij eerste migratie)
            modelBuilder.Entity<Laptop>().HasData(
                new Laptop
                {
                    ID = 1,
                    Brand = "Apple",
                    Model = "MacBook Pro M5",
                    Price = 2005,
                    Rating = 100,
                    ProcessorBrand = "Apple Silicon",
                    ProcessorTier = "M5",
                    NumCores = 12,
                    NumThreads = 36,
                    RamMemory = 38,
                    PrimaryStorageType = "SSD",
                    PrimaryStorageCapacity = 1000,
                    SecondaryStorageType = "HDD",
                    SecondaryStorageCapacity = 2000,
                    GpuBrand = "Apple Silicon",
                    GpuType = "Integrated",
                    IsTouchScreen = false,
                    DisplaySize = 15.6m,       // 'm' betekent decimal literal
                    ResolutionWidth = 2560,
                    ResolutionHeight = 1600,
                    OS = "macOS",
                    YearOfWarranty = 2030
                },
                new Laptop
                {
                    ID = 2,
                    Brand = "Windows",
                    Model = "X Series M4",
                    Price = 2000000,
                    Rating = 100,
                    ProcessorBrand = "Nvidia",
                    ProcessorTier = "High",
                    NumCores = 12,
                    NumThreads = 36,
                    RamMemory = 38,
                    PrimaryStorageType = "SSD",
                    PrimaryStorageCapacity = 1000,
                    SecondaryStorageType = "HDD",
                    SecondaryStorageCapacity = 2000,
                    GpuBrand = "Nvidia",
                    GpuType = "Discrete",
                    IsTouchScreen = true,
                    DisplaySize = 15.6m,
                    ResolutionWidth = 1920,
                    ResolutionHeight = 1080,
                    OS = "Windows",
                    YearOfWarranty = 2030
                }
            );

            // ===============================
            // DATA SEEDING - reservations
            // ===============================

            // Voeg 2 voorbeeldreservaties toe met klantgegevens
            modelBuilder.Entity<Reservation>().HasData(
                new Reservation
                {
                    ReservationID = 1,
                    CustomerName = "Jean-Jacques",
                    CustomerAddress = "Boomstraat 30",
                    CustomerEmail = "jean-jacquesvandewalle@hotmail.com",
                    CustomerPhone = "0456180394",
                    TotalPrice = 0m // Wordt later berekend uit de ReservationItems
                },
                new Reservation
                {
                    ReservationID = 2,
                    CustomerName = "Alice",
                    CustomerAddress = "Stationlaan 1",
                    CustomerEmail = "alice@example.com",
                    CustomerPhone = "0400000000",
                    TotalPrice = 0m
                }
            );

            // ===============================
            // DATA SEEDING - reservation items
            // ===============================

            // Voeg voorbeeld items toe
            // Let op: UnitPrice = Laptop.Price / 100 (zoals de opdracht voorschrijft)
            modelBuilder.Entity<ReservationItem>().HasData(
                new ReservationItem
                {
                    ReservationItemID = 1,
                    ReservationID = 1,     // hoort bij reservatie 1
                    LaptopID = 1,          // laptop met ID 1
                    Quantity = 1,          // 1 stuk
                    UnitPrice = 2005m / 100m // prijs gedeeld door 100 → 20.05
                },
                new ReservationItem
                {
                    ReservationItemID = 2,
                    ReservationID = 1,     // hoort bij reservatie 1
                    LaptopID = 2,          // laptop met ID 2
                    Quantity = 2,          // 2 stuks
                    UnitPrice = 2000000m / 100m // prijs gedeeld door 100 → 20.000
                },
                new ReservationItem
                {
                    ReservationItemID = 3,
                    ReservationID = 2,     // hoort bij reservatie 2
                    LaptopID = 2,          // laptop met ID 2
                    Quantity = 1,
                    UnitPrice = 2000000m / 100m
                }
            );
        }
    }
}
