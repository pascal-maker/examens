namespace CTAndAI.CarReservationSystem.Services
{
    public interface ICarReservationService
    {
        void AddReservation(string customerName, int duration, bool electricRequired, int carId);
        List<CarReservation> GetAllReservations();
        CarReservation GetReservationById(int id);
        void UpdateReservation(int id, string customerName, int duration, bool electricRequired, int carId);
        decimal GetTotalCost();
        void ExportReservationsToCsv(string filePath);
    }
}
