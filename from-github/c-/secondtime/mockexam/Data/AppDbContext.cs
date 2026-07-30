using Microsoft.EntityFrameworkCore;
using mockexam.Models;

namespace mockexam.Data
{
    public class AppDbContext : DbContext
    {
        public DbSet<Laptop> Laptops { get; set; } 

        public DbSet<Reservation> Reservations{ get; set; } 

        

          // 1. OnModelCreating is called by EF Core before creating the database.
//
// 2. modelBuilder.Entity<>() tells EF Core "configure this table/entity".
//
// 3. .HasData() says "insert this default data if it’s not already there".
//
// 4. EF Core creates the SQL INSERT statements during migrations.
//
// 5. When you run update-database, those INSERT statements run 
//    and your database starts with that data.

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
        // Call the base OnModelCreating (keeps default EF Core behavior
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Seed initial data into the Laptops table and Reservations table
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Laptop>()
                .HasData(new Laptop
                {
                    Id = 1, // Primary key must be set manually
                    Brand = "Dell",
                    Model = "XPS 13",
                    Price = 999,
                    Rating = 5,
                    ProcessorBrand = "Intel",
                    ProcessorTier = "Core i7",
                    NumCores = 4,
                    NumThreads = 8,
                    RamMemory = 16,
                    PrimaryStorageType = "SSD",
                    PrimaryStorageCapacity = 512,
                    SecondaryStorageType = "HDD",
                    SecondaryStorageCapacity = 1000,
                    GPUBrand = "NVIDIA",
                    GPUType = "GeForce GTX 1650",
                    IsTouchScreen = true,
                    DisplaySize = 13.3m,
                    ResolutionWidth = 1920,
                    ResolutionHeight = 1080,
                    OS = "Windows 10",
                    YearOfWarranty = 2
                },


                new Laptop
                {
                    Id = 2,
                    Brand = "Apple",
                    Model = "MacBook Pro",
                    Price = 1999,
                    Rating = 5,
                    ProcessorBrand = "Apple",
                    ProcessorTier = "M1",
                    NumCores = 8,
                    NumThreads = 16,
                    RamMemory = 16,
                    PrimaryStorageType = "SSD",
                    PrimaryStorageCapacity = 512,
                    SecondaryStorageType = "None",
                    SecondaryStorageCapacity = 0,
                    GPUBrand = "Apple",
                    GPUType = "Integrated",
                    IsTouchScreen = false,
                    DisplaySize = 13.3m,
                    ResolutionWidth = 2560,
                    ResolutionHeight = 1600,
                    OS = "macOS Big Sur",
                    YearOfWarranty = 1
                }


                );

            // Seed initial data into the Reservations table

            modelBuilder.Entity<Reservation>().HasData(
            new Reservation // First Reservation entry
            {
                ReservationId = 1, // Primary key
                CustomerAdress = "123 Main St, Cityville",
                CustomerName = "John Doe",
                CustomerEmail = "johndoe@hotmail.com",
                CustomerPhone = "123-456-7890",
                QuantityLaptop = 100,
                TotalPrice = 999.99m




            },

            new Reservation
            {
                ReservationId = 2,
                CustomerAdress = "456 Elm St, Townsville",
                CustomerName = "Jane Smith",
                CustomerEmail = "janesmith@gmail.com",
                CustomerPhone = "987-654-3210",
                QuantityLaptop = 50,
                TotalPrice = 1999.99m

            }

            );
            

            
           



            


        }

    }
}


// This code defines the AppDbContext class, which is used to interact with the database.


// Summary of seeding process:
    // 1. OnModelCreating is called before creating the database
    // 2. modelBuilder.Entity<>() configures the entity (table)
    // 3. .HasData() defines default rows to insert
    // 4. EF Core creates INSERT statements during migrations
    // 5. update-database runs those inserts so the DB starts with this data
