namespace CTAndAI.CarReservationSystem.Repositories
{
    public interface ICarReservationRepository
    {
        List<CarReservation> GetAllReservations();
        CarReservation GetReservationById(int id);
        void AddReservation(CarReservation reservation);
        void UpdateReservation(CarReservation reservation);
        void DeleteReservation(int id);
        decimal GetTotalCost();
        void ExportToCsv(string filePath);
    }
} 