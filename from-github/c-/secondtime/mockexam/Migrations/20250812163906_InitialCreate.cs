using Microsoft.EntityFrameworkCore.Migrations;
using MySql.EntityFrameworkCore.Metadata;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace mockexam.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterDatabase()
                .Annotation("MySQL:Charset", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Laptops",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySQL:ValueGenerationStrategy", MySQLValueGenerationStrategy.IdentityColumn),
                    Brand = table.Column<string>(type: "longtext", nullable: false),
                    Model = table.Column<string>(type: "longtext", nullable: false),
                    Price = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    Rating = table.Column<int>(type: "int", nullable: false),
                    ProcessorBrand = table.Column<string>(type: "longtext", nullable: false),
                    ProcessorTier = table.Column<string>(type: "longtext", nullable: false),
                    NumCores = table.Column<int>(type: "int", nullable: false),
                    NumThreads = table.Column<string>(type: "longtext", nullable: false),
                    RamMemory = table.Column<int>(type: "int", nullable: false),
                    PrimaryStorageType = table.Column<string>(type: "longtext", nullable: false),
                    PrimaryStorageCapacity = table.Column<int>(type: "int", nullable: false),
                    SecondaryStorageType = table.Column<string>(type: "longtext", nullable: false),
                    SecondaryStorageCapacity = table.Column<int>(type: "int", nullable: false),
                    GpuBrand = table.Column<string>(type: "longtext", nullable: false),
                    GpuType = table.Column<string>(type: "longtext", nullable: false),
                    IsTouchScreen = table.Column<bool>(type: "tinyint(1)", nullable: false),
                    DisplaySize = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    ResolutionWidth = table.Column<int>(type: "int", nullable: false),
                    ResolutionHeight = table.Column<int>(type: "int", nullable: false),
                    OS = table.Column<string>(type: "longtext", nullable: false),
                    YearOfWarranty = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Laptops", x => x.Id);
                })
                .Annotation("MySQL:Charset", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Reservations",
                columns: table => new
                {
                    ReservationId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySQL:ValueGenerationStrategy", MySQLValueGenerationStrategy.IdentityColumn),
                    CustomerAdress = table.Column<string>(type: "longtext", nullable: false),
                    CustomerName = table.Column<string>(type: "longtext", nullable: false),
                    CustomerEmail = table.Column<string>(type: "longtext", nullable: false),
                    CustomerPhone = table.Column<string>(type: "longtext", nullable: false),
                    QuantityLaptop = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    TotalPrice = table.Column<decimal>(type: "decimal(18,2)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Reservations", x => x.ReservationId);
                })
                .Annotation("MySQL:Charset", "utf8mb4");

            migrationBuilder.InsertData(
                table: "Laptops",
                columns: new[] { "Id", "Brand", "DisplaySize", "GpuBrand", "GpuType", "IsTouchScreen", "Model", "NumCores", "NumThreads", "OS", "Price", "PrimaryStorageCapacity", "PrimaryStorageType", "ProcessorBrand", "ProcessorTier", "RamMemory", "Rating", "ResolutionHeight", "ResolutionWidth", "SecondaryStorageCapacity", "SecondaryStorageType", "YearOfWarranty" },
                values: new object[,]
                {
                    { 1, "Dell", 13.3m, "NVIDIA", "GeForce GTX 1650", true, "XPS 13", 4, "8", "Windows 10", 999.99m, 512, "SSD", "Intel", "Core i7", 16, 5, 1080, 1920, 1000, "HDD", 2 },
                    { 2, "Apple", 13.3m, "Apple", "Integrated", false, "MacBook Pro", 8, "16", "macOS Big Sur", 1999.99m, 512, "SSD", "Apple", "M1", 16, 5, 1600, 2560, 0, "None", 1 }
                });

            migrationBuilder.InsertData(
                table: "Reservations",
                columns: new[] { "ReservationId", "CustomerAdress", "CustomerEmail", "CustomerName", "CustomerPhone", "QuantityLaptop", "TotalPrice" },
                values: new object[,]
                {
                    { 1, "123 Main St, Cityville", "johndoe@hotmail.com", "John Doe", "123-456-7890", 100m, 999.99m },
                    { 2, "456 Elm St, Townsville", "janesmith@gmail.com", "Jane Smith", "987-654-3210", 50m, 1999.99m }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Laptops");

            migrationBuilder.DropTable(
                name: "Reservations");
        }
    }
}
