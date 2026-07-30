using MySql.Data.MySqlClient;
using CsvHelper;
using System.Globalization;

namespace CTAndAI.CarReservationSystem.Repositories
{
    public class CarReservationRepository : ICarReservationRepository
    {
        private readonly string _connectionString;

        public CarReservationRepository(string connectionString)
        {
            _connectionString = connectionString;
        }

        public List<CarReservation> GetAllReservations()
        {
            var reservations = new List<CarReservation>();
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("SELECT * FROM CarReservations", connection);
                using (var reader = command.ExecuteReader()) //exceitreredaer alleen gebruken bij select wegens waarden neit buiten db query
                {
                    while (reader.Read())
                    {
                        reservations.Add(new CarReservation
                        {
                            Id = reader.GetInt32("Id"),
                            CarId = reader.GetInt32("CarId"),
                            CustomerName = reader.GetString("CustomerName"),
                            Duration = reader.GetInt32("Duration"),
                            Cost = reader.GetDecimal("Cost"),
                            ElectricRequired = reader.GetBoolean("ElectricRequired")
                        });
                    }
                }
            }
            return reservations;
        }

        public CarReservation GetReservationById(int id)
        {
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("SELECT * FROM CarReservations WHERE Id = @Id", connection);
                command.Parameters.AddWithValue("@Id", id);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return new CarReservation
                        {
                            Id = reader.GetInt32("Id"),
                            CarId = reader.GetInt32("CarId"),
                            CustomerName = reader.GetString("CustomerName"),
                            Duration = reader.GetInt32("Duration"),
                            Cost = reader.GetDecimal("Cost"),
                            ElectricRequired = reader.GetBoolean("ElectricRequired")
                        };
                    }
                }
            }
            return null;
        }
        
        //parsen gebeurt altijd in de repositry dus de klassen waarmee delete add of booking doen is de classe waarin iwe inde repistory gaan parsenene panning maken dus we boeken een reservaire lapop of auto gebeurt dit altijd heir in derepsitory addvalue is altijd bij ado net
        public void AddReservation(CarReservation reservation)
        {
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand(
                    "INSERT INTO CarReservations (CarId, CustomerName, Duration, Cost, ElectricRequired) VALUES (@CarId, @CustomerName, @Duration, @Cost, @ElectricRequired)",
                    connection);
                command.Parameters.AddWithValue("@CarId", reservation.CarId);
                command.Parameters.AddWithValue("@CustomerName", reservation.CustomerName);
                command.Parameters.AddWithValue("@Duration", reservation.Duration);
                command.Parameters.AddWithValue("@Cost", reservation.Cost);
                command.Parameters.AddWithValue("@ElectricRequired", reservation.ElectricRequired);
                command.ExecuteNonQuery();//gebriken we bij update inser t wgens niet ind e databse erbijbuiten
            }
        }

        public void UpdateReservation(CarReservation reservation)
        {
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand(
                    "UPDATE CarReservations SET CarId = @CarId, CustomerName = @CustomerName, Duration = @Duration, Cost = @Cost, ElectricRequired = @ElectricRequired WHERE Id = @Id", 
                    connection);
                command.Parameters.AddWithValue("@Id", reservation.Id);
                command.Parameters.AddWithValue("@CarId", reservation.CarId);
                command.Parameters.AddWithValue("@CustomerName", reservation.CustomerName);
                command.Parameters.AddWithValue("@Duration", reservation.Duration);
                command.Parameters.AddWithValue("@Cost", reservation.Cost);
                command.Parameters.AddWithValue("@ElectricRequired", reservation.ElectricRequired);
                command.ExecuteNonQuery();
            }
        }

        public void DeleteReservation(int id)
        {
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("DELETE FROM CarReservations WHERE Id = @Id", connection);
                command.Parameters.AddWithValue("@Id", id);
                command.ExecuteNonQuery();
            }
        }

        public decimal GetTotalCost()
        {
            using (var connection = new MySqlConnection(_connectionString))
            {
                connection.Open();
                var command = new MySqlCommand("SELECT SUM(Cost) FROM CarReservations", connection);
                var result = command.ExecuteScalar();
                return result == DBNull.Value ? 0 : Convert.ToDecimal(result);
            }
        }

        public void ExportToCsv(string filePath)
        {
            var reservations = GetAllReservations();
            using (var writer = new StreamWriter(filePath))
            using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
            {
                csv.WriteRecords(reservations);
            }
        }
    }
}