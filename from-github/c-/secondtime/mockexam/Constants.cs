namespace mockexamSystem
{
    // Static class used to store constant values used throughout the application
    // This helps avoid "magic strings" spread in the code and makes them easy to change in one place
    public static class Constants
    {
        // API endpoint for fetching car data
        public const string CarsApiUrl = "https://ctandai-exam2-ase0c4dyf3gudxf9.northeurope-01.azurewebsites.net/cars";

        // Database connection string for connecting to the CarReservationSystem MySQL database
        public const string ConnectionString = "Server=localhost;Database=CarReservationSystem;Uid=root;Pwd=9370;";
    }
}
// This class contains constants for API URLs and database connection strings