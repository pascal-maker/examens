using Newtonsoft.Json;

namespace CTAndAI.CarReservationSystem.Services
{
    public class CarService : ICarService
    {
        private readonly ICarRepository _carRepository;
        private readonly HttpClient _httpClient;

        public CarService(ICarRepository carRepository)
        {
            _carRepository = carRepository;
            _httpClient = new HttpClient();
        }

        public async Task<List<Car>> ImportCarsFromApiAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync(Constants.CarsApiUrl);
                response.EnsureSuccessStatusCode();
                
                var jsonContent = await response.Content.ReadAsStringAsync();
                var cars = JsonConvert.DeserializeObject<List<Car>>(jsonContent);
                
                if (cars != null)
                {
                    _carRepository.ImportCarsFromApi(cars);
                    return cars;
                }
                
                return new List<Car>();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error importing cars from API: {ex.Message}");
                return new List<Car>();
            }
        }

        public List<Car> GetAllCars()
        {
            return _carRepository.GetAllCars();
        }

        public List<Car> GetElectricCars()
        {
            return _carRepository.GetElectricCars();
        }

        public Car GetCarById(int id)
        {
            return _carRepository.GetCarById(id);
        }
    }
}
