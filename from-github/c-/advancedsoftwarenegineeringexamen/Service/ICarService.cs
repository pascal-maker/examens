namespace CTAndAI.CarReservationSystem.Services
{
    public interface ICarService
    {
        Task<List<Car>> ImportCarsFromApiAsync();
        List<Car> GetAllCars();
        List<Car> GetElectricCars();
        Car GetCarById(int id);
    }
}
