using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using mockexam.Data;
namespace mockexam.Data
{
    // This class implements IDesignTimeDbContextFactory to create the DbContext at design time
    
        // This class implements IDesignTimeDbContextFactory to create the DbContext at design tim
    public class AppDbContextFactory : IDesignTimeDbContextFactory<AppDbContext>
    // This class implements IDesignTimeDbContextFactory to create the DbContext at design time
    {         public AppDbContext CreateDbContext(string[] args)
        { 
             // Configure it to use MySQL with your connection string
            var optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();
            optionsBuilder.UseMySQL(
                "server=localhost;database=mockexam;user=root;password=9370"
                );
            // Return a new instance of AppDbContext with the configured options
            return new AppDbContext(optionsBuilder.Options);
        }
    }
}

