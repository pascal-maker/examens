namespace CTAndAI.CarReservationSystem.Services
{
    public class CarReservationService : ICarReservationService
    {
        private readonly ICarReservationRepository _reservationRepository;
        private readonly ICarRepository _carRepository;

        public CarReservationService(ICarReservationRepository reservationRepository, ICarRepository carRepository)
        {
            _reservationRepository = reservationRepository;
            _carRepository = carRepository;
        }

        public void AddReservation(string customerName, int duration, bool electricRequired, int carId)
        {
            var car = _carRepository.GetCarById(carId);
            if (car == null)
            {
                throw new ArgumentException("Car not found");
            }

            if (electricRequired && !car.Electric)
            {
                throw new ArgumentException("Selected car is not electric but electric car is required");
            }

            var cost = car.PricePerDay * duration;
            var reservation = new CarReservation
            {
                CarId = carId,
                CustomerName = customerName,
                Duration = duration,
                Cost = cost,
                ElectricRequired = electricRequired
            };

            _reservationRepository.AddReservation(reservation);
        }

        public List<CarReservation> GetAllReservations()
        {
            return _reservationRepository.GetAllReservations();
        }

        public CarReservation GetReservationById(int id)
        {
            return _reservationRepository.GetReservationById(id);
        }

        public void UpdateReservation(int id, string customerName, int duration, bool electricRequired, int carId)
        {
            var car = _carRepository.GetCarById(carId);
            if (car == null)
            {
                throw new ArgumentException("Car not found");
            }

            if (electricRequired && !car.Electric)
            {
                throw new ArgumentException("Selected car is not electric but electric car is required");
            }

            var cost = car.PricePerDay * duration;
            var reservation = new CarReservation
            {
                Id = id,
                CarId = carId,
                CustomerName = customerName,
                Duration = duration,
                Cost = cost,
                ElectricRequired = electricRequired
            };

            _reservationRepository.UpdateReservation(reservation);
        }

        public decimal GetTotalCost()
        {
            return _reservationRepository.GetTotalCost();
        }

        public void ExportReservationsToCsv(string filePath)
        {
            _reservationRepository.ExportToCsv(filePath);
        }
    }
}
