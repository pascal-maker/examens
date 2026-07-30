namespace CTAndAI.CarReservationSystem.Repositories
{
    public interface ICarRepository
    {
        List<Car> GetAllCars();
        List<Car> GetElectricCars();
        Car GetCarById(int id);

        void ImportCarsFromApi(List<Car> cars);
    }
}