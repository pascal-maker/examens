using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace examenadvancedsoftwarengineering.Migrations
{
    /// <inheritdoc />
    public partial class AddReservationItemsAndRenameAddress : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "QuantityPerLaptop",
                table: "Reservations");

            migrationBuilder.RenameColumn(
                name: "CustomerAdress",
                table: "Reservations",
                newName: "CustomerAddress");

            migrationBuilder.AlterColumn<decimal>(
                name: "TotalPrice",
                table: "Reservations",
                type: "decimal(65,30)",
                nullable: false,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.CreateTable(
                name: "ReservationItems",
                columns: table => new
                {
                    ReservationItemID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    ReservationID = table.Column<int>(type: "int", nullable: false),
                    LaptopID = table.Column<int>(type: "int", nullable: false),
                    Quantity = table.Column<int>(type: "int", nullable: false),
                    UnitPrice = table.Column<decimal>(type: "decimal(65,30)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ReservationItems", x => x.ReservationItemID);
                    table.ForeignKey(
                        name: "FK_ReservationItems_Laptops_LaptopID",
                        column: x => x.LaptopID,
                        principalTable: "Laptops",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_ReservationItems_Reservations_ReservationID",
                        column: x => x.ReservationID,
                        principalTable: "Reservations",
                        principalColumn: "ReservationID",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.UpdateData(
                table: "Laptops",
                keyColumn: "ID",
                keyValue: 1,
                columns: new[] { "Brand", "DisplaySize", "GpuBrand", "GpuType", "Model", "OS", "PrimaryStorageType", "ProcessorBrand", "ProcessorTier", "ResolutionHeight", "ResolutionWidth" },
                values: new object[] { "Apple", 15.6m, "Apple Silicon", "Integrated", "MacBook Pro M5", "macOS", "SSD", "Apple Silicon", "M5", 1600, 2560 });

            migrationBuilder.UpdateData(
                table: "Laptops",
                keyColumn: "ID",
                keyValue: 2,
                columns: new[] { "Brand", "DisplaySize", "GpuType", "Model", "PrimaryStorageType", "ProcessorTier", "ResolutionHeight", "ResolutionWidth" },
                values: new object[] { "Windows", 15.6m, "Discrete", "X Series M4", "SSD", "High", 1080, 1920 });

            migrationBuilder.InsertData(
                table: "Reservations",
                columns: new[] { "ReservationID", "CustomerAddress", "CustomerEmail", "CustomerName", "CustomerPhone", "TotalPrice" },
                values: new object[,]
                {
                    { 1, "Boomstraat 30", "jean-jacquesvandewalle@hotmail.com", "Jean-Jacques", "0456180394", 0m },
                    { 2, "Stationlaan 1", "alice@example.com", "Alice", "0400000000", 0m }
                });

            migrationBuilder.InsertData(
                table: "ReservationItems",
                columns: new[] { "ReservationItemID", "LaptopID", "Quantity", "ReservationID", "UnitPrice" },
                values: new object[,]
                {
                    { 1, 1, 1, 1, 20.05m },
                    { 2, 2, 2, 1, 20000m },
                    { 3, 2, 1, 2, 20000m }
                });

            migrationBuilder.CreateIndex(
                name: "IX_ReservationItems_LaptopID",
                table: "ReservationItems",
                column: "LaptopID");

            migrationBuilder.CreateIndex(
                name: "IX_ReservationItems_ReservationID",
                table: "ReservationItems",
                column: "ReservationID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "ReservationItems");

            migrationBuilder.DeleteData(
                table: "Reservations",
                keyColumn: "ReservationID",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Reservations",
                keyColumn: "ReservationID",
                keyValue: 2);

            migrationBuilder.RenameColumn(
                name: "CustomerAddress",
                table: "Reservations",
                newName: "CustomerAdress");

            migrationBuilder.AlterColumn<int>(
                name: "TotalPrice",
                table: "Reservations",
                type: "int",
                nullable: false,
                oldClrType: typeof(decimal),
                oldType: "decimal(65,30)");

            migrationBuilder.AddColumn<decimal>(
                name: "QuantityPerLaptop",
                table: "Reservations",
                type: "decimal(65,30)",
                nullable: false,
                defaultValue: 0m);

            migrationBuilder.UpdateData(
                table: "Laptops",
                keyColumn: "ID",
                keyValue: 1,
                columns: new[] { "Brand", "DisplaySize", "GpuBrand", "GpuType", "Model", "OS", "PrimaryStorageType", "ProcessorBrand", "ProcessorTier", "ResolutionHeight", "ResolutionWidth" },
                values: new object[] { "Macbook", 150.46m, "Apple Sillicon", "Multithreading", "M5", "Catalina", "Ssd", "AppleSilicon", "Idk", 800, 200 });

            migrationBuilder.UpdateData(
                table: "Laptops",
                keyColumn: "ID",
                keyValue: 2,
                columns: new[] { "Brand", "DisplaySize", "GpuType", "Model", "PrimaryStorageType", "ProcessorTier", "ResolutionHeight", "ResolutionWidth" },
                values: new object[] { "Winodws", 150.46m, "Multithreading", "M4", "Ssd", "Big", 800, 200 });
        }
    }
}
