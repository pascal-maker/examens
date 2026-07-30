// EF Core basis-namespace (DbContext, DbContextOptionsBuilder, etc.)
using Microsoft.EntityFrameworkCore;

// Interface voor design-time factories (gebruikt door 'dotnet ef')
using Microsoft.EntityFrameworkCore.Design;

// Toegang tot je modelklassen (Reservation, Laptop, etc.)
using Laptopreservation.Models;

// Toegang tot je eigen Data-laag (waar AppDbContext staat)
using Laptopreservation.Data;

// Pomelo MySQL provider (ServerVersion, UseMySql, enz.)
using Pomelo.EntityFrameworkCore.MySql.Infrastructure;

// Namespace voor de hoofdapplicatie
namespace Laptopreservation
{
    // Definieert een factory die EF Core gebruikt tijdens design-time (bv. bij migraties)
    // Zonder deze factory weet 'dotnet ef' soms niet hoe een DbContext te maken
    public class AppDbContextFactory : IDesignTimeDbContextFactory<AppDbContext>
    {
        // Verplicht door de interface: maakt een AppDbContext voor design-time
        // 'args' bevat CLI-argumenten (meestal leeg bij design-time)
        public AppDbContext CreateDbContext(string[] args)
        {
            // Builder om opties (zoals connectiestring en provider) te configureren
            var optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();
            
            // Connectiestring naar je MySQL-database (moet overeenkomen met runtime-config)
            // LET OP: in productie liever via appsettings.json of user-secrets, niet hardcoded
            var connectionString = "server=localhost;database=examenadvancedsoftwarengineering;user=root;password=9370";
            
            // Configureer EF Core om Pomelo MySQL te gebruiken
            // ServerVersion.AutoDetect leest de versie van je MySQL-server en stelt EF correct in
            optionsBuilder.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));

            // Maak en retourneer een AppDbContext met de geconfigureerde opties
            return new AppDbContext(optionsBuilder.Options);
        }
    }
}
