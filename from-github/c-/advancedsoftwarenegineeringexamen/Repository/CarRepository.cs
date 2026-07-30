using MySql.Data.MySqlClient;

namespace CTAndAI.CarReservationSystem.Repositories
{
    public class CarRepository : ICarRepository
    {
        private readonly string _connectionString;

        public CarRepository(string connectionString)
        {
            _connectionString = connectionString;
        }

        public List<Car> GetAllCars()
        {
            var cars = new List<Car>();
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("SELECT * FROM Cars", connection);
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        cars.Add(new Car
                        {
                            Id = reader.GetInt32("Id"),
                            Brand = reader.GetString("Brand"),
                            Model = reader.GetString("Model"),
                            Year = reader.GetInt32("Year"),
                            PricePerDay = reader.GetDecimal("PricePerDay"),
                            Electric = reader.GetBoolean("Electric"),
                            LicensePlate = reader.GetString("LicensePlate")
                        });
                    }
                }
            }
            return cars;
        }

        public List<Car> GetElectricCars()
        {
            var cars = new List<Car>();
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("SELECT * FROM Cars WHERE Electric = true", connection);
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        cars.Add(new Car
                        {
                            Id = reader.GetInt32("Id"),
                            Brand = reader.GetString("Brand"),
                            Model = reader.GetString("Model"),
                            Year = reader.GetInt32("Year"),
                            PricePerDay = reader.GetDecimal("PricePerDay"),
                            Electric = reader.GetBoolean("Electric"),
                            LicensePlate = reader.GetString("LicensePlate")
                        });
                    }
                }
            }
            return cars;
        }

        public Car GetCarById(int id)
        {
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("SELECT * FROM Cars WHERE Id = @Id", connection);
                command.Parameters.AddWithValue("@Id", id);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return new Car
                        {
                            Id = reader.GetInt32("Id"),
                            Brand = reader.GetString("Brand"),
                            Model = reader.GetString("Model"),
                            Year = reader.GetInt32("Year"),
                            PricePerDay = reader.GetDecimal("PricePerDay"),
                            Electric = reader.GetBoolean("Electric"),
                            LicensePlate = reader.GetString("LicensePlate")
                        };
                    }
                }
            }
            return null;
        }

        public void ImportCarsFromApi(List<Car> cars)
        {
            // First clear existing cars
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var clearCommand = new MySqlCommand("DELETE FROM Cars", connection);
                clearCommand.ExecuteNonQuery();

                // Then insert new cars
                foreach (var car in cars)
                {
                    var command = new MySqlCommand(
                        "INSERT INTO Cars (Id, Brand, Model, Year, PricePerDay, Electric, LicensePlate) VALUES (@Id, @Brand, @Model, @Year, @PricePerDay, @Electric, @LicensePlate)", 
                        connection);
                    command.Parameters.AddWithValue("@Id", car.Id);
                    command.Parameters.AddWithValue("@Brand", car.Brand);
                    command.Parameters.AddWithValue("@Model", car.Model);
                    command.Parameters.AddWithValue("@Year", car.Year);
                    command.Parameters.AddWithValue("@PricePerDay", car.PricePerDay);
                    command.Parameters.AddWithValue("@Electric", car.Electric);
                    command.Parameters.AddWithValue("@LicensePlate", car.LicensePlate);
                    command.ExecuteNonQuery();
                }
            }
        }
    }
}